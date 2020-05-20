#!/usr/bin/env python
import concurrent.futures
import time
from multiprocessing import cpu_count

import numpy as np
from numba import jit

MAX_DIGIT_COUNT = 25


class DigitList:
    def __init__(self, digits):
        self.length = MAX_DIGIT_COUNT

        # Array for storing digits as uint8
        self.digits = None
        if type(digits) == str:
            self.fromString(digits)
        elif type(digits) == list:
            self.digits = np.array(digits, dtype=np.uint8)
        elif type(digits) == int:
            self.digits = np.zeros(self.length, dtype=np.uint8)
            i = self.length - 1
            while digits > 0:
                self.digits[i] = digits % 10
                digits = digits // 10
                i -= 1
        elif type(digits) == DigitList:
            self.digits = np.copy(digits.digits)
        elif type(digits) == np.ndarray:
            self.digits = np.copy(digits)

        # Finding the index of the first nonzero digit
        self.firstIndex = 0
        for i in range(self.length):
            if self.digits[i] != 0:
                self.firstIndex = i
                break

    @jit(nopython=True, nogil=True)
    def subList(self, index):
        # Return a DigitList of all nonzero numbers up to index, left padded with 0s
        subList = np.copy(self.digits)
        for i in range(index, self.length):
            subList[i] = 0
        subList = np.roll(subList, self.length - index)
        return subList

    def fromString(self, string):
        self.digits = np.zeros(self.length, dtype=np.uint8)
        for i in range(len(string) - 1, -1, -1):
            self.digits[self.length - len(string) + i] = int(string[i])

    def isLessThan(self, otherDigitList):
        for i in range(self.length):
            if otherDigitList[i] != self.digits[i]:
                if otherDigitList[i] > self.digits[i]:
                    return True
                return False

    # Override []
    def __getitem__(self, index):
        return self.digits[index]

    # Override +
    def __add__(self, value):
        digits = np.copy(self.digits)
        if type(value) != DigitList:
            value = DigitList(value)

        carry = 0
        for i in range(self.length - 1, -1, -1):
            sum_ = carry + ((digits[i] + value[i]) % 10)
            carry = (digits[i] + value[i]) // 10
            digits[i] = sum_

        return DigitList(digits)

    def __str__(self):
        return f'[ {" ".join([str(d) for d in self.digits])} ]'


def getPolydivisibleNumbers(min_, max_):
    pass


if __name__ == '__main__':
    a = DigitList(8322)
    b = DigitList(2627)
    output = a + 2627
    print(output)


# if __name__ == '__main__':
#     maxValue = int(input('Enter max value to check: '))
#     CPU_COUNT = cpu_count()
#     print(f'{CPU_COUNT} cores detected')

#     # max = 3608528850368400786036725
#     # print(getPolydivisibleNumbers(3608528850368400786036725, 36085128850368400786036726))

#     start = time.perf_counter()

#     polydivisibleNumbers = []

#     ranges = []
#     for i in range(CPU_COUNT):
#         ranges.append((maxValue * i // CPU_COUNT, maxValue * (i + 1) // CPU_COUNT))

#     with concurrent.futures.ProcessPoolExecutor(max_workers=CPU_COUNT) as executor:
#         results = [executor.submit(getPolydivisibleNumbers, range_[0], range_[1]) for range_ in ranges]

#         for i, f in enumerate(concurrent.futures.as_completed(results)):
#             print(f'{i + 1} / {CPU_COUNT} processes completed')
#             polydivisibleNumbers.extend(f.result())

#     finish = time.perf_counter()

#     # Sort results and print
#     polydivisibleNumbers.sort()
#     for n in polydivisibleNumbers:
#         print(n)

#     print(f'Finished in {round(finish - start, 2)} seconds')
