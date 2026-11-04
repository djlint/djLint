"""Helpers for preserving significant attribute line breaks.

An attribute value reaches the page as it stands, so joining its lines
changes the document: a `title` tooltip loses a line, hyperscript (`_`)
loses a command separator, and a `data-` value read by script comes back
different. Only values holding a token list or css are joined; every other
value keeps its breaks behind an internal marker until formatting is done.

A string written across lines inside a template tag is held the same way:
the whitespace after its line breaks is part of its value.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import COLLAPSIBLE_WHITESPACE, TEMPLATE_TAG_WHOLE
from djlint.helpers import compile_pattern, mask_raw_text_bodies

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_COLLAPSIBLE_RUN_PATTERN: Final = compile_pattern(f"[{re.escape(COLLAPSIBLE_WHITESPACE)}]+")
_LINE_BREAK_RUN_PATTERN: Final = compile_pattern(
    rf"[{re.escape(COLLAPSIBLE_WHITESPACE)}]*\n"
    rf"[{re.escape(COLLAPSIBLE_WHITESPACE)}]*"
)

_TEMPLATE_TAG_WHOLE_PATTERN: Final = compile_pattern(TEMPLATE_TAG_WHOLE, re.S)


def _sub_outside_template_tags(pattern: re.Pattern[str], replacement: str, value: str) -> str:
    """Rewrite a value's own text, leaving each template tag in it as written.

    A template tag in a value is code, and its strings mean what they say:
    collapsing the spaces of `class="x {{ "a  b" }}"` changed the string.
    Its line breaks are held behind the marker, as the value's would be, so
    that flattening the tag's attributes does not join them either.
    """
    if "{" not in value:
        return pattern.sub(replacement, value)
    parts: list[str] = []
    last_end = 0
    for tag in _TEMPLATE_TAG_WHOLE_PATTERN.finditer(value):
        parts.extend((
            pattern.sub(replacement, value[last_end : tag.start()]),
            tag.group().replace("\n", VERBATIM_ATTRIBUTE_NEWLINE),
        ))
        last_end = tag.end()
    parts.append(pattern.sub(replacement, value[last_end:]))
    return "".join(parts)


def _hold_line_breaks(tag: re.Match[str]) -> str:
    return tag.group().replace("\n", VERBATIM_ATTRIBUTE_NEWLINE)


def split_outside_template_tags(value: str, separator: str) -> list[str]:
    """Split a value at a separator written outside its template tags."""
    if "{" not in value:
        return value.split(separator)
    masked = _TEMPLATE_TAG_WHOLE_PATTERN.sub(lambda tag: "_" * len(tag.group()), value)
    parts: list[str] = []
    start = 0
    position = masked.find(separator)
    while position >= 0:
        parts.append(value[start:position])
        start = position + len(separator)
        position = masked.find(separator, start)
    parts.append(value[start:])
    return parts


CLASS_ATTRIBUTE_NEWLINE: Final = "\x00DJLINT_CLASS_NEWLINE\x00"
VERBATIM_ATTRIBUTE_NEWLINE: Final = "\x00DJLINT_ATTR_NEWLINE\x00"
MIN_MULTILINE_CLASS_LINES: Final = 2
_CLASS_ATTRIBUTE_PATTERN: Final = compile_pattern(
    r"(?<![\w:.-])class(?![\w:.-])\s*=\s*(['\"])", re.I
)

_JOINABLE_ATTRIBUTE_NAMES: Final = frozenset({"class", "data-srcset", "sizes", "srcset", "style"})
_TRIMMED_ATTRIBUTE_NAMES: Final = frozenset({"class", "style"})

TEMPLATE_STRING_NEWLINE: Final = "\x00DJLINT_STRING_NEWLINE\x00"
# A tag runs to its first closer outside a string, so `{% trans "a %}" %}` and
# `{% set s = "{%" %}` are each one tag, and an unclosed one ends at the next
# opener outside a string. An escape outside a string is skipped as one, or
# each quote of `\"\"\"` would start a string read to the end. Read from each
# opener, the quotes after it pair up the same way, so a read only runs past
# the next opener inside a string, which ends at the next quote of its kind:
# the reads from successive openers overlap by about a string, and the scan
# stays linear however many quotes are left open. A comment is read whole
# first, so a quote in it pairs with nothing after it; one left open, or a
# comment block never ended, is read only to the next opener of its kind.
_TEMPLATE_TAG_PATTERN: Final = compile_pattern(
    r"""
    (?P<comment>
        \{\#(?:(?!\#\}|\{\#).)*+\#\}
      | \{%[-+]?[ \t]*comment\b(?:(?!%\}|\{%).)*+%\}
        (?:(?!\{%[-+]?[ \t]*(?:end)?comment\b).)*+
        \{%[-+]?[ \t]*endcomment[ \t]*[-+]?%\}
    )
  | \{\{(?:\\.|"(?:\\.|[^"\\])*+"|'(?:\\.|[^'\\])*+'|(?!\}\}|\{\{).)*+\}\}
  | \{%(?:\\.|"(?:\\.|[^"\\])*+"|'(?:\\.|[^'\\])*+'|(?!%\}|\{%).)*+%\}
    """,
    re.S | re.X,
)
# Braces balance inside a mako expression, as in `${f({"a": 1})}`, outside
# its strings. One left open ends at the next `${`, read the same way as an
# unclosed tag above.
_MAKO_EXPRESSION_PATTERN: Final = compile_pattern(
    r"""
    \$(?P<braces>\{
        (?:\\.|"(?:\\.|[^"\\])*+"|'(?:\\.|[^'\\])*+'|(?&braces)|(?!\$\{)[^{}"'\\])*+
    \})
    """,
    re.S | re.X,
)
# Read inside one tag as the tag was read: an escape outside a string is
# skipped as one, and only a string (group 1) is encoded.
_TEMPLATE_STRING_PATTERN: Final = compile_pattern(
    r"""\\.|("(?:\\.|[^"\\])*+"|'(?:\\.|[^'\\])*+')""", re.S
)


def encode_attribute_newlines(attributes: str, config: Config) -> str:
    """Replace significant attribute line breaks with internal markers.

    A `class` value is normalized here too: it is a list of tokens, so the
    whitespace between them and at its edges says nothing.
    """
    if "\n" not in attributes and not _CLASS_ATTRIBUTE_PATTERN.search(attributes):
        return attributes

    changed = False
    parts: list[str] = []
    last_end = 0

    for match in config.attribute_pattern.finditer(attributes):
        if match.start() == match.end():
            continue

        name = match.group(1)
        value = match.group(2)
        lowered = name.lower() if name else ""
        if (
            not name
            or not value
            or value[0] not in {'"', "'"}
            or value[-1] != value[0]
            or ("\n" not in value and lowered != "class")
        ):
            continue

        laid_out_by_js_json_formatter = bool(
            config.format_attribute_js_json and config.format_attribute_js_json_pattern.match(name)
        )

        if lowered == "class" and config.preserve_class_newlines:
            lines = [line.strip() for line in value[1:-1].splitlines()]
            class_lines = [line for line in lines if line]
            if len(class_lines) < MIN_MULTILINE_CLASS_LINES:
                encoded_value = " ".join(class_lines)
            else:
                encoded_value = CLASS_ATTRIBUTE_NEWLINE.join(class_lines)
        elif laid_out_by_js_json_formatter:
            continue
        elif lowered == "class":
            encoded_value = _sub_outside_template_tags(
                _COLLAPSIBLE_RUN_PATTERN, " ", value[1:-1]
            ).strip(COLLAPSIBLE_WHITESPACE)
        elif lowered in _TRIMMED_ATTRIBUTE_NAMES:
            encoded_value = _sub_outside_template_tags(
                _LINE_BREAK_RUN_PATTERN, " ", value[1:-1]
            ).strip(COLLAPSIBLE_WHITESPACE)
        elif lowered in _JOINABLE_ATTRIBUTE_NAMES:
            # Its own line breaks are layout, but not those in a template
            # string, as in srcset="{{ f("a
            #   b") }} 2x".
            encoded_value = _TEMPLATE_TAG_WHOLE_PATTERN.sub(_hold_line_breaks, value[1:-1])
            if encoded_value == value[1:-1]:
                continue
        else:
            encoded_value = VERBATIM_ATTRIBUTE_NEWLINE.join(value[1:-1].split("\n"))

        parts.extend((
            attributes[last_end : match.start()],
            f"{name}={value[0]}{encoded_value}{value[0]}",
        ))
        last_end = match.end()
        changed = True

    if not changed:
        return attributes

    parts.append(attributes[last_end:])
    return "".join(parts)


def _encode_string_newlines(match: re.Match[str]) -> str:
    if match.group(1) is None:
        return match.group()
    return match.group().replace("\n", TEMPLATE_STRING_NEWLINE)


def multiline_template_tag_spans(html: str) -> list[tuple[int, int]]:
    """Where each template tag written across lines starts and ends.

    Read as strings across lines are found, so a closer in a string does
    not end the tag, and comments and raw text bodies are left out. A mako
    `${...}` expression counts too, up to the brace that balances its own.
    """
    if "\n" not in html or ("{{" not in html and "{%" not in html and "${" not in html):
        return []
    scanned = mask_raw_text_bodies(html)
    spans = [
        tag.span()
        for tag in _TEMPLATE_TAG_PATTERN.finditer(scanned)
        if tag.group("comment") is None and "\n" in tag.group()
    ]
    if "${" in scanned:
        spans.extend(
            expression.span()
            for expression in _MAKO_EXPRESSION_PATTERN.finditer(scanned)
            if "\n" in expression.group()
        )
    return spans


def encode_template_string_newlines(html: str) -> str:
    """Hold the line breaks of a string inside a template tag behind a marker.

    The whitespace after such a break is part of the string, but every pass
    that lays out lines would strip or indent it as layout. Behind the
    marker the string stays on one line until indenting is done. A raw text
    body is javascript or css rather than template and is left alone. Most
    attribute values already hold their breaks behind their own marker; one
    whose lines are joined or laid out anyway (`class`, `style`, `srcset`, a
    value formatted as javascript) still has its template strings held.
    """
    if "\n" not in html or ("{{" not in html and "{%" not in html):
        return html

    parts: list[str] = []
    last_end = 0
    for tag in _TEMPLATE_TAG_PATTERN.finditer(mask_raw_text_bodies(html)):
        if (
            tag.group("comment") is not None
            or "\n" not in tag.group()
            or ('"' not in tag.group() and "'" not in tag.group())
        ):
            continue
        start, end = tag.span()
        parts.extend((
            html[last_end:start],
            _TEMPLATE_STRING_PATTERN.sub(_encode_string_newlines, html[start:end]),
        ))
        last_end = end

    if not parts:
        return html

    parts.append(html[last_end:])
    return "".join(parts)


def restore_template_string_newlines(html: str) -> str:
    """Restore the line breaks held inside template tag strings."""
    if TEMPLATE_STRING_NEWLINE not in html:
        return html

    return html.replace(TEMPLATE_STRING_NEWLINE, "\n")


def restore_verbatim_attribute_newlines(html: str) -> str:
    """Restore preserved verbatim attribute line breaks."""
    if VERBATIM_ATTRIBUTE_NEWLINE not in html:
        return html

    return html.replace(VERBATIM_ATTRIBUTE_NEWLINE, "\n")


def decode_class_attribute_newlines(value: str, join_space: str) -> str:
    """Restore preserved class attribute line breaks."""
    if CLASS_ATTRIBUTE_NEWLINE not in value:
        return value

    return join_space.join(value.split(CLASS_ATTRIBUTE_NEWLINE))


def restore_class_attribute_newlines(html: str) -> str:
    """Restore any preserved class line breaks that skipped attr formatting."""
    if CLASS_ATTRIBUTE_NEWLINE not in html:
        return html

    out: list[str] = []
    pos = 0

    while True:
        marker_pos = html.find(CLASS_ATTRIBUTE_NEWLINE, pos)
        if marker_pos == -1:
            out.append(html[pos:])
            return "".join(out)

        out.append(html[pos:marker_pos])

        line_start = html.rfind("\n", 0, marker_pos) + 1
        line = html[line_start:marker_pos]
        matches = tuple(_CLASS_ATTRIBUTE_PATTERN.finditer(line))
        indent_size = matches[-1].end() if matches else max(line.rfind('"'), line.rfind("'"), 0) + 1

        out.append("\n" + (" " * indent_size))
        pos = marker_pos + len(CLASS_ATTRIBUTE_NEWLINE)
