"""Helpers for preserving significant attribute line breaks.

An attribute value reaches the page as it stands, so joining its lines
changes the document: a `title` tooltip loses a line, hyperscript (`_`)
loses a command separator, and a `data-` value read by script comes back
different. Only values holding a token list or css are joined; every other
value keeps its breaks behind an internal marker until formatting is done.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import COLLAPSIBLE_WHITESPACE

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_COLLAPSIBLE_RUN_PATTERN: Final = re.compile(
    f"[{re.escape(COLLAPSIBLE_WHITESPACE)}]+", cache_pattern=False
)
_LINE_BREAK_RUN_PATTERN: Final = re.compile(
    rf"[{re.escape(COLLAPSIBLE_WHITESPACE)}]*\n"
    rf"[{re.escape(COLLAPSIBLE_WHITESPACE)}]*",
    cache_pattern=False,
)

CLASS_ATTRIBUTE_NEWLINE: Final = "\x00DJLINT_CLASS_NEWLINE\x00"
VERBATIM_ATTRIBUTE_NEWLINE: Final = "\x00DJLINT_ATTR_NEWLINE\x00"
MIN_MULTILINE_CLASS_LINES: Final = 2
_CLASS_ATTRIBUTE_PATTERN: Final = re.compile(
    r"(?<![\w:.-])class(?![\w:.-])\s*=\s*(['\"])", re.I, cache_pattern=False
)

_JOINABLE_ATTRIBUTE_NAMES: Final = frozenset({
    "class",
    "data-srcset",
    "sizes",
    "srcset",
    "style",
})
_TRIMMED_ATTRIBUTE_NAMES: Final = frozenset({"class", "style"})


def encode_attribute_newlines(attributes: str, config: Config) -> str:
    """Replace significant attribute line breaks with internal markers.

    A `class` value is normalized here too: it is a list of tokens, so the
    whitespace between them and at its edges says nothing.
    """
    if "\n" not in attributes and not _CLASS_ATTRIBUTE_PATTERN.search(
        attributes
    ):
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
            config.format_attribute_js_json
            and config.format_attribute_js_json_pattern.match(name)
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
            encoded_value = _COLLAPSIBLE_RUN_PATTERN.sub(
                " ", value[1:-1]
            ).strip(COLLAPSIBLE_WHITESPACE)
        elif lowered in _TRIMMED_ATTRIBUTE_NAMES:
            encoded_value = _LINE_BREAK_RUN_PATTERN.sub(" ", value[1:-1]).strip(
                COLLAPSIBLE_WHITESPACE
            )
        elif lowered in _JOINABLE_ATTRIBUTE_NAMES:
            continue
        else:
            encoded_value = VERBATIM_ATTRIBUTE_NEWLINE.join(
                value[1:-1].split("\n")
            )

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
