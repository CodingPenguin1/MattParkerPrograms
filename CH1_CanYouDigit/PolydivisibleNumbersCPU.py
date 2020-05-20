#!/usr/bin/env python
import concurrent.futures
import time
from math import ceil, floor, log10
from multiprocessing import cpu_count

import numpy as np
from numba import jit


def getPolydivisibleNumbers(minVal, maxVal):
    polydivisibleNumbers = []
    for n in range(minVal, maxVal):
        # nstr = str(n)
        polydivisible = True

        if n == 0:
            polydivisibleNumbers.append(0)
            continue

        numDigits = floor(log10(n)) + 1
        for i in range(0, numDigits):
            num = n // (10 ** i)
            if num % (numDigits - i) != 0:
                polydivisible = False
                break
        if polydivisible:
            polydivisibleNumbers.append(n)
    return polydivisibleNumbers


if __name__ == '__main__':
    maxValue = int(input('Enter max value to check: '))
    CPU_COUNT = cpu_count()
    print(f'{CPU_COUNT} cores detected')

    func = None
    if maxValue < 2 ** 64:
        func = jit(getPolydivisibleNumbers, nopython=True, nogil=True)
        print('Using JIT compilation')
    else:
        func = getPolydivisibleNumbers
        print('Value too large, unable to JIT compile')

    # max = 3608528850368400786036725
    # 3,608,528,850,368,400,786,036,725
    # print(getPolydivisibleNumbers(3608528850368400786036725, 3608528850368400786036726))

    start = time.perf_counter()

    polydivisibleNumbers = []

    ranges = []
    for i in range(CPU_COUNT):
        ranges.append((maxValue * i // CPU_COUNT, maxValue * (i + 1) // CPU_COUNT))

    with concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT) as executor:
        results = [executor.submit(func, range_[0], range_[1]) for range_ in ranges]

        for i, f in enumerate(concurrent.futures.as_completed(results)):
            print(f'{i + 1} / {CPU_COUNT} processes completed')
            polydivisibleNumbers.extend(f.result())

    finish = time.perf_counter()

    # Sort results and print
    polydivisibleNumbers.sort()
    for n in polydivisibleNumbers:
        print(n)

    print(f'Found {len(polydivisibleNumbers)} numbers')

    print(f'Finished in {round(finish - start, 2)} seconds')
