"""Rule H048: Check for an aria attribute the specification does not define.

A misspelled aria attribute does nothing at all: no browser or screen
reader reports it, and the markup keeps the look of having been made
accessible. Only a plain `aria-` name is judged, so a binding written by a
framework, as in `:aria-label` or `[attr.aria-label]`, is left alone.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.const import HTML_ARIA_ATTRIBUTE_NAMES
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
    """Check for an aria attribute the specification does not define."""
    errors: list[LintError] = []

    for token in tokenize_markup(html):
        if token.closing or token.declaration:
            continue

        group = html[token.name_end : token.attributes_end]
        if "aria-" not in group.lower():
            continue

        ignored = None
        for match in config.attribute_pattern.finditer(group):
            name = match.group(1)
            if not name:
                continue
            lowered = name.lower()
            if not lowered.startswith("aria-"):
                continue
            if lowered in HTML_ARIA_ATTRIBUTE_NAMES:
                continue

            if ignored is None:
                ignored = (
                    overlaps_ignored_block(config, html, token)
                    or inside_ignored_rule(config, html, token, rule["name"])
                    or inside_ignored_linter_block(config, html, token)
                )
            if ignored:
                break

            errors.append({
                "code": rule["name"],
                "line": get_line(token.name_end + match.start(1), line_ends),
                "match": name[:20],
                "message": rule["message"],
            })

    return tuple(errors)
