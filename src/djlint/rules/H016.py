"""Rule H016: Check that a document has a title."""

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
    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError


def _documents_without_a_title(html: str) -> list[TagToken]:
    """The opening html tag of every document holding no title.

    An svg carries a title of its own that names the graphic rather than
    the page, so one written inside it does not answer for the document.
    """
    missing: list[TagToken] = []
    open_html: TagToken | None = None
    has_title = False
    svg_depth = 0

    for token in tokenize_markup(html):
        name = token.name.lower()

        if name == "svg":
            if token.closing:
                svg_depth = max(svg_depth - 1, 0)
            elif not token.self_closing:
                svg_depth += 1
            continue

        if name == "html":
            if token.closing:
                if open_html is not None and not has_title:
                    missing.append(open_html)
                open_html, has_title = None, False
            else:
                open_html, has_title = token, False
            continue

        if name == "title" and not token.closing and not svg_depth:
            has_title = True

    return missing


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that a document has a title."""
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": rule["message"],
        }
        for token in _documents_without_a_title(html)
        if not (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        )
    )
