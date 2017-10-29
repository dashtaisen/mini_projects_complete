"""
Nicholas A Miller
27 October 2017

Problem 125: palindromic sums of consecutive squares

The palindromic number 595 is interesting because it can be written as the sum of consecutive squares: 62 + 72 + 82 + 92 + 102 + 112 + 122.

There are exactly eleven palindromes below one-thousand that can be written as consecutive square sums, and the sum of these palindromes is 4164. Note that 1 = 02 + 12 has not been included as this problem is concerned with the squares of positive integers.

Find the sum of all the numbers less than 10^8 that are both palindromic and can be written as the sum of consecutive squares.
"""

import math

def is_palindrome(s):
    """Recursively check if a string is a palindrome"""
    if len(s) < 2:
        return True
    elif not s[0] == s[-1]:
        return False
    else:
        return is_palindrome(s[1:-1])

def get_palindrome_sum(max_number):
    """Find sum of all palindromic square-sums up to max_number
    Inputs:
        max_number: maximum number to search to
    Returns:
        sum of palindromic numbers
    """
    #Use a set in case there are duplicates
    palindromes = set()
    #Only need to iterate up to sqrt, since we're squaring
    for i in range(1,int(math.sqrt(max_number))):
        #Start with the first squared number
        current = i**2
        for j in range(i+1,int(math.sqrt(max_number))):
            #Iterate over each consecutive square
            current += j**2
            #Stop if we hit the maximum
            if current > max_number:
                break
            if is_palindrome(str(current)):
                palindromes.add(current)
    #print(sorted(palindromes))
    return sum(palindromes)

if __name__ == "__main__":
    palindrome_sum = get_palindrome_sum(10**8)
    print(palindrome_sum)
    assert palindrome_sum == 2906969179
    print("OK!")
