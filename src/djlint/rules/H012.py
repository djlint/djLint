"""Rule H012: Check for spaces around an attribute's equals sign.

The check runs over one tag's attribute area at a time rather than over
the whole document. A pattern anchored at `<` has to walk forward looking
for the `=`, and where a document holds many `<` and no `>` that walk
reaches the end of the file from every one of them, which is quadratic.
A tag's attribute area is bounded, so scanning it is linear.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError

# A quoted value or a template tag is stepped over whole, so an "=" with a
# space beside it inside one is the author's text rather than an attribute.
_SPACED_EQUALS_PATTERN: Final = re.compile(
    r"""
      "[^"]*"
    | '[^']*'
    | {{[^}]*}}
    | {%[^%]*%}
    | {\#[^\#]*\#}
    | {[^}]*}
    | (?P<before>\s+=)
    | (?P<after>=\s)
    """,
    re.S | re.X,
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
    """Check for spaces around an attribute's equals sign."""
    errors: list[LintError] = []

    for token in tokenize_markup(html):
        if token.closing or token.declaration:
            continue

        attributes = html[token.name_end : token.attributes_end]
        # One finding per side, as the two patterns this replaced gave, so
        # a tag spaced on both sides is reported the way it always was.
        ends = {
            match.end()
            for match in _SPACED_EQUALS_PATTERN.finditer(attributes)
            for side in ("before", "after")
            if match.group(side)
        }
        if not ends:
            continue

        if (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            continue

        errors.extend(
            {
                "code": rule["name"],
                "line": get_line(token.start, line_ends),
                "match": html[token.start : token.name_end + end].strip()[:20],
                "message": rule["message"],
            }
            for end in sorted(ends)
        )

    return tuple(errors)
