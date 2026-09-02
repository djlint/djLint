"""Rule H051: Check for a role ARIA does not define.

A role no specification names is dropped outright, and the element keeps
whatever meaning it had. `role="buton"` leaves a `<div>` a `<div>`, which
reads as nothing to a screen reader while the markup looks as though it
had been given a purpose.

A value holding template syntax is unknowable and is left alone, and so is
a binding written by a framework, as in `:role` or `[attr.role]`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_ARIA_ROLE_NAMES
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

_ROLE_PATTERN = re.compile(
    r"(?<![-.:\w])role\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'>]+))",
    re.I,
    cache_pattern=False,
)
_TEMPLATE_PATTERN = re.compile(r"{[{%#]", cache_pattern=False)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for a role ARIA does not define."""
    errors: list[LintError] = []

    for token in tokenize_markup(html):
        if token.closing or token.declaration:
            continue

        match = _ROLE_PATTERN.search(html, token.name_end, token.attributes_end)
        if not match:
            continue

        value = next(group for group in match.groups() if group is not None)
        if _TEMPLATE_PATTERN.search(value):
            continue

        unknown = [
            word
            for word in value.split()
            if word.lower() not in HTML_ARIA_ROLE_NAMES
        ]
        if not unknown:
            continue

        if (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": unknown[0][:20],
            "message": rule["message"],
        })

    return tuple(errors)
