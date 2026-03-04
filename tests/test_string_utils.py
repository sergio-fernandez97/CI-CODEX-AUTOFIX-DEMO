from src.string_utils import reverse_string, count_vowels, is_palindrome


def test_reverse_string():
    assert reverse_string("abc") == "cba"


def test_count_vowels():
    assert count_vowels("hello") == 2


def test_palindrome_true():
    assert is_palindrome("level") is True


def test_palindrome_false():
    assert is_palindrome("python") is False