"""Rule H036: Check for br tags used as vertical space.

Only the block element a break sits inside has to be read as a tag. That
check was a pattern anchored at `<`, walking forward over the attributes
to find the tag's `>`, and where a document holds many `<` and no `>`
that walk reaches the end of the file from every one of them, which is
quadratic.

The walk lands on the first `>` that is not inside a quoted value, and
the document's quotes and brackets answer that for every tag at once, so
they are read once instead. The other two checks read a break against its
neighbours rather than a tag and walk nowhere, so they stay patterns.
"""

from __future__ import annotations

from bisect import bisect_left
from itertools import chain
from typing import TYPE_CHECKING, NamedTuple

import regex as re

from djlint.helpers import (
    inside_html_attribute,
    inside_ignored_linter_block,
    inside_ignored_rule,
    inside_template_block,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError

# The elements whose own box carries the space a break against its edge
# would add.
_BLOCKS: Final = r"""
      p | div | li | dd | dt | td | th | section | article | aside
    | header | footer | main | nav | blockquote | figcaption | h[1-6]
"""
# A break carrying attributes is not this rule's business.
_BREAK: Final = r"<br\s*/?>"

# A run of breaks is vertical space rather than a break in the content.
_RUN_PATTERN: Final = re.compile(
    rf"{_BREAK}(?:\s|&nbsp;|&\#160;)*{_BREAK}", re.I | re.X, cache_pattern=False
)
_BEFORE_A_CLOSING_PATTERN: Final = re.compile(
    rf"{_BREAK}\s*</(?:{_BLOCKS})\s*>", re.I | re.X, cache_pattern=False
)
_OPENING_BLOCK_PATTERN: Final = re.compile(
    rf"<(?:{_BLOCKS})\b", re.I | re.X, cache_pattern=False
)
_AFTER_AN_OPENING_PATTERN: Final = re.compile(
    rf"\s*{_BREAK}", re.I | re.X, cache_pattern=False
)
_MARK_PATTERN: Final = re.compile(r"[\"'>]", cache_pattern=False)


class _Break(NamedTuple):
    """One use of a break, spanning what is reported with it."""

    start: int
    end: int

    def span(self) -> tuple[int, int]:
        """Return the source span."""
        return self.start, self.end


class _TagEnds(NamedTuple):
    """Where a tag running into each quote or bracket of the document ends."""

    marks: list[int]
    ends: list[int]

    def after(self, position: int) -> int:
        """The `>` ending a tag whose attributes start here, or -1."""
        return self.ends[bisect_left(self.marks, position)]


def _tag_ends(html: str) -> _TagEnds:
    """Answer where a tag ends for every position of the document at once.

    A tag ends at the first `>` outside a quoted value, so a `>` answers
    itself and a quote hands the question to the mark after the quote
    that closes it. Read from the back, each mark costs one lookup, where
    walking forward from every tag in turn re-reads the same text.
    """
    marks = [match.start() for match in _MARK_PATTERN.finditer(html)]
    unclosed = len(marks)
    ends = [-1] * (unclosed + 1)
    following = {'"': unclosed, "'": unclosed}

    for index in reversed(range(unclosed)):
        quote = html[marks[index]]
        if quote == ">":
            ends[index] = marks[index]
            continue
        closing = following[quote]
        if closing < unclosed:
            ends[index] = ends[closing + 1]
        following[quote] = index

    return _TagEnds(marks, ends)


def _spans(pattern: re.Pattern[str], html: str) -> Iterator[_Break]:
    return (_Break(*match.span()) for match in pattern.finditer(html))


def _against_a_block_opening(html: str) -> Iterator[_Break]:
    """Yield each break written against the inside edge of a block box.

    Openings are read in document order and one reported with a break is
    stepped over whole, so a tag inside the attributes of another is
    passed by the way the pattern's own non-overlapping search passed it.
    """
    ends: _TagEnds | None = None
    reported_to = 0

    for opening in _OPENING_BLOCK_PATTERN.finditer(html):
        if opening.start() < reported_to:
            continue
        if ends is None:
            ends = _tag_ends(html)
        tag_end = ends.after(opening.end())
        if tag_end < 0:
            continue
        following = _AFTER_AN_OPENING_PATTERN.match(html, tag_end + 1)
        if following is not None:
            yield _Break(opening.start(), following.end())
            reported_to = following.end()


def _reported(
    config: Config, html: str, rule: dict[str, Any], found: _Break
) -> bool:
    """Whether the use is a finding rather than ignored content.

    The rule looks for a tag, so markup written inside an attribute
    value, as in `<p title="a<br><br>b">`, is text rather than a tag of
    its own, and markup inside a template tag is a string argument rather
    than part of the document.
    """
    return not (
        inside_html_attribute(html, found)
        or inside_template_block(config, html, found)
        or overlaps_ignored_block(config, html, found)
        or inside_ignored_rule(config, html, found, rule["name"])
        or inside_ignored_linter_block(config, html, found)
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
    """Check for br tags used as vertical space.

    A break in the middle of a block's content is a break in the content,
    as the html specification puts it, and is left alone; a postal
    address is written that way. Reported instead are a run of breaks,
    which is vertical space, and a break against the inside edge of a
    block box, which renders nothing the box's own margin does not.
    """
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(found.start, line_ends),
            "match": html[found.start : found.end].strip()[:20],
            "message": rule["message"],
        }
        for found in chain(
            _spans(_RUN_PATTERN, html),
            _against_a_block_opening(html),
            _spans(_BEFORE_A_CLOSING_PATTERN, html),
        )
        if _reported(config, html, rule, found)
    )
