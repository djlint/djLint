"""Helpers for preserving significant attribute line breaks.

Covers multiline class values and whitespace-sensitive values such as
hyperscript `_` attributes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


CLASS_ATTRIBUTE_NEWLINE: Final = "\x00DJLINT_CLASS_NEWLINE\x00"
VERBATIM_ATTRIBUTE_NEWLINE: Final = "\x00DJLINT_ATTR_NEWLINE\x00"
MIN_MULTILINE_CLASS_LINES: Final = 2
_CLASS_ATTRIBUTE_PATTERN: Final = re.compile(
    r"(?<![\w:.-])class(?![\w:.-])\s*=\s*(['\"])", re.I, cache_pattern=False
)

# attribute values where line breaks are semantically significant: in
# hyperscript ("_") a newline separates commands and a "--" comment runs
# to the end of the line, so joining lines can change the program.
_VERBATIM_ATTRIBUTE_NAMES: Final = frozenset({"_"})


def encode_attribute_newlines(attributes: str, config: Config) -> str:
    """Replace significant attribute line breaks with internal markers."""
    if "\n" not in attributes:
        return attributes

    changed = False
    parts: list[str] = []
    last_end = 0

    for match in re.finditer(config.attribute_pattern, attributes, flags=re.X):
        if match.start() == match.end():
            continue

        name = match.group(1)
        value = match.group(2)
        if (
            not name
            or not value
            or "\n" not in value
            or value[0] not in {'"', "'"}
            or value[-1] != value[0]
        ):
            continue

        if name in _VERBATIM_ATTRIBUTE_NAMES:
            encoded_value = VERBATIM_ATTRIBUTE_NEWLINE.join(
                line.rstrip() for line in value[1:-1].splitlines()
            )
        elif name.lower() == "class" and config.preserve_class_newlines:
            lines = [line.strip() for line in value[1:-1].splitlines()]
            class_lines = [line for line in lines if line]
            if len(class_lines) < MIN_MULTILINE_CLASS_LINES:
                encoded_value = " ".join(class_lines)
            else:
                encoded_value = CLASS_ATTRIBUTE_NEWLINE.join(class_lines)
        else:
            continue

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
        if matches:
            indent_size = matches[-1].end()
        else:
            indent_size = max(line.rfind('"'), line.rfind("'"), 0) + 1

        out.append("\n" + (" " * indent_size))
        pos = marker_pos + len(CLASS_ATTRIBUTE_NEWLINE)
