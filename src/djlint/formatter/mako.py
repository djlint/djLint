"""Keep Mako's line-based syntax out of the formatter's hands.

Mako reads a line that starts with "%" as a control line, as in
`% if x:` and `% endif`, and one that starts with "##" as a comment. Both
must start a line of their own: joined onto another line, a control line
is text and a comment comments out what follows it. The formatter moves
lines around freely, so under the mako profile each of them is swapped
for a marker it keeps in place, and put back as written afterwards.

A `${}` expression is python code, which the formatter would read as
markup, so it is swapped for a marker as well.
"""

from __future__ import annotations

from bisect import bisect_right
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
# A control line's part in a block: `% else:` and the like go on with one,
# `% endif` and the like end one, and any other line ending in a colon, as
# `% if x:` or `% for a in b:`, starts one.
_BRANCH_PATTERN: Final = compile_pattern(r"%[ \t]*(?:elif|else|except|finally)\b")
_END_PATTERN: Final = compile_pattern(r"%[ \t]*end\w*")
_START_PATTERN: Final = compile_pattern(r"%[ \t]*\w.*:[ \t]*(?:\#.*)?$")
# A Mako tag with a name, as `<%block name="x">` or `<%self:widget>`, and
# its closing tag. A python block has no name.
_MAKO_TAG_PATTERN: Final = compile_pattern(
    r"""<(/?)%([A-Za-z_][\w.:-]*)\b(?:"[^"]*"|'[^']*'|[^'">])*?(/?)>"""
)
# What opens a Mako expression or tag.
_MAKO_SYNTAX: Final = ("${", "<%", "</%")
# What Mako's lexer reads in an expression to find the brace that ends it:
# a comment, a string, which may hold a brace, and a bracket.
_EXPRESSION_TOKEN_PATTERN: Final = compile_pattern(
    r"""
      \#[^\n]*\n
    | "{3}(?:[^\\]|\\.)*?"{3} | '{3}(?:[^\\]|\\.)*?'{3}
    | "(?:[^\\"]++|\\.)*+" | '(?:[^\\']++|\\.)*+'
    | [{}()\[\]]
    """,
    re.S | re.X,
)
# Which of the three nesting levels a bracket changes, and by how much.
_BRACKETS: Final = {"{": (0, 1), "}": (0, -1), "(": (1, 1), ")": (1, -1), "[": (2, 1), "]": (2, -1)}
# What a shift of an expression's lines would change: a string or a line
# continuation that runs over lines.
_SPANS_LINES_PATTERN: Final = compile_pattern(r"""'{3}|"{3}|\\\n""")
# An expression's stand-in, whose lines the formatter may have joined.
_EXPRESSION_STAND_IN_PATTERN: Final = compile_pattern(r"\$\{[_\s]*?\}")
_NOT_NEWLINE_PATTERN: Final = compile_pattern(r"[^\n]")


@final
class MaskedMako:
    """A piece of the template swapped for a marker.

    The kind says what the piece is: "expression", "attributes", "line",
    "verbatim", or "open" or "close" for a Mako tag. The indent is that of
    the line an expression starts on.
    """

    __slots__ = ("indent", "kind", "marker", "text")

    def __init__(self, marker: str, text: str, kind: str, indent: str = "") -> None:
        self.marker = marker
        self.text = text
        self.kind = kind
        self.indent = indent


def _blank(html: str, stretches: list[tuple[int, int]]) -> str:
    """Blank stretches of the template to the same length, keeping the newlines."""
    output: list[str] = []
    previous_end = 0
    for start, end in sorted(stretches):
        if start < previous_end:
            continue
        output.extend((html[previous_end:start], _NOT_NEWLINE_PATTERN.sub(" ", html[start:end])))
        previous_end = end
    output.append(html[previous_end:])
    return "".join(output)


def _covers(spans: list[tuple[int, int]]) -> Callable[[int, int], bool]:
    """Whether the spans hold the whole of a stretch of the template."""
    merged: list[list[int]] = []
    for start, end in sorted(spans):
        if merged and start < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    starts = [start for start, _ in merged]

    def covered(start: int, end: int) -> bool:
        index = bisect_right(starts, start) - 1
        return index >= 0 and end <= merged[index][1]

    return covered


def _expression_end(html: str, start: int) -> int:
    """Where the expression that opens at start ends, or -1 if it does not.

    As in Mako, the expression ends at the first "}" outside a string or a
    comment where no bracket of any kind is open.
    """
    levels = [0, 0, 0]
    for token in _EXPRESSION_TOKEN_PATTERN.finditer(html, start + 2):
        bracket = _BRACKETS.get(token.group())
        if bracket is None:
            continue
        if token.group() == "}" and max(levels) <= 0:
            return token.end()
        levels[bracket[0]] += bracket[1]
    return -1


def _expressions(html: str, covered: Callable[[int, int], bool]) -> list[tuple[int, int]]:
    """The `${}` expressions outside the stretches covered.

    One that never ends is a syntax error in Mako, and the search stops
    there rather than read the rest of the template again for each one
    after it.
    """
    found: list[tuple[int, int]] = []
    start = html.find("${")
    while start >= 0:
        if covered(start, start + 2):
            start = html.find("${", start + 2)
            continue
        end = _expression_end(html, start)
        if end < 0:
            break
        found.append((start, end))
        start = html.find("${", end)
    return found


def _alone_on_its_line(html: str, start: int, end: int) -> bool:
    line_start = html.rfind("\n", 0, start) + 1
    line_end = html.find("\n", end)
    return (
        not html[line_start:start].strip()
        and not html[end : None if line_end < 0 else line_end].strip()
    )


def _line_indent(html: str, position: int) -> str:
    """The indentation of the line a position is on."""
    line_start = html.rfind("\n", 0, position) + 1
    line = html[line_start:position]
    return line[: len(line) - len(line.lstrip(" \t"))]


def _block_tags(html: str, covered: Callable[[int, int], bool]) -> list[tuple[int, int, str]]:
    """The Mako tags that hold a block of lines, as `<%block>` or `<%def>`.

    Only a pair whose opening and closing tags each stand alone on their
    line is one: laid out over lines, the tags of `<%block name="title">Hi
    </%block>` would add the line breaks to what the block renders.
    """
    found: list[tuple[int, int, str]] = []
    opened: list[tuple[str, int, int]] = []
    for tag in _MAKO_TAG_PATTERN.finditer(html):
        closing, name, self_closing = tag.group(1, 2, 3)
        start, end = tag.span()
        if self_closing or name in {"doc", "text"} or covered(start, end):
            continue
        if not closing:
            opened.append((name, start, end))
            continue
        for index in range(len(opened) - 1, -1, -1):
            if opened[index][0] == name:
                _, open_start, open_end = opened[index]
                del opened[index:]
                if _alone_on_its_line(html, open_start, open_end) and _alone_on_its_line(
                    html, start, end
                ):
                    found.extend(((open_start, open_end, "open"), (start, end, "close")))
                break
    return found


def _expression_stand_in(text: str) -> str:
    """An expression of underscores in the shape of the one it stands for.

    Each line keeps its indentation and length, so the formatter lays the
    lines out as it would have, and holds no space where the formatter
    could break it or read an attribute. A marker would make a short
    expression longer, so the stand-ins go back in the order they come in.
    """
    lines: list[str] = []
    for line in text.split("\n"):
        content = line.lstrip(" \t")
        lines.append(line[: len(line) - len(content)] + "_" * len(content))
    return "${" + "\n".join(lines)[2:-1] + "}"


def _stand_in(kind: str, text: str, marker: str) -> str:
    """What stands in for the masked text while the formatter runs.

    A control line or Mako tag that starts, goes on with or ends a block
    stands in as a template tag of that part, so the formatter indents the
    lines between as it does any template block. Attributes stand in as one
    attribute, an expression as one of underscores, and anything else as
    a comment, which the formatter keeps on the line it is written on.
    """
    if kind == "attributes":
        return f" {marker}"
    if kind == "open":
        return f"{{% if {marker} %}}"
    if kind == "close":
        return f"{{% endif {marker} %}}"
    if kind == "verbatim":
        return f"<!--{marker}-->"
    if kind == "expression":
        return _expression_stand_in(text)
    if _BRANCH_PATTERN.match(text):
        return f"{{% else {marker} %}}"
    if _END_PATTERN.match(text):
        return f"{{% endif {marker} %}}"
    if _START_PATTERN.match(text):
        return f"{{% if {marker} %}}"
    return f"<!--{marker}-->"


def mask_mako(html: str, *, expressions: bool) -> tuple[str, list[MaskedMako]]:
    """Swap the Mako syntax the formatter must not touch for markers.

    An opening tag that holds a control line, as in an attribute written
    only `% if` some condition holds, keeps its attributes as written: the
    lines between the control lines belong to them. The tag is read with
    the control lines and expressions blanked, so a ">" in a condition, as
    in `% if a > b:`, does not end it.

    Expressions are masked only when asked for: under the all profile a
    `${}` is as likely a javascript template literal.
    """
    if "%" not in html and "##" not in html and not (expressions and "${" in html):
        return html, []

    prefix = _MARKER_PREFIX
    while prefix in html:
        prefix = f"_{prefix}"

    spans: list[tuple[int, int, str]] = []
    python_blocks: list[tuple[int, int]] = []
    for block in _VERBATIM_PATTERN.finditer(html):
        if block.group(2) is not None:
            python_blocks.append(block.span())
        else:
            start, end = block.span()
            start += len(block.group()) - len(block.group().lstrip(" \t"))
            spans.append((start, end, "verbatim"))
    protected = [*python_blocks, *((start, end) for start, end, _ in spans)]
    covered = _covers(protected)

    lines: list[tuple[int, int]] = []
    for line in _MAKO_LINE_PATTERN.finditer(html):
        start, end = line.span()
        start += len(line.group()) - len(line.group().lstrip(" \t"))
        if not covered(start, end):
            lines.append((start, end))
    spans.extend((start, end, "line") for start, end in lines)

    found = _expressions(html, _covers([*protected, *lines])) if expressions else []
    spans.extend((start, end, "expression") for start, end in found)
    covered = _covers([*protected, *found])

    blanked = _blank(html, [*(line.span() for line in _MAKO_LINE_PATTERN.finditer(html)), *found])
    for token in tokenize_tags(blanked):
        if token.closing or token.declaration:
            continue
        # The attributes run up to the ">", or the "/" of "/>", whitespace
        # before it included, so the last control line keeps its line.
        area_end = token.end - (2 if token.self_closing else 1)
        area = html[token.name_end : area_end]
        if "\n" in area and _MAKO_LINE_PATTERN.search(area) and not covered(token.start, token.end):
            spans.append((token.name_end, area_end, "attributes"))

    spans.extend(_block_tags(html, covered))

    spans.sort()
    masked: list[MaskedMako] = []
    output: list[str] = []
    previous_end = 0
    for start, end, kind in spans:
        if start < previous_end:
            continue
        marker = f"{prefix}{len(masked)}__"
        text = html[start:end]
        indent = _line_indent(html, start) if kind == "expression" else ""
        masked.append(MaskedMako(marker, text, kind, indent))
        output.extend((html[previous_end:start], _stand_in(kind, text, marker)))
        previous_end = end
    output.append(html[previous_end:])
    masked_html = "".join(output)
    # A python block, left in place, could hold what reads as a stand-in.
    if found and len(_EXPRESSION_STAND_IN_PATTERN.findall(masked_html)) != sum(
        piece.kind == "expression" for piece in masked
    ):
        return mask_mako(html, expressions=False)
    return masked_html, masked


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


def _restore_expressions(html: str, masked: list[MaskedMako]) -> str | None:
    """Put the expressions back, or None if their stand-ins are not all there.

    The lines of an expression after its first move as far as the formatter
    moved the line it starts on: python reads the lines inside brackets the
    same wherever they start. One that runs a string or a line continuation
    over lines goes back exactly as written.
    """
    expressions = [piece for piece in masked if piece.kind == "expression"]
    if not expressions:
        return html
    stand_ins = list(_EXPRESSION_STAND_IN_PATTERN.finditer(html))
    if len(stand_ins) != len(expressions):
        return None

    def replace(stand_in: re.Match[str], piece: MaskedMako) -> str:
        text = piece.text
        indent = _line_indent(stand_in.string, stand_in.start())
        if "\n" not in text or indent == piece.indent or _SPANS_LINES_PATTERN.search(text):
            return text
        first, *rest = text.split("\n")
        return "\n".join([
            first,
            *(
                indent + line[len(piece.indent) :]
                if line.strip() and line.startswith(piece.indent)
                else line
                for line in rest
            ),
        ])

    output: list[str] = []
    previous_end = 0
    for stand_in, piece in zip(stand_ins, expressions, strict=True):
        output.extend((html[previous_end : stand_in.start()], replace(stand_in, piece)))
        previous_end = stand_in.end()
    output.append(html[previous_end:])
    return "".join(output)


def restore_mako(html: str, masked: list[MaskedMako]) -> str | None:
    """Put the masked Mako syntax back as it was written.

    A control line or a comment gets a line of its own again, at the
    indentation the formatter gave its marker, since Mako reads the line
    the same wherever it starts. The other lines of an expression move with
    its first, and anything else goes back exactly as written. None means
    the expressions could not all be put back.
    """
    restored = _restore_expressions(html, masked)
    if restored is None:
        return None
    html = restored
    for piece in masked:
        if piece.kind == "expression":
            continue
        if piece.kind == "attributes":
            html = re.sub(
                rf"[ \t\n]*{re.escape(piece.marker)}[ \t\n]*", _constant(piece.text), html, count=1
            )
            continue

        stand_in = re.search(
            rf"<!--{re.escape(piece.marker)}-->|\{{%[^%]*?{re.escape(piece.marker)}[ \t]*%\}}", html
        )
        if stand_in is None:
            continue
        start, end = stand_in.span()
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
