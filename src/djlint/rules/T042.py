"""Rule T042: Check for content outside a block in a template that extends another.

Once a template extends another, the parent decides what is output and
the child only fills the parent's blocks. Django, Jinja and Nunjucks
silently discard text and html written after `{% extends %}` and outside
every `{% block %}`, so a paragraph that looks fine in the source never
reaches the page.

A template tag there still runs, so `{% load %}`, `{% set %}` and an
`{% if %}` wrapped around a block are left alone. The body of a
`{% macro %}` or of a block form `{% set %}` is captured rather than
output, so it is left alone too, as is anything inside `{% comment %}`,
`{% raw %}` or `{% verbatim %}`. A `{% blocktrans %}` is not a
`{% block %}`: its text is output like any other and is reported.
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
_HIDDEN_REGION: Final = (
    r"{%[-+]?\s*(comment|raw|verbatim)\b(?:(?!%}).)*%}"
    r".*?{%[-+]?\s*end\1\b(?:(?!%}).)*%}"
)
_TOKEN_PATTERN: Final = re.compile(
    rf"{_HIDDEN_REGION}|{{#.*?#}}|{{%.*?%}}|{{{{.*?}}}}",
    re.S,
    cache_pattern=False,
)
_CAPTURING_OPENING_PATTERN: Final = re.compile(
    r"{%[-+]?\s*(?:block(?!trans)|macro|set(?!(?:(?!%}).)*=))\b",
    re.S,
    cache_pattern=False,
)
_CAPTURING_CLOSING_PATTERN: Final = re.compile(
    r"{%[-+]?\s*end(?:block(?!trans)|macro|set)\b", cache_pattern=False
)
_CONTENT_PATTERN: Final = re.compile(r"\S(?:.*\S)?", re.S, cache_pattern=False)


def _first_extends(config: Config, html: str) -> re.Match[str] | None:
    """The first `{% extends %}` tag that executes, or None.

    An extends tag written inside a comment or a raw block never runs,
    so it does not turn the template into a child.
    """
    return next(
        (
            match
            for match in _EXTENDS_PATTERN.finditer(html)
            if not overlaps_ignored_block(config, html, match)
            and not inside_ignored_linter_block(config, html, match)
        ),
        None,
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
    """Check for content outside a block in a template that extends another.

    The template after the extends tag is read as a stream of tags with
    text between them. A tag that captures its body, as `{% block %}`,
    `{% macro %}` or a block form `{% set %}`, is counted on a depth, and
    each run of text found at depth zero is reported once, at its start.
    A tag between two runs splits them, so each is reported on its own.
    """
    extends = _first_extends(config, html)
    if extends is None:
        return ()

    errors: list[LintError] = []
    depth = 0
    position = extends.end()

    while True:
        token = _TOKEN_PATTERN.search(html, position)
        text_end = token.start() if token else len(html)
        if depth == 0:
            content = _CONTENT_PATTERN.search(html, position, text_end)
            if content and not inside_ignored_rule(
                config, html, content, rule["name"]
            ):
                errors.append({
                    "code": rule["name"],
                    "line": get_line(content.start(), line_ends),
                    "match": content.group()[:20],
                    "message": rule["message"],
                })
        if token is None:
            break

        position = token.end()
        if _CAPTURING_OPENING_PATTERN.match(token.group()):
            depth += 1
        elif _CAPTURING_CLOSING_PATTERN.match(token.group()) and depth:
            depth -= 1

    return tuple(errors)
