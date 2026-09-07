"""Rule H022: Check for an external link written over plain http.

The check walks one tag's attribute area at a time rather than scanning
from every angle bracket to the end of the file. A pattern anchored at
`<` has to walk forward looking for the link, and where a document holds
many `<` and no `>` that walk reaches the end of the file from every one
of them, which is quadratic. Two things bound the work here: a document
with no plain http link at all is answered by a single scan, and a walk
that has crossed a stretch of the document remembers what it found there,
so the tags sharing that stretch do not cross it again.

The tags come from that walk rather than from the markup tokenizer, which
opens fewer of them: the replaced pattern reads a tag the tokenizer turns
down, such as one named `<3div ` or one holding a stray brace, and a
document whose first tag leaves a quote open stops the tokenizer for
good, so tokenizing here would drop findings the rule used to report.
"""

from __future__ import annotations

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
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError

_TAG_START_PATTERN: Final = re.compile(r"<\w+\s", cache_pattern=False)

# a loopback or a private host is not external, and a dotted name ending
# in .local, .test or .localhost names a development machine
_LINK_PATTERN: Final = re.compile(
    r"""
    (?<![-.:\w])
    (?:href|data-url|action|src|url|srcset)
    \s*=["']http://
    (?!
        localhost[:/"']
      | 127\.0\.0\.1
      | 0\.0\.0\.0
      | \[::1\]
      | 10\.
      | 192\.168\.
      | 172\.(?:1[6-9]|2\d|3[01])\.
      | [^"'/]*\.(?:local|test|localhost)[:/"']
    )
    """,
    re.I | re.X,
    cache_pattern=False,
)

_UNVISITED: Final = -2
_NOTHING: Final = -1


class _Span(NamedTuple):
    """Where a finding sits, standing in for the pattern match."""

    start: int
    end: int

    def span(self) -> tuple[int, int]:
        """Return the source span."""
        return self.start, self.end


def _first_link(
    html: str,
    links: dict[int, int],
    walked: dict[int, int],
    start: int,
    limit: int,
) -> int:
    """Where the first link the attribute walk reaches ends, or -1.

    A quoted value is stepped over whole, so an "http://" written inside
    one is the author's text rather than a link of its own, and the walk
    ends at the ">" that closes the tag. Every position it crosses shares
    its answer, so the walk of the next tag stops as soon as it meets a
    stretch this one has already read.
    """
    crossed: list[int] = []
    cursor = start
    found = _NOTHING
    while cursor <= limit:
        remembered = walked.get(cursor, _UNVISITED)
        if remembered != _UNVISITED:
            found = remembered
            break
        link = links.get(cursor)
        if link is not None:
            found = link
            break
        crossed.append(cursor)
        char = html[cursor]
        if char == ">":
            break
        if char in {'"', "'"}:
            closing = html.find(char, cursor + 1)
            if closing < 0:
                break
            cursor = closing + 1
        else:
            cursor += 1

    for position in crossed:
        walked[position] = found
    return found


def _spans(html: str) -> tuple[_Span, ...]:
    """The tags reported, in the order the replaced pattern found them."""
    links = {
        match.start(): match.end()
        for match in _LINK_PATTERN.finditer(html, overlapped=True)
    }
    if not links:
        return ()

    limit = max(links)
    walked: dict[int, int] = {}
    found: list[_Span] = []
    position = 0
    while 0 <= (start := html.find("<", position)) <= limit:
        tag = _TAG_START_PATTERN.match(html, start)
        if tag is None:
            position = start + 1
            continue
        end = _first_link(html, links, walked, tag.end(), limit)
        if end == _NOTHING:
            position = start + 1
            continue
        found.append(_Span(start, end))
        # the replaced pattern took its matches apart, so a "<" written
        # inside one of them opened no tag of its own
        position = end
    return tuple(found)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for an external link written over plain http."""
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(span.start, line_ends),
            "match": html[span.start : span.end].strip()[:20],
            "message": rule["message"],
        }
        for span in _spans(html)
        # markup written inside an attribute value, as in
        # `<p title="<a href='http://x'>">`, is text rather than a tag
        if not inside_html_attribute(html, span)
        and not overlaps_ignored_block(config, html, span)
        and not inside_template_block(config, html, span)
        and not inside_ignored_rule(config, html, span, rule["name"])
        and not inside_ignored_linter_block(config, html, span)
    )
