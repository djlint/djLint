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


SINGLE_QUOTE_MESSAGE: Final = "Single quotes should be used in tags."

_QUOTED_TAG_TEMPLATE: Final = (
    r"{%[ \t]*?(?:trans(?:late)?|with|extends|include|now)[\s]+?"
    r"(?:(?:(?!%}|QUOTE).)+?=)?QUOTE(?:(?!%}|QUOTE).)*?QUOTE(?:(?!%}).)*?%}"
)
_WRONGLY_QUOTED_TAG_PATTERNS: Final = {
    style: re.compile(
        _QUOTED_TAG_TEMPLATE.replace("QUOTE", quote), re.S, cache_pattern=False
    )
    for style, quote in (("double", "'"), ("single", '"'))
}


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for wrongly quoted strings outside HTML attributes."""
    message = (
        SINGLE_QUOTE_MESSAGE
        if config.quote_style == "single"
        else rule["message"]
    )
    errors: list[LintError] = []
    for match in _WRONGLY_QUOTED_TAG_PATTERNS[config.quote_style].finditer(
        html
    ):
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
            "message": message,
        })
    return tuple(errors)
