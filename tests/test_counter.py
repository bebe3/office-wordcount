"""Tests for the word counting functionality."""

import pytest

from word_count import (
    calculate_word_statistics,
    count_characters,
    count_characters_with_space,
    count_words,
)
from word_count.statistics import Statistics


class TestCalculateWordStatistics:
    """Test cases for calculate_word_statistics function."""

    def test_english_only(self) -> None:
        """Test counting English text with spaces and punctuation."""
        result = calculate_word_statistics("Hello Python World. 3.14.")
        assert result == Statistics(
            words=4,
            characters_no_space=22,  # HelloPythonWorld.3.14.
            characters_with_space=25,  # includes spaces
            non_asian_words=4,
            asian_characters=0,
        )

    def test_japanese_only(self) -> None:
        """Test counting Japanese text (Asian characters only)."""
        result = calculate_word_statistics("こんにちは世界。")
        # Each Japanese character counts as one word
        assert result.words == 8  # 7 chars + 1 punctuation
        assert result.asian_characters == 8
        assert result.non_asian_words == 0

    def test_mixed_english_japanese(self) -> None:
        """Test counting mixed English and Japanese text."""
        result = calculate_word_statistics("Hello 世界")
        assert result.words == 3  # 1 English word + 2 Japanese chars
        assert result.non_asian_words == 1
        assert result.asian_characters == 2

    def test_mixed_with_newlines(self) -> None:
        """Test mixed text with line breaks."""
        result = calculate_word_statistics("Pytest 7.0\nこれはテストです。")
        assert result.non_asian_words == 2  # Pytest, 7.0
        assert result.asian_characters == 9  # Japanese chars + punctuation

    def test_fullwidth_symbols(self) -> None:
        """Test that fullwidth symbols are counted as Asian characters."""
        result = calculate_word_statistics("Hello！（パイソン）")  # noqa: RUF001
        assert result.non_asian_words == 1  # Hello
        assert result.asian_characters >= 7  # fullwidth symbols + katakana

    def test_whitespace_only(self) -> None:
        """Test text containing only whitespace."""
        result = calculate_word_statistics(" \t\n\r ")
        assert result == Statistics(
            words=0,
            characters_no_space=0,
            characters_with_space=3,  # space, tab, space (newlines excluded)
            non_asian_words=0,
            asian_characters=0,
        )

    def test_empty_string(self) -> None:
        """Test empty input."""
        result = calculate_word_statistics("")
        assert result == Statistics(
            words=0,
            characters_no_space=0,
            characters_with_space=0,
            non_asian_words=0,
            asian_characters=0,
        )

    def test_korean_text(self) -> None:
        """Test Korean text counting."""
        result = calculate_word_statistics("안녕하세요")
        assert result.words == 5
        assert result.asian_characters == 5
        assert result.non_asian_words == 0

    def test_chinese_traditional(self) -> None:
        """Test Traditional Chinese text."""
        result = calculate_word_statistics("繁體中文")
        assert result.words == 4
        assert result.asian_characters == 4

    def test_numbers_and_punctuation(self) -> None:
        """Test that numbers and punctuation are handled correctly."""
        result = calculate_word_statistics("Test 123, example.")
        assert result.non_asian_words == 3  # Test, 123, example.
        assert result.asian_characters == 0


class TestStatisticsDataclass:
    """Tests for the Statistics dataclass."""

    def test_frozen(self) -> None:
        """Verify Statistics is immutable."""
        stats = Statistics(
            words=1,
            characters_no_space=1,
            characters_with_space=1,
            non_asian_words=1,
            asian_characters=0,
        )
        with pytest.raises(AttributeError):
            stats.words = 2  # type: ignore[misc]

    def test_to_dict(self) -> None:
        """Test dictionary conversion."""
        stats = Statistics(
            words=10,
            characters_no_space=50,
            characters_with_space=55,
            non_asian_words=5,
            asian_characters=5,
        )
        result = stats.to_dict()
        assert result == {
            "words": 10,
            "characters_no_space": 50,
            "characters_with_space": 55,
            "non_asian_words": 5,
            "asian_characters": 5,
        }

    def test_addition(self) -> None:
        """Test Statistics addition for aggregation."""
        stats1 = Statistics(
            words=10,
            characters_no_space=50,
            characters_with_space=55,
            non_asian_words=5,
            asian_characters=5,
        )
        stats2 = Statistics(
            words=20,
            characters_no_space=100,
            characters_with_space=110,
            non_asian_words=10,
            asian_characters=10,
        )
        total = stats1 + stats2
        assert total.words == 30
        assert total.characters_no_space == 150
        assert total.characters_with_space == 165
        assert total.non_asian_words == 15
        assert total.asian_characters == 15

    def test_equality(self) -> None:
        """Test Statistics equality comparison."""
        stats1 = Statistics(
            words=10,
            characters_no_space=50,
            characters_with_space=55,
            non_asian_words=5,
            asian_characters=5,
        )
        stats2 = Statistics(
            words=10,
            characters_no_space=50,
            characters_with_space=55,
            non_asian_words=5,
            asian_characters=5,
        )
        assert stats1 == stats2

    def test_inequality(self) -> None:
        """Test Statistics inequality comparison."""
        stats1 = Statistics(
            words=10,
            characters_no_space=50,
            characters_with_space=55,
            non_asian_words=5,
            asian_characters=5,
        )
        stats2 = Statistics(
            words=20,
            characters_no_space=50,
            characters_with_space=55,
            non_asian_words=5,
            asian_characters=5,
        )
        assert stats1 != stats2


class TestCountWords:
    """Tests for count_words function."""

    def test_english(self) -> None:
        """Test counting English words."""
        assert count_words("Hello World") == 2

    def test_japanese(self) -> None:
        """Test counting Japanese text (each char = 1 word)."""
        assert count_words("こんにちは") == 5

    def test_mixed(self) -> None:
        """Test counting mixed English and Japanese."""
        assert count_words("Hello 世界") == 3  # 1 + 2

    def test_empty(self) -> None:
        """Test empty string."""
        assert count_words("") == 0


class TestCountCharacters:
    """Tests for count_characters function."""

    def test_english(self) -> None:
        """Test counting English characters (no spaces)."""
        assert count_characters("Hello World") == 10

    def test_japanese(self) -> None:
        """Test counting Japanese characters."""
        assert count_characters("こんにちは") == 5

    def test_with_spaces(self) -> None:
        """Test that spaces are excluded."""
        assert count_characters("a b c") == 3

    def test_empty(self) -> None:
        """Test empty string."""
        assert count_characters("") == 0


class TestCountCharactersWithSpace:
    """Tests for count_characters_with_space function."""

    def test_english(self) -> None:
        """Test counting English characters with spaces."""
        assert count_characters_with_space("Hello World") == 11

    def test_with_newlines(self) -> None:
        """Test that newlines are excluded."""
        assert count_characters_with_space("Hello\nWorld") == 10

    def test_tabs_included(self) -> None:
        """Test that tabs are included."""
        assert count_characters_with_space("a\tb") == 3

    def test_empty(self) -> None:
        """Test empty string."""
        assert count_characters_with_space("") == 0
