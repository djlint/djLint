"""Rule H044: Check that a header row does not mix th and td cells."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Iterator

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError

_CELL_TAGS = frozenset(("th", "td"))


def _odd_cells(html: str) -> Iterator[TagToken]:
    """Yield the cells of a header row written unlike the rest of that row.

    A row is judged on its own, so the explanation row of `td` that the
    html specification puts in a `thead` beside the row of headers is not
    a mixture. An empty `td` opening the row is the corner cell of a table
    with headers down its first column, which is the markup the W3C
    accessibility tutorial asks for, so it sets nothing and is skipped.
    """
    depth = 0
    row_cell = ""
    open_cell: TagToken | None = None
    for token in tokenize_markup(html):
        name = token.name.lower()

        if name == "thead":
            depth = max(depth - 1, 0) if token.closing else depth + 1
            row_cell = ""
            continue

        if not depth:
            continue

        if name == "tr":
            row_cell = ""
            continue

        if name not in _CELL_TAGS:
            continue

        if token.closing:
            if (
                open_cell is not None
                and open_cell.name.lower() == "td"
                and not row_cell
                and not html[open_cell.end : token.start].strip()
            ):
                open_cell = None
                continue
            if open_cell is not None:
                if not row_cell:
                    row_cell = open_cell.name.lower()
                elif open_cell.name.lower() != row_cell:
                    yield open_cell
                open_cell = None
            continue

        open_cell = token


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that a header row does not mix th and td cells."""
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": rule["message"],
        }
        for token in _odd_cells(html)
        if not (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        )
    )
