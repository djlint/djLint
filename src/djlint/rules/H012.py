"""Rule H012: Check for spaces around an attribute's equals sign.

The check walks one tag's attribute area at a time rather than scanning
from every angle bracket to the end of the file. A pattern anchored at
`<` has to walk forward looking for the spaced equals, and where a
document holds many `<` and no `>` that walk reaches the end of the file
from every one of them, which is quadratic. Two things bound the work
here: a document holding no spaced equals at all is answered by a single
scan, and a walk that has crossed a stretch of the document remembers
what it found there, so the tags sharing that stretch do not cross it
again.

The tags come from that walk rather than from the markup tokenizer, which
opens fewer of them: the replaced patterns read a tag the tokenizer turns
down, such as one named `<3div ` or one holding a stray brace, and a
document whose first tag leaves a quote open stops the tokenizer for
good, so tokenizing here would drop findings the rule used to report.
"""

from __future__ import annotations

from bisect import bisect_left
from itertools import chain
from typing import TYPE_CHECKING, NamedTuple

import regex as re

from djlint.helpers import (
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

# A tag opens on a name, and the walk over its attributes starts on the
# name's second character, the rest of the name being ordinary text to
# the walk.
_TAG_START_PATTERN: Final = re.compile(r"<\w", cache_pattern=False)

# The two spellings reported: a space before the equals and a space after
# it. A tag spaced on both sides is reported once for each.
_SPACE_BEFORE_PATTERN: Final = re.compile(r"\s+=", re.S, cache_pattern=False)
_SPACE_AFTER_PATTERN: Final = re.compile(r"=\s", re.S, cache_pattern=False)

_UNVISITED: Final = -2
_NOTHING: Final = -1


class _Span(NamedTuple):
    """Where a finding sits, standing in for the pattern match."""

    start: int
    end: int

    def span(self) -> tuple[int, int]:
        """Return the source span."""
        return self.start, self.end


class _Marks:
    """Where each character of interest sits, read once per document."""

    def __init__(self, html: str) -> None:
        self._html = html
        self._found: dict[str, list[int]] = {}

    def _positions(self, char: str) -> list[int]:
        positions = self._found.get(char)
        if positions is None:
            positions = []
            at = self._html.find(char)
            while at >= 0:
                positions.append(at)
                at = self._html.find(char, at + 1)
            self._found[char] = positions
        return positions

    def after(self, char: str, start: int) -> int:
        """The first `char` written at or after `start`, or -1."""
        positions = self._positions(char)
        index = bisect_left(positions, start)
        return positions[index] if index < len(positions) else _NOTHING


def _steps(html: str, marks: _Marks, position: int) -> tuple[int, ...]:
    """Where the walk can go from here, in the order the pattern tried.

    A quoted value and a template tag are each stepped over whole, so an
    equals written inside one is the author's text rather than an
    attribute's; anything else is read one character at a time, and a `>`
    or a brace the template spellings do not close ends the walk.
    """
    char = html[position]

    if char in {'"', "'"}:
        closing = marks.after(char, position + 1)
        return () if closing < 0 else (closing + 1,)

    if char == "{":
        steps: list[int] = []
        opener = html[position + 1 : position + 2]
        if opener in {"{", "%", "#"}:
            # `{{ }}`, `{% %}` and `{# #}` each close on their own mark
            # written against the brace
            closing = marks.after(
                "}" if opener == "{" else opener, position + 2
            )
            if closing >= 0 and html[closing + 1 : closing + 2] == "}":
                steps.append(closing + 2)
        # a lone `{ }` is stepped over the same way, and stands in where
        # one of the spellings above is left unclosed
        closing = marks.after("}", position + 1)
        if closing >= 0:
            steps.append(closing + 1)
        return tuple(steps)

    if char in {">", "}"}:
        return ()

    return (position + 1,)


def _walk(
    html: str,
    marks: _Marks,
    exits: dict[int, int],
    walked: dict[int, int],
    limit: int,
    start: int,
) -> int:
    """Where the walk starting here ends, or -1 if it reaches no equals.

    The pattern read the attributes greedily, so the walk keeps going for
    as long as it can and reports the last spaced equals it reaches
    rather than the first. Every position it settles shares its answer,
    so the walk of the next tag stops as soon as it meets a stretch this
    one has already read.
    """
    pending: list[tuple[int, tuple[int, ...], int]] = []
    position = start

    while True:
        found = walked.get(position, _UNVISITED)
        if found == _UNVISITED:
            if position > limit:
                found = _NOTHING
            else:
                steps = _steps(html, marks, position)
                if steps:
                    pending.append((position, steps, 0))
                    position = steps[0]
                    continue
                found = exits.get(position, _NOTHING)
                walked[position] = found

        descending = False
        while pending:
            origin, steps, index = pending.pop()
            if found != _NOTHING:
                walked[origin] = found
                continue
            index += 1
            if index < len(steps):
                pending.append((origin, steps, index))
                position = steps[index]
                descending = True
                break
            found = exits.get(origin, _NOTHING)
            walked[origin] = found

        if descending:
            continue
        if not pending:
            return found


def _spans(html: str, marks: _Marks, exits: dict[int, int]) -> Iterator[_Span]:
    """The tags reported, in the order the replaced pattern found them."""
    if not exits:
        return

    limit = max(exits)
    walked: dict[int, int] = {}
    position = 0
    while (tag := _TAG_START_PATTERN.search(html, position)) is not None:
        start = tag.start()
        if start > limit:
            return
        end = _walk(html, marks, exits, walked, limit, tag.end())
        if end == _NOTHING:
            position = start + 1
            continue
        yield _Span(start, end)
        # the replaced pattern took its matches apart, so a `<` written
        # inside one of them opened no tag of its own
        position = end


def _space_before(html: str) -> dict[int, int]:
    """Where a walk landing on the position reaches a space before `=`."""
    exits: dict[int, int] = {}
    for match in _SPACE_BEFORE_PATTERN.finditer(html):
        end = match.end()
        # the run of spaces is read greedily, so landing anywhere in it
        # reaches the same equals
        for position in range(match.start(), end - 1):
            exits[position] = end
    return exits


def _space_after(html: str) -> dict[int, int]:
    """Where a walk landing on the position reaches a space after `=`."""
    return {
        match.start(): match.end()
        for match in _SPACE_AFTER_PATTERN.finditer(html)
    }


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for spaces around an attribute's equals sign."""
    marks = _Marks(html)
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(span.start, line_ends),
            "match": html[span.start : span.end].strip()[:20],
            "message": rule["message"],
        }
        for span in chain(
            _spans(html, marks, _space_before(html)),
            _spans(html, marks, _space_after(html)),
        )
        # markup written inside a template tag is a string argument
        # rather than part of the document
        if not overlaps_ignored_block(config, html, span)
        and not inside_template_block(config, html, span)
        and not inside_ignored_rule(config, html, span, rule["name"])
        and not inside_ignored_linter_block(config, html, span)
    )
