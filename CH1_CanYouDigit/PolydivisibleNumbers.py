#!/usr/bin/env python
from multiprocessing import cpu_count

import numpy as np

import concurrent.futures
import time


def getPolydivisibleNumbers(minVal, maxVal):
    polydivisibleNumbers = []
    for n in range(minVal, maxVal):
        nstr = str(n)
        polydivisible = True
        for i in range(len(nstr), 1, -1):
            num = int(nstr[:i])
            if num % i != 0:
                polydivisible = False
                break
        if polydivisible:
            polydivisibleNumbers.append(n)
    return polydivisibleNumbers


if __name__ == '__main__':
    maxValue = int(input('Enter max value to check: '))
    CPU_COUNT = cpu_count()
    print(f'{CPU_COUNT} cores detected')

    # max = 3608528850368400786036725
    # print(getPolydivisibleNumbers(3608528850368400786036725, 3608528850368400786036726))

    start = time.perf_counter()

    polydivisibleNumbers = []

    ranges = []
    for i in range(CPU_COUNT):
        ranges.append((maxValue * i // CPU_COUNT, maxValue * (i + 1) // CPU_COUNT))

    with concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT) as executor:
        results = [executor.submit(getPolydivisibleNumbers, range_[0], range_[1]) for range_ in ranges]

        for i, f in enumerate(concurrent.futures.as_completed(results)):
            print(f'{i + 1} / {CPU_COUNT} processes completed')
            polydivisibleNumbers.extend(f.result())

    finish = time.perf_counter()

    # Sort results and print
    polydivisibleNumbers.sort()
    for n in polydivisibleNumbers:
        print(n)

    print(f'Finished in {round(finish - start, 2)} seconds')
