"""Rule T002: Check quote style in Django template tags."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_html_attribute,
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_SINGLE_QUOTED_TAG_PATTERN: Final = re.compile(
    r"{%[ \t]*?(?:trans(?:late)?|with|extends|include|now)[\s]+?"
    r"(?:(?:(?!%}|').)+?=)?'(?:(?!%}|').)*?'(?:(?!%}).)*?%}",
    re.S,
    cache_pattern=False,
)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for single-quoted strings outside HTML attributes."""
    errors: list[LintError] = []
    for match in _SINGLE_QUOTED_TAG_PATTERN.finditer(html):
        if (
            inside_html_attribute(html, match)
            or overlaps_ignored_block(config, html, match)
            or inside_ignored_rule(config, html, match, rule["name"])
            or inside_ignored_linter_block(config, html, match)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })
    return tuple(errors)
