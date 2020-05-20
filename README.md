# Matt Parker Programs

This repository is a collection of programs that solve puzzles and problems introduced in [Matt Parker](http://standupmaths.com/)'s *[Things to Make and Do in the Fourth Dimension](http://makeanddo4d.com/)*

## Nine Digits Arrangement

The objective of this puzzle is to arrange all 9 digits sequentially such that the number formed by the digits up to each index is divisible by the index + 1. For example, the sequence 1 2 3 4 5 6 7 8 9 starts to follow this property for the first few digits:

"1" is divisible by 1

"12" is divisible by 2

"123" is divisible by 3

The pattern ends at the fourth digit, as 1234 over 4 is 308.5. There is one 9-digit number that uses each digit only once and has this property of divisibility. This program finds this number.

In case you want to solve it by hand, I've hidden the answer:

<details><summary>ANSWER</summary>

`381654729`

</details>

## Polydivisible Numbers

[From Wikipedia](https://en.wikipedia.org/wiki/Polydivisible_number): In mathematics a polydivisible number (or magic number) is a number in a given number base with digits abcde... that has the following properties:

Its first digit a is not 0.

The number formed by its first two digits ab is a multiple of 2.

The number formed by its first three digits abc is a multiple of 3.

The number formed by its first four digits abcd is a multiple of 4.

This is different than [Nine Digits Arrangement](##Nine-Digits-Arrangement) in that digits can be excluded or repeated in the number, the range of allowable digits includes 0, and the number of digits allowed is infinite.

This program finds all polydivisible numbers up to a user-specified max value.

<details><summary>LIST OF ALL 20,456 POLYDIVISIBLE NUMBERS</summary>

```

```

</details>
