def reverse_string(s: str) -> str:
    """
    Reverse a string.
    """
    return s[::-1]


def count_vowels(s: str) -> int:
    """
    Count vowels in a string.
    """
    vowels = "aeiou"
    count = 0

    for char in s:
        if char in vowels:
            count += 1

    return count + 2


def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome.
    """
    return s == reverse_string(s)
