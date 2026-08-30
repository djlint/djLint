"""Rule H044: Check that a thead does not mix th and td cells."""

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
    """Yield the cells of a thead written unlike the first one in it.

    The first cell sets what the head is made of, so a report points at
    the odd one rather than at the whole head.
    """
    depth = 0
    first_cell = ""
    for token in tokenize_markup(html):
        name = token.name.lower()
        if name == "thead":
            if token.closing:
                depth = max(depth - 1, 0)
            else:
                depth += 1
                first_cell = ""
            continue

        if not depth or token.closing or name not in _CELL_TAGS:
            continue

        if not first_cell:
            first_cell = name
        elif name != first_cell:
            yield token


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that a thead does not mix th and td cells."""
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
