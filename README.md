# office-wordcount

A word counting tool that handles mixed Asian and non-Asian text, counting words the same way Microsoft Office does.

[![CI](https://github.com/bebe3/office-wordcount/actions/workflows/ci.yml/badge.svg)](https://github.com/bebe3/office-wordcount/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/office-wordcount.svg)](https://badge.fury.io/py/office-wordcount)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Office-compatible word counting**: Counts words like Microsoft Office
  - Non-Asian text: Counts whitespace-separated tokens
  - Asian text (CJK): Counts each character as one word
- **Multiple output formats**: JSON (for scripting) and ASCII table (for humans)
- **Pipe-friendly**: Automatically uses JSON when piped, table when interactive
- **Type-safe**: Full type hints and PEP 561 compliance

## Installation

```bash
pip install office-wordcount
```

Or with uv:

```bash
uv add office-wordcount
```

## Usage

### Command Line

```bash
# Count words in a file (full statistics)
office-wordcount document.txt

# Read from stdin
cat document.txt | office-wordcount

# Get single values (useful for scripting)
office-wordcount -w document.txt    # words only
office-wordcount -c document.txt    # characters (no spaces)
office-wordcount -C document.txt    # characters (with spaces)
office-wordcount -a document.txt    # Asian characters only
office-wordcount -A document.txt    # non-Asian words only

# Process multiple files
office-wordcount *.txt

# Force JSON output
office-wordcount --format json document.txt

# Show only total for multiple files
office-wordcount --total *.txt
```

### CLI Options

| Option | Long | Description |
|--------|------|-------------|
| `-w` | `--words` | Output only the word count |
| `-c` | `--chars` | Output only the character count (no spaces) |
| `-C` | `--chars-with-space` | Output only the character count (with spaces) |
| `-a` | `--asian` | Output only the Asian character count |
| `-A` | `--non-asian` | Output only the non-Asian word count |
| `-f` | `--format` | Output format: `json`, `table`, or `auto` |
| `-t` | `--total` | Show only the total (for multiple files) |

### Output Examples

**Table format (default for terminal):**

```
Words                  : 150
Characters (no space)  : 750
Characters (with space): 800
Non-Asian words        : 100
Asian characters       : 50
```

**JSON format (default for pipes):**

```json
{
  "words": 150,
  "characters_no_space": 750,
  "characters_with_space": 800,
  "non_asian_words": 100,
  "asian_characters": 50
}
```

**Single value (with -w, -c, etc.):**

```bash
$ office-wordcount -w document.txt
150
```

### Python API

```python
# Simple functions for single values
from word_count import count_words, count_characters

words = count_words("Hello 世界")        # 3
chars = count_characters("Hello 世界")   # 7

# Full statistics
from word_count import calculate_word_statistics

stats = calculate_word_statistics("Hello 世界")
print(stats.words)            # 3 (1 English word + 2 Chinese characters)
print(stats.non_asian_words)  # 1
print(stats.asian_characters) # 2

# Convert to dictionary
print(stats.to_dict())
```

### Available Functions

| Function | Description |
|----------|-------------|
| `count_words(text)` | Count total words |
| `count_characters(text)` | Count characters (no spaces) |
| `count_characters_with_space(text)` | Count characters (with spaces) |
| `calculate_word_statistics(text)` | Get all statistics as `Statistics` object |

## Why This Tool?

When counting words in documents with mixed languages (like English and Japanese), different tools give different results:

| Tool | "Hello 世界" | Notes |
|------|-------------|-------|
| `wc -w` | 2 | Splits only by whitespace |
| Microsoft Word | 3 | Counts Asian chars individually |
| **office-wordcount** | 3 | Matches Office behavior |

This tool is designed to match Microsoft Office's word counting, which is the standard in many professional contexts.

## Validation

See [validation_dataset.md](validation_dataset.md) for test cases used to verify Microsoft Word compatibility. The dataset includes:

- Basic tests (English, Japanese, Korean, Chinese)
- Mixed language tests
- Special characters (fullwidth, circled numbers, era names)
- CJK radicals and extensions
- Punctuation handling
- Emoji tests

## Development

```bash
# Clone the repository
git clone https://github.com/bebe3/office-wordcount.git
cd office-wordcount

# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linter
uv run ruff check src tests

# Run type checker
uv run mypy src

# Format code
uv run ruff format src tests
```

## License

MIT License - see [LICENSE](LICENSE) for details.
