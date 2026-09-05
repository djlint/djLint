"""Rule T041: Check that the extends tag is the first tag in the template.

Django refuses a template whose `{% extends %}` comes after another tag,
and renders any text written before it, so the text leaks into the page
ahead of everything the parent produces. Jinja renders that text too, and
nunjucks drops it. A `{# #}` comment is the one thing every engine lets
stand before it, and a branch tag is left alone too: jinja documents
`{% if x %}{% extends "a" %}{% else %}{% extends "b" %}{% endif %}` as
the way to choose a parent.
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


_EXTENDS_PATTERN: Final = re.compile(
    r"{%[-+]?\s*extends\b(?:(?!%}).)*%}", re.S, cache_pattern=False
)
_BRANCH_PATTERN: Final = re.compile(
    r"{%[-+]?\s*(?:if|elif|else)\b", cache_pattern=False
)
_PIECE_PATTERN: Final = re.compile(
    r"(?P<blank>[\s\ufeff]+|{#(?:(?!#}).)*#})"
    r"|{%(?:(?!%}).)*%}"
    r"|{{(?:(?!}}).)*}}"
    r"|[^\s{]+"
    r"|{",
    re.S,
    cache_pattern=False,
)


def _ignored(
    rule: dict[str, Any], config: Config, html: str, match: re.Match[str]
) -> bool:
    return (
        overlaps_ignored_block(config, html, match)
        or inside_ignored_rule(config, html, match, rule["name"])
        or inside_ignored_linter_block(config, html, match)
    )


def _first_extends(
    rule: dict[str, Any], config: Config, html: str
) -> re.Match[str] | None:
    """Find the first `{% extends %}` that runs.

    One inside a `{% comment %}`, `{% raw %}` or `{% verbatim %}` block,
    a `{# #}` comment or a djlint:off region never runs, so the search
    goes on past it.
    """
    for match in _EXTENDS_PATTERN.finditer(html):
        if not _ignored(rule, config, html, match):
            return match
    return None


def _something_precedes(
    rule: dict[str, Any], config: Config, html: str, end: int
) -> bool:
    """Whether anything but whitespace and template comments comes first.

    A byte order mark is read as whitespace. A piece inside a block djLint
    does not lint, as a `{% load %}` written in a `{% comment %}` block,
    renders nothing and does not count. Nor does a branch tag, which
    opens nothing of its own: an `{% extends %}` chosen inside an
    `{% if %}` is still the first thing its template produces.
    """
    for piece in _PIECE_PATTERN.finditer(html, 0, end):
        if piece.group("blank") or _BRANCH_PATTERN.match(piece.group()):
            continue
        if not _ignored(rule, config, html, piece):
            return True
    return False


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that the extends tag is the first tag in the template.

    Only the first `{% extends %}` that runs is checked. A second one is
    an error of its own, and not this rule's to report.
    """
    extends = _first_extends(rule, config, html)
    if extends is None or not _something_precedes(
        rule, config, html, extends.start()
    ):
        return ()

    return (
        {
            "code": rule["name"],
            "line": get_line(extends.start(), line_ends),
            "match": extends.group().strip()[:20],
            "message": rule["message"],
        },
    )
