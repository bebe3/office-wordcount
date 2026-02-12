"""
office-wordcount: Word counting that handles mixed Asian and non-Asian text.

This module provides word counting functionality similar to Microsoft Office,
where Asian characters (CJK) are counted individually while non-Asian text
is counted by whitespace-separated words.
"""

from word_count.counter import (
    calculate_word_statistics,
    count_characters,
    count_characters_with_space,
    count_words,
)
from word_count.statistics import Statistics

__version__ = "1.0.1"
__all__ = [
    "Statistics",
    "__version__",
    "calculate_word_statistics",
    "count_characters",
    "count_characters_with_space",
    "count_words",
]
