"""Rewrites of attribute values that change nothing the page renders."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint._const import QUOTED_ATTRIBUTE_VALUE, TAG_START, TEMPLATE_TAG_WHOLE
from djlint._helpers import (
    RE_FLAGS_ISX,
    RE_FLAGS_IX,
    compile_pattern,
    inside_template_block,
    overlaps_ignored_block,
)

if TYPE_CHECKING:
    from typing import Final

    import regex as re

    from djlint._settings import Config


# Both read a value as compressing will write it, which runs later: quoted or
# not, and spaced from its "=" or not. Matching only the quoted form left an
# unquoted one for the next run. An unquoted value ends where compressing ends
# it, so `type=text/css{{ x }}` is one value of its own. A template tag or
# comment is read whole, even across lines, so what is written inside one, as
# in `{# rel=stylesheet #}`, is not taken for markup, and so is one in a
# quoted value, where a quote or ">" of its own, as in `"{{ "a > b" }}"`, does
# not end the value. Another tag's start ends a tag that was never closed.
_ATTRIBUTES: Final = (
    rf"""(?:{QUOTED_ATTRIBUTE_VALUE}|{TEMPLATE_TAG_WHOLE}|(?!\{{[{{%\#]|{TAG_START})[^'">])*?"""
)
# A bare value as compressing reads it, template tags and all: the one in
# `src={{ url }}` is part of the value, and compressing quotes it.
_BARE_VALUE: Final = (
    r"""(?:[^\s"'=<>/{}]|/(?!>)|\{\{(?:(?!\}\}|\{\{).)*+\}\}|\{%(?:(?!%\}|\{%).)*+%\})++"""
)
# What follows a value in a tag, read one whole piece at a time and never
# back: a value with its "=", a comment, a name, or any other character. It
# stops only at a template tag of its own, which may write any attribute, at
# another `type=`, or at the end of the tag.
_REST_OF_TAG: Final = rf"""
    (?:=\s*(?:{QUOTED_ATTRIBUTE_VALUE}|{_BARE_VALUE})
      |\{{\#(?:(?!\#\}}|\{{\#).)*+\#\}}
      |(?!type\s*=)[-.:@\w]+
      |(?!\{{[{{%]|type\s*=)[^<>]
    )*+
"""
# A template tag written with jinja's "-" marker strips the whitespace on that
# side, which would glue a neighbour onto the value or onto the tag name.
_TRIMS_BEFORE: Final = r"\s*\{[{%\#]-"
_TRIMMED_AFTER: Final = r"-[}%\#]\}\s*"
# The type written out is the default only on the element it is the default
# for: `text/css` on a `<script>` is not javascript, and on a `<link>` it is
# only implied for a stylesheet. A rel a template tag helps write may render
# as anything, and so may one after a template tag outside a value: it can
# write a rel of its own, which a browser reads first, or leave this one out.
_STYLESHEET_REL: Final = rf"""
    (?=(?:{QUOTED_ATTRIBUTE_VALUE}|\{{\#(?:(?!\#\}}).)*\#\}}|(?!\{{[{{%\#]|{TAG_START})[^'">])*?\srel\s*=\s*
        (?:"[^"{{]*?(?<![^\s"])stylesheet(?![^\s"])[^"{{]*"
          |'[^'{{]*?(?<![^\s'])stylesheet(?![^\s'])[^'{{]*'
          |stylesheet(?=\s|/?>)))
"""
# An attribute of its own starts after whitespace that renders, or after a
# statement tag written there, as in `{% if a %}method="post"`. Anything else
# makes it part of a longer name, as `@method` or `data-{% endif %}method`.
_ATTRIBUTE_START: Final = rf"""
    (?:(?<=\s)|(?<=\s\{{%[^{{}}]*[^-{{}}]%\}}))(?<!{_TRIMMED_AFTER})
"""


# Of two types a browser reads the first, so one written later in the tag
# would take over once the default was dropped. So could one that a template
# tag after it writes, as `{{ attrs }}` may; a comment writes nothing. A later
# type that is the same default takes over as nothing new, and is dropped in
# turn, so a run drops both rather than one now and one the next time.
def _default_type(element: str, value: str, condition: str = "") -> str:
    return rf"""
    (<{element}(?![-.:\w]){condition}{_ATTRIBUTES})
    \s+(?<![-.:\w])(?<!{_TRIMMED_AFTER})type\s*=\s*
    (?:(["']){value}\2|{value}(?=\s|/?>))
    (?!{_TRIMS_BEFORE})
    (?!{_REST_OF_TAG}
        (?:\{{[{{%]|type\s*=\s*(?!"{value}"|'{value}'|{value}(?=\s|/?>))))
    """


_DEFAULT_TYPE_PATTERN: Final = compile_pattern(
    rf"""(?|
    {_default_type("script", "text/javascript")}
    |{_default_type("style", "text/css")}
    |{_default_type("link", "text/css", _STYLESHEET_REL)}
    )""",
    RE_FLAGS_ISX,
)

_FORM_METHOD_PATTERN: Final = compile_pattern(
    rf"""
    (<form(?![-.:\w])(?>{QUOTED_ATTRIBUTE_VALUE}|{TEMPLATE_TAG_WHOLE}|\{{(?:(?!{TAG_START})[^}}])*+\}}|(?!{TAG_START})[^'">{{}}])*?
     {_ATTRIBUTE_START}method\s*=\s*(["'])?)
    ([a-z]+)
    ((?(2)\2|(?=\s|/?>)))
    (?!{_TRIMS_BEFORE})
    """,
    RE_FLAGS_IX,
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
        return overlaps_ignored_block(config, html, match) or inside_template_block(
            config, html, match
        )

    dropped = 0

    def drop_default_type(match: re.Match[str]) -> str:
        nonlocal dropped
        if is_left_alone(match):
            return match.group()
        dropped += 1
        return match.group(1)

    def lowercase_method(match: re.Match[str]) -> str:
        if is_left_alone(match):
            return match.group()
        return f"{match.group(1)}{match.group(3).lower()}{match.group(4)}"

    # A match runs from the tag's start, so a second default type in the
    # same tag, dropped once the first has gone, is found on the next scan.
    while True:
        dropped = 0
        html = _DEFAULT_TYPE_PATTERN.sub(drop_default_type, html)
        if not dropped:
            break
    return _FORM_METHOD_PATTERN.sub(lowercase_method, html)
