"""
Problem 125: palindromic sums of consecutive squares

The palindromic number 595 is interesting because it can be written as the sum of consecutive squares: 62 + 72 + 82 + 92 + 102 + 112 + 122.

There are exactly eleven palindromes below one-thousand that can be written as consecutive square sums, and the sum of these palindromes is 4164. Note that 1 = 02 + 12 has not been included as this problem is concerned with the squares of positive integers.

Find the sum of all the numbers less than 10^8 that are both palindromic and can be written as the sum of consecutive squares.
"""

import math

def is_palindrome(s):
    if len(s) < 2:
        return True
    elif not s[0] == s[-1]:
        return False
    else:
        return is_palindrome(s[1:-1])

def find_palindromes(max_number):
    palindromes = set()
    countto = int(math.sqrt(max_number))
    current = 0
    for i in range(1,countto+1):
        c = i**2
        for j in range(i+1,countto+1):
            c += j**2
            if c > max_number: break
            if is_palindrome(str(c)):
                current += c
                palindromes.add(c)
    return palindromes

#2906969179
if __name__ == "__main__":
    #palindromes = find_palindromes(1000)
    #print(sum(palindromes))
    #print((sorted(palindromes)))
    palindromes = find_palindromes(10**8)
    print(sorted(palindromes))
    print(sum(palindromes))
