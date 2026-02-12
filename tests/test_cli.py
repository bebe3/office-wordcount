"""Integration tests for the CLI."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    """Create a sample text file for testing."""
    file = tmp_path / "sample.txt"
    file.write_text("Hello World", encoding="utf-8")
    return file


@pytest.fixture
def japanese_file(tmp_path: Path) -> Path:
    """Create a Japanese text file for testing."""
    file = tmp_path / "japanese.txt"
    file.write_text("こんにちは世界", encoding="utf-8")
    return file


@pytest.fixture
def mixed_file(tmp_path: Path) -> Path:
    """Create a mixed language text file for testing."""
    file = tmp_path / "mixed.txt"
    file.write_text("Hello 世界", encoding="utf-8")
    return file


class TestCliBasic:
    """Basic CLI functionality tests."""

    def test_version(self) -> None:
        """Test --version flag."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert "office-wordcount" in result.stdout

    def test_help(self) -> None:
        """Test --help flag."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()


class TestCliFileInput:
    """Tests for file input processing."""

    def test_single_file_json(self, sample_file: Path) -> None:
        """Test processing a single file with JSON output."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "--format",
                "json",
                str(sample_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["words"] == 2
        assert data["non_asian_words"] == 2

    def test_single_file_table(self, sample_file: Path) -> None:
        """Test processing a single file with table output."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "--format",
                "table",
                str(sample_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert "Words" in result.stdout
        assert "2" in result.stdout

    def test_japanese_file(self, japanese_file: Path) -> None:
        """Test processing Japanese text file."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "--format",
                "json",
                str(japanese_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["asian_characters"] == 7
        assert data["non_asian_words"] == 0

    def test_mixed_file(self, mixed_file: Path) -> None:
        """Test processing mixed language file."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "--format",
                "json",
                str(mixed_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["words"] == 3  # 1 English + 2 Japanese
        assert data["non_asian_words"] == 1
        assert data["asian_characters"] == 2

    def test_multiple_files(self, sample_file: Path, japanese_file: Path) -> None:
        """Test processing multiple files."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "--format",
                "json",
                str(sample_file),
                str(japanese_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "files" in data
        assert len(data["files"]) == 2
        assert "total" in data

    def test_total_only(self, sample_file: Path, japanese_file: Path) -> None:
        """Test --total flag."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "--format",
                "json",
                "--total",
                str(sample_file),
                str(japanese_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        # Should have total stats directly, not files list
        assert "words" in data
        assert "files" not in data


class TestCliStdin:
    """Tests for stdin processing."""

    def test_stdin_json(self) -> None:
        """Test reading from stdin with JSON output."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "--format", "json"],
            input="Hello World",
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["words"] == 2

    def test_stdin_mixed_text(self) -> None:
        """Test stdin with mixed Asian/non-Asian text."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "--format", "json"],
            input="Hello 世界",
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["words"] == 3  # 1 English + 2 Japanese


class TestCliSingleValue:
    """Tests for single-value output options."""

    def test_words_option(self, mixed_file: Path) -> None:
        """Test -w/--words option."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "-w", str(mixed_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "3"

    def test_chars_option(self, mixed_file: Path) -> None:
        """Test -c/--chars option."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "-c", str(mixed_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "7"

    def test_chars_with_space_option(self, mixed_file: Path) -> None:
        """Test -C/--chars-with-space option."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "-C", str(mixed_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "8"

    def test_asian_option(self, mixed_file: Path) -> None:
        """Test -a/--asian option."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "-a", str(mixed_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "2"

    def test_non_asian_option(self, mixed_file: Path) -> None:
        """Test -A/--non-asian option."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "-A", str(mixed_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "1"

    def test_stdin_with_words_option(self) -> None:
        """Test -w option with stdin."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "-w"],
            input="Hello 世界",
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "3"

    def test_multiple_files_with_words_option(
        self, sample_file: Path, japanese_file: Path
    ) -> None:
        """Test -w option with multiple files (returns total)."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "word_count.cli",
                "-w",
                str(sample_file),
                str(japanese_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "9"  # 2 (Hello World) + 7 (Japanese)


class TestCliErrors:
    """Tests for error handling."""

    def test_file_not_found(self) -> None:
        """Test error message for missing file."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", "nonexistent.txt"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 1
        assert "not found" in result.stderr.lower()

    def test_is_a_directory(self, tmp_path: Path) -> None:
        """Test error message when given a directory."""
        result = subprocess.run(
            [sys.executable, "-m", "word_count.cli", str(tmp_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 1
        assert "is a directory" in result.stderr.lower()
