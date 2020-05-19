#!/usr/bin/env python

from itertools import permutations


def checkPermutation(permutation):
    # Split number into each section to check
    subNumbers = []
    for i in range(2, len(permutation) + 1):  # No point checking the first digit alone because every number is divisible by 1
        subNumbers.append(int(float(''.join(permutation[:i]))))

    # Check each section
    valid = True
    for i, n in enumerate(subNumbers):
        if n % (i + 2) != 0:  # Check n % (i + 2) instead of n % (i + 1) because we chopped the 0th index from the list, so i is shifted down 1
            valid = False

    # Return number if valid
    if valid:
        return subNumbers[len(subNumbers) - 1]


if __name__ == '__main__':
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    permutations = [p for p in permutations(digits)]
    for p in permutations:
        validPermutation = checkPermutation(p)
        if validPermutation is not None:
            print(validPermutation)
