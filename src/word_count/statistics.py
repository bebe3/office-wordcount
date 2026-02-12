"""Statistics dataclass for word count results."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Statistics:
    """Immutable container for text statistics.

    This dataclass holds the results of text analysis, providing both
    combined word counts and separate metrics for Asian and non-Asian text.

    Attributes:
        words: Total word count (non_asian_words + asian_characters).
               This matches Microsoft Office's word counting behavior.
        characters_no_space: Total character count excluding whitespace.
        characters_with_space: Total character count excluding only line breaks.
        non_asian_words: Count of whitespace-separated non-Asian words.
        asian_characters: Count of individual Asian characters (CJK, etc.).

    Example:
        >>> stats = Statistics(
        ...     words=15,
        ...     characters_no_space=45,
        ...     characters_with_space=50,
        ...     non_asian_words=5,
        ...     asian_characters=10,
        ... )
        >>> stats.words
        15
    """

    words: int
    characters_no_space: int
    characters_with_space: int
    non_asian_words: int
    asian_characters: int

    def to_dict(self) -> dict[str, int]:
        """Convert statistics to a dictionary.

        Returns:
            Dictionary with all statistics fields and their values.
        """
        return asdict(self)

    def __add__(self, other: Statistics) -> Statistics:
        """Add two Statistics objects together.

        Useful for aggregating statistics from multiple files.

        Args:
            other: Another Statistics object to add.

        Returns:
            New Statistics object with summed values.
        """
        return Statistics(
            words=self.words + other.words,
            characters_no_space=self.characters_no_space + other.characters_no_space,
            characters_with_space=(
                self.characters_with_space + other.characters_with_space
            ),
            non_asian_words=self.non_asian_words + other.non_asian_words,
            asian_characters=self.asian_characters + other.asian_characters,
        )
