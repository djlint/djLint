"""Rule T044: Check for a statement keyword written inside an output tag.

An output tag prints a value, so `{{ if x }}`, `{{ url 'home' }}` and
`{{ endif }}` are statements written in the wrong delimiters. Django,
Jinja and Nunjucks all raise a syntax error on the first two, and a
closing keyword on its own is read as a variable that renders nothing
while the block it was meant to close stays open.

A bare keyword is an ordinary variable lookup, `{{ url }}` above all, so
only a keyword given an argument is reported. A control keyword such as
`if` or `for` can never begin an expression, so whatever follows it is
an argument. The remaining names double as variables and functions, and
there only a quoted string or a word counts as an argument, which leaves
an expression that merely starts with the name alone: `{{ url ~ "/x" }}`,
`{{ url ? url : '#' }}`, `{{ block .super }}` and `{{ filter [0] }}`.

The rule reads `{% raw %}` and `{% verbatim %}` blocks for itself, over
and above the shared span helper. That helper pairs an opener only with
a closer carrying no name, so the named form Django's own docs use to
embed another templating language,
`{% verbatim vueapp %}...{% endverbatim vueapp %}`, would otherwise
leave its body exposed, and that body is exactly where a `{{ if }}` or a
`{{ else }}` belonging to Vue or Handlebars is written. A `{{ }}` inside
a quoted argument of a block tag, as in
`{% trans "Write {{ if x }} instead" %}`, is text the engine prints
rather than a tag, and is left alone too.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_AFTER_EVERY_SPAN: Final = float("inf")

_STATEMENT_PATTERN: Final = re.compile(
    r"""
    (?<!\{)\{\{[-+]?\s*
    (?:
        # nothing prints one of these as a value, in a template or in
        # the javascript a template carries, so whatever is written
        # after one is its argument, an operator included
        (?:if|elif|for|extends|import|with|autoescape)
        \s+[^\s}|]
      |
        # these double as variables and functions, so only a quoted
        # string or a word counts as an argument; an operator, a
        # subscript, a call, a comma and an expression word all belong
        # to an expression that merely starts with the name
        (?:blocktrans|block|include|set|load|url|trans|call|filter
          |cycle|firstof|now|regroup|widthratio|macro|from)
        \s+(?!(?:is|in|if|and|or|not|else)(?![\w.]))["'\w]
    )
    """,
    re.S | re.X,
    cache_pattern=False,
)
_KEYWORD_ONLY_PATTERN: Final = re.compile(
    r"""
    # a closing or branch keyword on its own is never a variable name in
    # practice; the lookbehind keeps a handlebars triple stash out
    (?<!\{)\{\{[-+]?\s*
    (?:
        end(?:if|for|block|with|set|macro|call|filter|autoescape|comment
            |raw|verbatim|spaceless|blocktrans|translate|trans)
      | else
      | elif
    )
    \s*[-+]?\}\}
    """,
    re.S | re.X,
    cache_pattern=False,
)
_RAW_TAG_PATTERN: Final = re.compile(
    r"""
    # the body stops at the next tag opening so that an unclosed `{%`
    # costs the scan the distance to its neighbour rather than the rest
    # of the file
    \{%[-+]?\s*(end)?(raw|verbatim)\b(?:(?!%\}|\{%).)*?%\}
    """,
    re.I | re.S | re.X,
    cache_pattern=False,
)
_BLOCK_TAG_PATTERN: Final = re.compile(
    r"\{%(?:(?!%\}|\{%).)*?%\}", re.S, cache_pattern=False
)
_QUOTED_PATTERN: Final = re.compile(
    r"\"[^\"]*\"|'[^']*'", re.S, cache_pattern=False
)


def _raw_block_spans(html: str) -> tuple[tuple[int, int], ...]:
    """Where a `{% raw %}` or `{% verbatim %}` block holds the document.

    An opener already inside one is part of the text the block emits, so
    the first closer of the same name ends it, and an opener that is
    never closed covers nothing.
    """
    spans: list[tuple[int, int]] = []
    open_start: int | None = None
    open_name = ""

    for match in _RAW_TAG_PATTERN.finditer(html):
        name = match.group(2).lower()
        if open_start is None:
            if not match.group(1):
                open_start, open_name = match.start(), name
        elif match.group(1) and name == open_name:
            spans.append((open_start, match.end()))
            open_start = None

    return tuple(spans)


def _quoted_argument_spans(html: str) -> tuple[tuple[int, int], ...]:
    """Where a block tag holds a quoted string."""
    return tuple(
        (tag.start() + quoted.start(), tag.start() + quoted.end())
        for tag in _BLOCK_TAG_PATTERN.finditer(html)
        for quoted in _QUOTED_PATTERN.finditer(tag.group())
    )


def _covered_by(spans: Sequence[tuple[int, int]], match: re.Match[str]) -> bool:
    """Whether one of the sorted, non overlapping spans holds the match."""
    start, end = match.span()
    index = bisect_right(spans, (start, _AFTER_EVERY_SPAN)) - 1
    if index < 0:
        return False

    span_start, span_end = spans[index]
    return span_start <= start and end <= span_end


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for a statement keyword written inside an output tag.

    The spans a match is measured against are built only once a match
    exists, so a file the rule has nothing to say about is scanned by the
    two keyword patterns alone.
    """
    matches = sorted(
        (
            match
            for pattern in (_STATEMENT_PATTERN, _KEYWORD_ONLY_PATTERN)
            for match in pattern.finditer(html)
        ),
        key=lambda match: match.start(),
    )
    if not matches:
        return ()

    raw_blocks = _raw_block_spans(html)
    quoted_arguments = _quoted_argument_spans(html)

    return tuple(
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in matches
        if not _covered_by(raw_blocks, match)
        and not _covered_by(quoted_arguments, match)
        and not overlaps_ignored_block(config, html, match)
        and not inside_ignored_rule(config, html, match, rule["name"])
        and not inside_ignored_linter_block(config, html, match)
    )
