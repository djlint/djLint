"""Keep Mako's line-based syntax out of the formatter's hands.

Mako reads a line that starts with "%" as a control line, as in
`% if x:` and `% endif`, and one that starts with "##" as a comment. Both
must start a line of their own: joined onto another line, a control line
is text and a comment comments out what follows it. The formatter moves
lines around freely, so under the mako profile each of them is swapped
for a marker it keeps in place, and put back as written afterwards.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, final

import regex as re

from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import RE_FLAGS_IMS, RE_FLAGS_MX, compile_pattern

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final

# A control line or a comment. "%%" writes a literal "%", "%>" ends a python
# block, and a "%}" at the start of a line ends a template tag of another
# language under the all profile.
_MAKO_LINE_PATTERN: Final = compile_pattern(r"^[ \t]*(?:%(?![%>}])|\#\#)[^\n]*", RE_FLAGS_MX)
# What the formatter must leave as written: a `## djlint:off` region, a doc
# or text block, whose contents are a comment and literal output, and a
# python block, whose code is not markup.
_VERBATIM_PATTERN: Final = compile_pattern(
    r"""
      ^[ \t]*\#\#[ \t]*djlint:off\b.*?(?:^[ \t]*\#\#[ \t]*djlint:on\b[^\n]*|\Z)
    | <%(doc|text)\b.*?</%\1>
    | (<%(?![\w/]).*?%>)
    """,
    RE_FLAGS_IMS | re.X,
)
_MARKER_PREFIX: Final = "__djlint_mako_"
# What opens a Mako expression or tag.
_MAKO_SYNTAX: Final = ("${", "<%", "</%")


@final
class MaskedMako:
    """A piece of the template swapped for a marker."""

    __slots__ = ("in_tag", "marker", "text")

    def __init__(self, marker: str, text: str, *, in_tag: bool) -> None:
        self.marker = marker
        self.text = text
        self.in_tag = in_tag


def _blank_lines(html: str) -> str:
    """Blank the Mako lines to the same length, keeping the newlines."""
    return _MAKO_LINE_PATTERN.sub(lambda line: " " * len(line.group()), html)


def mask_mako(html: str) -> tuple[str, list[MaskedMako]]:
    """Swap the Mako syntax the formatter must not touch for markers.

    An opening tag that holds a control line, as in an attribute written
    only `% if` some condition holds, keeps its attributes as written: the
    lines between the control lines belong to them. The tag is read with
    the control lines blanked, so a ">" in a condition, as in `% if a > b:`,
    does not end it.
    """
    if "%" not in html and "##" not in html:
        return html, []

    prefix = _MARKER_PREFIX
    while prefix in html:
        prefix = f"_{prefix}"

    spans: list[tuple[int, int, bool]] = []
    python_blocks: list[tuple[int, int]] = []
    for block in _VERBATIM_PATTERN.finditer(html):
        if block.group(2) is not None:
            python_blocks.append(block.span())
        else:
            start, end = block.span()
            start += len(block.group()) - len(block.group().lstrip(" \t"))
            spans.append((start, end, False))

    def covered(start: int, end: int) -> bool:
        return any(
            span_start <= start and end <= span_end for span_start, span_end, _ in spans
        ) or any(
            block_start <= start and end <= block_end for block_start, block_end in python_blocks
        )

    blanked = _blank_lines(html)
    for token in tokenize_tags(blanked):
        if token.closing or token.declaration:
            continue
        # The attributes run up to the ">", or the "/" of "/>", whitespace
        # before it included, so the last control line keeps its line.
        area_end = token.end - (2 if token.self_closing else 1)
        area = html[token.name_end : area_end]
        if "\n" in area and _MAKO_LINE_PATTERN.search(area) and not covered(token.start, token.end):
            spans.append((token.name_end, area_end, True))

    for line in _MAKO_LINE_PATTERN.finditer(html):
        start, end = line.span()
        start += len(line.group()) - len(line.group().lstrip(" \t"))
        if not covered(start, end):
            spans.append((start, end, False))

    spans.sort()
    masked: list[MaskedMako] = []
    output: list[str] = []
    previous_end = 0
    for start, end, in_tag in spans:
        if start < previous_end:
            continue
        marker = f"{prefix}{len(masked)}__"
        masked.append(MaskedMako(marker, html[start:end], in_tag=in_tag))
        output.extend((html[previous_end:start], f" {marker}" if in_tag else f"<!--{marker}-->"))
        previous_end = end
    output.append(html[previous_end:])
    return "".join(output), masked


def holds_mako(profile: str, source: str) -> bool:
    """Whether a script or style body holds Mako syntax.

    A beautifier would take it apart: `${x}` outside a backquoted string
    and a `<%block>` tag are not javascript. Under the mako profile any of
    it counts, since Mako evaluates a `${}` in a script before the browser
    sees it; under another one only a masked control line or comment does.
    """
    if _MARKER_PREFIX in source:
        return True
    return profile == "mako" and any(syntax in source for syntax in _MAKO_SYNTAX)


def _starts_with_mako_line(text: str) -> bool:
    return _MAKO_LINE_PATTERN.match(text) is not None


def _ends_with_mako_line(text: str) -> bool:
    return _MAKO_LINE_PATTERN.match(text[text.rfind("\n") + 1 :]) is not None


def _constant(text: str) -> Callable[[re.Match[str]], str]:
    """A replacement that puts the text back as it is, backslashes and all."""
    return lambda _match: text


def restore_mako(html: str, masked: list[MaskedMako]) -> str:
    """Put the masked Mako syntax back as it was written.

    A control line or a comment gets a line of its own again, at the
    indentation the formatter gave its marker, since Mako reads the line
    the same wherever it starts. Anything else goes back exactly as written.
    """
    for piece in masked:
        if piece.in_tag:
            html = re.sub(
                rf"[ \t\n]*{re.escape(piece.marker)}[ \t\n]*", _constant(piece.text), html, count=1
            )
            continue

        marker = f"<!--{piece.marker}-->"
        start = html.find(marker)
        if start < 0:
            continue
        end = start + len(marker)
        line_start = html.rfind("\n", 0, start) + 1
        line_end = html.find("\n", end)
        if line_end < 0:
            line_end = len(html)
        before = html[line_start:start]
        after = html[end:line_end]
        indent = before[: len(before) - len(before.lstrip(" \t"))]

        text = piece.text
        if _starts_with_mako_line(text):
            text = text.lstrip(" \t")
            if before.strip():
                text = f"\n{indent}{text}"
        if _ends_with_mako_line(piece.text) and after.strip():
            text = f"{text}\n{indent}{after.lstrip(' ')}"
            end = line_end
        html = html[:start] + text + html[end:]
    return html
