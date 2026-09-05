"""Rule T043: Check for a block name used more than once.

Django, Jinja and Nunjucks all refuse a template that names two blocks
the same, and they refuse it at parse time, so the page fails to load at
all. The engines do not care that the two blocks sit in different branches
of an `{% if %}`, so no branch is tracked here: a name that appears twice
anywhere in the file is an error, and each occurrence after the first is
reported at its own tag.

A block written inside a comment, a `{% raw %}` or `{% verbatim %}` body,
or a `djlint:off` region never reaches the parser, so it neither counts as
an occurrence nor is reported.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
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


_BLOCK_PATTERN: Final = re.compile(
    r"{%[-+]?\s*block(?!trans)\s+(?P<name>[\w.-]+?)(?=\s|[-+]?%})"
    r"(?:(?!%}).)*?[-+]?%}",
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
    """Check for a block name used more than once.

    Names are compared as written, since the engines treat `Content` and
    `content` as two blocks. An `{% endblock name %}` only names the block
    it closes and is not an occurrence.
    """
    errors: list[LintError] = []
    seen: set[str] = set()

    for match in _BLOCK_PATTERN.finditer(html):
        if overlaps_ignored_block(
            config, html, match
        ) or inside_ignored_linter_block(config, html, match):
            continue

        name = match.group("name")
        if name not in seen:
            seen.add(name)
            continue

        if inside_ignored_rule(config, html, match, rule["name"]):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })

    return tuple(errors)
