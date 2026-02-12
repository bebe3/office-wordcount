"""Tests for output formatters."""

import json

import pytest

from word_count.formatter import format_json, format_table
from word_count.statistics import Statistics


@pytest.fixture
def sample_stats() -> Statistics:
    """Create sample Statistics for testing."""
    return Statistics(
        words=100,
        characters_no_space=500,
        characters_with_space=550,
        non_asian_words=50,
        asian_characters=50,
    )


class TestFormatJson:
    """Tests for JSON formatting."""

    def test_single_stats(self, sample_stats: Statistics) -> None:
        """Test JSON output for single Statistics."""
        result = format_json(sample_stats)
        data = json.loads(result)
        assert data["words"] == 100
        assert data["characters_no_space"] == 500

    def test_multiple_files(self, sample_stats: Statistics) -> None:
        """Test JSON output for multiple files."""
        files = [("file1.txt", sample_stats), ("file2.txt", sample_stats)]
        result = format_json(files, total=sample_stats + sample_stats)
        data = json.loads(result)
        assert len(data["files"]) == 2
        assert data["total"]["words"] == 200

    def test_compact_output(self, sample_stats: Statistics) -> None:
        """Test compact JSON without indentation."""
        result = format_json(sample_stats, indent=None)
        assert "\n" not in result

    def test_multiple_files_without_total(self, sample_stats: Statistics) -> None:
        """Test JSON output for multiple files without total."""
        files = [("file1.txt", sample_stats), ("file2.txt", sample_stats)]
        result = format_json(files)
        data = json.loads(result)
        assert len(data["files"]) == 2
        assert "total" not in data


class TestFormatTable:
    """Tests for table formatting."""

    def test_single_stats_vertical(self, sample_stats: Statistics) -> None:
        """Test vertical table for single Statistics."""
        result = format_table(sample_stats)
        assert "Words" in result
        assert "100" in result
        assert "Characters (no space)" in result
        assert "500" in result

    def test_multiple_files_horizontal(self, sample_stats: Statistics) -> None:
        """Test horizontal table for multiple files."""
        files = [("file1.txt", sample_stats), ("file2.txt", sample_stats)]
        result = format_table(files, total=sample_stats + sample_stats)
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "TOTAL" in result
        assert "200" in result  # Total words

    def test_table_header_columns(self, sample_stats: Statistics) -> None:
        """Test that table has correct header columns."""
        files = [("test.txt", sample_stats)]
        result = format_table(files)
        assert "File" in result
        assert "Words" in result
        assert "Chars" in result
        assert "Non-Asian" in result
        assert "Asian" in result

    def test_single_vertical_format(self, sample_stats: Statistics) -> None:
        """Test that single stats uses vertical format with colon separator."""
        result = format_table(sample_stats)
        assert " : " in result  # Vertical format uses colon separator
