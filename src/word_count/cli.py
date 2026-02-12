"""Command-line interface for office-wordcount.

Provides word counting with support for mixed Asian/non-Asian text,
reading from files or stdin, with JSON or table output.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from word_count import __version__, calculate_word_statistics
from word_count.formatter import format_json, format_table, is_interactive
from word_count.statistics import Statistics


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="office-wordcount",
        description="Count words in text files, handling mixed Asian and non-Asian text.",
        epilog=(
            "Examples:\n"
            "  office-wordcount file.txt\n"
            "  cat file.txt | office-wordcount\n"
            "  office-wordcount -w file.txt        # words only\n"
            "  office-wordcount -c file.txt        # characters only\n"
            "  office-wordcount --format json *.txt"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Input files to process. If omitted, reads from stdin.",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "table", "auto"],
        default="auto",
        help=(
            "Output format. 'auto' uses table for terminal, "
            "JSON for pipes. (default: auto)"
        ),
    )

    parser.add_argument(
        "-t",
        "--total",
        action="store_true",
        help="Show only the total (for multiple files).",
    )

    # Single value options (mutually exclusive)
    value_group = parser.add_mutually_exclusive_group()
    value_group.add_argument(
        "-w",
        "--words",
        action="store_true",
        help="Output only the word count.",
    )
    value_group.add_argument(
        "-c",
        "--chars",
        action="store_true",
        help="Output only the character count (no spaces).",
    )
    value_group.add_argument(
        "-C",
        "--chars-with-space",
        action="store_true",
        help="Output only the character count (with spaces).",
    )
    value_group.add_argument(
        "-a",
        "--asian",
        action="store_true",
        help="Output only the Asian character count.",
    )
    value_group.add_argument(
        "-A",
        "--non-asian",
        action="store_true",
        help="Output only the non-Asian word count.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def read_stdin() -> str:
    """Read all text from stdin.

    Returns:
        Complete text content from stdin.
    """
    return sys.stdin.read()


def read_file(path: Path) -> str:
    """Read text content from a file.

    Args:
        path: Path to the file to read.

    Returns:
        File contents as string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
        UnicodeDecodeError: If the file is not valid UTF-8.
    """
    return path.read_text(encoding="utf-8")


def process_files(
    paths: Sequence[Path],
) -> tuple[list[tuple[str, Statistics]], Statistics]:
    """Process multiple files and calculate statistics.

    Args:
        paths: Sequence of file paths to process.

    Returns:
        Tuple of (list of (filename, stats) pairs, total stats).
    """
    results: list[tuple[str, Statistics]] = []
    total = Statistics(
        words=0,
        characters_no_space=0,
        characters_with_space=0,
        non_asian_words=0,
        asian_characters=0,
    )

    for path in paths:
        text = read_file(path)
        stats = calculate_word_statistics(text)
        results.append((str(path), stats))
        total = total + stats

    return results, total


def get_single_value(stats: Statistics, args: argparse.Namespace) -> int | None:
    """Extract a single value from stats based on args.

    Args:
        stats: Statistics object.
        args: Parsed arguments.

    Returns:
        The requested value, or None if no single-value option was specified.
    """
    if args.words:
        return stats.words
    if args.chars:
        return stats.characters_no_space
    if args.chars_with_space:
        return stats.characters_with_space
    if args.non_asian:
        return stats.non_asian_words
    if args.asian:
        return stats.asian_characters
    return None


def _render_output(
    output_format: str,
    stats: Statistics | Sequence[tuple[str, Statistics]],
    *,
    total: Statistics | None = None,
) -> None:
    """Render statistics to stdout in the specified format."""
    if output_format == "json":
        print(format_json(stats, total=total))
    else:
        print(format_table(stats, total=total))


def run(args: argparse.Namespace) -> int:
    """Execute the CLI with parsed arguments.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    output_format = args.format
    if output_format == "auto":
        output_format = "table" if is_interactive() else "json"

    try:
        # 1. Normalize input
        if args.files:
            paths = [Path(f) for f in args.files]
            results, total = process_files(paths)
        else:
            text = read_stdin()
            stats = calculate_word_statistics(text)
            results, total = [("stdin", stats)], stats

        # 2. Determine target stats
        target_stats = total if (args.total or len(results) > 1) else results[0][1]

        # 3. Single value output (early return)
        single_value = get_single_value(target_stats, args)
        if single_value is not None:
            print(single_value)
            return 0

        # 4. Structured output
        if args.total or len(results) == 1:
            _render_output(output_format, target_stats)
        else:
            _render_output(output_format, results, total=total)

    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}", file=sys.stderr)
        return 1
    except IsADirectoryError as e:
        print(f"Error: Is a directory: {e.filename}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Error: Permission denied: {e.filename}", file=sys.stderr)
        return 1
    except UnicodeDecodeError as e:
        print(f"Error: File is not valid UTF-8 text: {e.reason}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    except BrokenPipeError:
        sys.stderr.close()
        return 0

    return 0


def main() -> None:
    """Entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    sys.exit(run(args))


if __name__ == "__main__":
    main()
