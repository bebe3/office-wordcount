"""Output formatters for CLI display.

Provides JSON and ASCII table formatting for Statistics objects.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeIs

if TYPE_CHECKING:
    from word_count.statistics import Statistics


def _is_multiple(
    stats: Statistics | Sequence[tuple[str, Statistics]],
) -> TypeIs[Sequence[tuple[str, Statistics]]]:
    """Check if stats represents multiple file results."""
    return isinstance(stats, Sequence) and not isinstance(stats, str)


def format_json(
    stats: Statistics | Sequence[tuple[str, Statistics]],
    *,
    total: Statistics | None = None,
    indent: int | None = 2,
) -> str:
    """Format statistics as JSON.

    Args:
        stats: Either a single Statistics object or a sequence of
               (filename, Statistics) tuples.
        total: Optional total Statistics for multiple files.
        indent: JSON indentation level. None for compact output.

    Returns:
        JSON-formatted string.
    """
    if _is_multiple(stats):
        result: dict[str, dict[str, int] | list[dict[str, int | str]]] = {
            "files": [{"file": name, **stat.to_dict()} for name, stat in stats]
        }
        if total is not None:
            result["total"] = total.to_dict()
        return json.dumps(result, indent=indent)
    return json.dumps(stats.to_dict(), indent=indent)


def format_table(
    stats: Statistics | Sequence[tuple[str, Statistics]],
    *,
    total: Statistics | None = None,
) -> str:
    """Format statistics as an ASCII table.

    Args:
        stats: Either a single Statistics object or a sequence of
               (filename, Statistics) tuples.
        total: Optional total Statistics for multiple files.

    Returns:
        ASCII table formatted string.
    """
    if _is_multiple(stats):
        return _format_multiple_table(stats, total=total)
    return _format_single_table(stats)


def _format_single_table(stats: Statistics) -> str:
    """Format a single Statistics object as a vertical table."""
    labels = [
        ("Words", stats.words),
        ("Characters (no space)", stats.characters_no_space),
        ("Characters (with space)", stats.characters_with_space),
        ("Non-Asian words", stats.non_asian_words),
        ("Asian characters", stats.asian_characters),
    ]

    max_label = max(len(label) for label, _ in labels)
    lines = [f"{label.ljust(max_label)} : {value}" for label, value in labels]
    return "\n".join(lines)


def _format_multiple_table(
    files: Sequence[tuple[str, Statistics]],
    *,
    total: Statistics | None = None,
) -> str:
    """Format multiple file statistics as a horizontal table."""
    headers = ["File", "Words", "Chars", "Chars+Space", "Non-Asian", "Asian"]

    rows = [
        [
            name,
            str(s.words),
            str(s.characters_no_space),
            str(s.characters_with_space),
            str(s.non_asian_words),
            str(s.asian_characters),
        ]
        for name, s in files
    ]

    if total is not None:
        rows.append(
            [
                "TOTAL",
                str(total.words),
                str(total.characters_no_space),
                str(total.characters_with_space),
                str(total.non_asian_words),
                str(total.asian_characters),
            ]
        )

    # Calculate column widths
    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]

    # Build table
    lines: list[str] = []

    # Header
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths, strict=True))
    lines.append(header_line)
    lines.append("-+-".join("-" * w for w in widths))

    # Data rows
    for row in rows:
        lines.append(
            " | ".join(cell.ljust(w) for cell, w in zip(row, widths, strict=True))
        )

    return "\n".join(lines)


def is_interactive() -> bool:
    """Check if stdout is connected to a terminal.

    Returns:
        True if running interactively, False if piped.
    """
    return sys.stdout.isatty()
