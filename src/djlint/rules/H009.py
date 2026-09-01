"""Rule H009: Check that tag names are lowercase."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.const import HTML_TAG_NAMES
from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that tag names are lowercase.

    The elements reported are the ones the formatter lowercases, so
    `--reformat` always clears the finding. An element it does not know,
    such as the svg `clipPath` whose case is meaningful, is left alone by
    both.
    """
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(token.start + 1, line_ends),
            "match": f"{'/' if token.closing else ''}{token.name}"[:20],
            "message": rule["message"],
        }
        for token in tokenize_markup(html)
        if token.name != token.name.lower()
        and token.name.lower() in HTML_TAG_NAMES
        and not (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        )
    )
