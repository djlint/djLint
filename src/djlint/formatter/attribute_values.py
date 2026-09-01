"""Rewrites of attribute values that change nothing the page renders."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IX,
    inside_template_block,
    overlaps_ignored_block,
)

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_DEFAULT_TYPE_PATTERN: Final = re.compile(
    r"""
    (<(?:script|style|link)\b(?:"[^"]*"|'[^']*'|[^'">])*?)
    \s+(?<![-.:\w])type\s*=["'](?:text/css|text/javascript)["']
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)

_FORM_METHOD_PATTERN: Final = re.compile(
    r"""
    (<form\b(?:"[^"]*"|'[^']*'|\{[^}]*\}|[^'">{}/])*?
     (?<![-.:\w])method\s*=\s*["'])
    ([a-z]+)
    (["'])
    """,
    RE_FLAGS_IX,
    cache_pattern=False,
)


def format_attribute_values(html: str, config: Config) -> str:
    """Drop a redundant type, and lowercase a form method.

    Both are what the page already does: html5 assumes the type these
    elements carry, and `method` is an enumerated attribute whose value is
    matched without regard to case.

    The spans checked are the ones linting uses, which cover a verbatim
    block's contents but not its opening tag: a `<script>` is a real tag
    whose attributes can be rewritten, while the same text written inside
    a `<pre>` is content and is left alone. So is a tag written inside a
    template tag, as in `{% set s = '<form method="POST">' %}`, which
    is a string the template holds rather than an element of the page.
    """

    def is_left_alone(match: re.Match[str]) -> bool:
        return overlaps_ignored_block(
            config, html, match
        ) or inside_template_block(config, html, match)

    def drop_default_type(match: re.Match[str]) -> str:
        if is_left_alone(match):
            return match.group()
        return match.group(1)

    def lowercase_method(match: re.Match[str]) -> str:
        if is_left_alone(match):
            return match.group()
        return f"{match.group(1)}{match.group(2).lower()}{match.group(3)}"

    html = _DEFAULT_TYPE_PATTERN.sub(drop_default_type, html)
    return _FORM_METHOD_PATTERN.sub(lowercase_method, html)
