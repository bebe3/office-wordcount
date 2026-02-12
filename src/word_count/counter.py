"""Core word counting functionality.

This module provides text analysis functions that count words
in a manner compatible with Microsoft Office's word count feature.
"""

from __future__ import annotations

from word_count.patterns import (
    ASIANS,
    BREAKS,
    CHAR_EXCLUDES,
    NON_ASIAN_WORDS,
    SPACES,
    UNICODE_SEPARATORS,
)
from word_count.statistics import Statistics


def count_words(text: str) -> int:
    """Count total words in text.

    Implements Microsoft Office-style word counting where:
    - Non-Asian text is split by whitespace (each token = 1 word)
    - Asian characters (CJK) are counted individually (each char = 1 word)

    Args:
        text: The input text to analyze.

    Returns:
        Total word count.

    Example:
        >>> count_words("Hello World")
        2
        >>> count_words("Hello 世界")
        3
    """
    asian_characters = sum(len(m.group()) for m in ASIANS.finditer(text))
    non_asian_words = sum(1 for _ in NON_ASIAN_WORDS.finditer(text))
    separator_words = sum(1 for _ in UNICODE_SEPARATORS.finditer(text))
    return non_asian_words + asian_characters + separator_words


def count_characters(text: str) -> int:
    """Count characters excluding whitespace.

    Args:
        text: The input text to analyze.

    Returns:
        Character count without any whitespace.

    Example:
        >>> count_characters("Hello World")
        10
    """
    stripped = SPACES.sub("", text)
    return len(CHAR_EXCLUDES.sub("", stripped))


def count_characters_with_space(text: str) -> int:
    """Count characters including spaces but excluding line breaks.

    Args:
        text: The input text to analyze.

    Returns:
        Character count with spaces, excluding line breaks.

    Example:
        >>> count_characters_with_space("Hello World")
        11
    """
    stripped = BREAKS.sub("", text)
    return len(CHAR_EXCLUDES.sub("", stripped))


def calculate_word_statistics(text: str) -> Statistics:
    """Calculate all word and character statistics for the given text.

    This is a convenience function that returns all statistics at once.
    Use individual functions (count_words, count_characters, etc.) if you
    only need specific values.

    Args:
        text: The input text to analyze. Can contain any Unicode characters.

    Returns:
        Statistics object containing all word and character counts.

    Example:
        >>> stats = calculate_word_statistics("Hello 世界")
        >>> stats.words
        3
        >>> stats.to_dict()
        {'words': 3, 'characters_no_space': 7, ...}
    """
    asian_characters = sum(len(m.group()) for m in ASIANS.finditer(text))
    non_asian_words = sum(1 for _ in NON_ASIAN_WORDS.finditer(text))
    separator_words = sum(1 for _ in UNICODE_SEPARATORS.finditer(text))

    return Statistics(
        words=non_asian_words + asian_characters + separator_words,
        characters_no_space=count_characters(text),
        characters_with_space=count_characters_with_space(text),
        non_asian_words=non_asian_words,
        asian_characters=asian_characters,
    )
