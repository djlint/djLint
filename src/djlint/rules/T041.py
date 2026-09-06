"""Rule T041: Check that the extends tag is the first tag in the template.

Django refuses a template whose `{% extends %}` comes after another tag,
and renders any text written before it, so the text leaks into the page
ahead of everything the parent produces. Jinja renders that text too, and
nunjucks drops it. A `{# #}` comment is the one thing every engine lets
stand before it. A branch tag is left alone on the jinja and nunjucks
profiles, where jinja documents
`{% if x %}{% extends "a" %}{% else %}{% extends "b" %}{% endif %}` as
the way to choose a parent; django reads the rest of the template into
the extends and then rejects the `{% endif %}`, so there it counts.

Which parts of the file produce nothing is worked out here rather than
taken from the shared ignored block patterns. Those are built for the
formatter and for rules about markup, and answer a different question:
they stop a `{% comment %}` block at the `{%` of its closing tag, never
match a named `{% verbatim x %}` block, and hide an html comment, a
`{% blocktrans %}` and a `<?php ?>` even though each of those is written
into the page ahead of everything the parent template produces, which is
the whole of what this rule looks for.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import TYPE_CHECKING

import regex as re

from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_AFTER_EVERY_SPAN: Final = float("inf")

_EXTENDS_PATTERN: Final = re.compile(
    r"{%[-+]?\s*extends\b(?:(?!%}).)*%}", re.S, cache_pattern=False
)

# whitespace and a byte order mark are all django lets a template hold
# ahead of its `{% extends %}`; jinja and nunjucks also take a branch
# tag, which opens nothing of its own.
_BLANK_PATTERN: Final = re.compile(r"[\s\ufeff]+", cache_pattern=False)
_BLANK_OR_BRANCH_PATTERN: Final = re.compile(
    r"(?:[\s\ufeff]+|{%[-+]?\s*(?:if|elif|else)\b(?:(?!%}).)*%})+",
    re.I | re.S,
    cache_pattern=False,
)
_PROFILES_REJECTING_A_BRANCHED_EXTENDS: Final = frozenset({"django"})

# a byte order mark ahead of the "---" still opens front matter
_FRONT_MATTER_PATTERN: Final = re.compile(
    r"\A\ufeff?---(?:(?!{%)[\s\S])*?^---[^\S\n]*$", re.M, cache_pattern=False
)

_OPENING_PATTERN: Final = re.compile(
    r"""
      (?P<off_html><!--\s*djlint:off(?P<off_html_rules>[^>]*?)-->)
    | (?P<on_html><!--\s*djlint:on\b[^>]*?-->)
    | (?P<off_hash>
        (?<!{){\#\s*djlint:\s*off(?P<off_hash_rules>(?:(?!\#}).)*)\#}
      )
    | (?P<off_comment>
        {%\s*comment\s*%}\s*djlint:off
        (?P<off_comment_rules>(?:(?!{%).)*)
        {%\s*endcomment\s*%}
      )
    | (?P<hash>(?<!{){\#)
    | (?P<comment>{%[-+]?\s*comment\b)
    | (?P<literal>{%[-+]?\s*(?P<literal_name>raw|verbatim)\b)
    | (?P<raw_text><(?P<raw_text_name>script|style|pre|textarea)\b)
    """,
    re.I | re.S | re.X,
    cache_pattern=False,
)

_ON_HTML_PATTERN: Final = re.compile(
    r"<!--\s*djlint:on\s*-->", re.I | re.S, cache_pattern=False
)
_ON_HASH_PATTERN: Final = re.compile(
    r"{\#\s*djlint:\s*on\s*\#}", re.I | re.S, cache_pattern=False
)
_ON_COMMENT_PATTERN: Final = re.compile(
    r"{%\s*comment\s*%}\s*djlint:on\s*{%\s*endcomment\s*%}",
    re.I | re.S,
    cache_pattern=False,
)
_END_COMMENT_PATTERN: Final = re.compile(
    r"{%[-+]?\s*endcomment\b(?:(?!%}).)*%}", re.I | re.S, cache_pattern=False
)
_END_LITERAL_PATTERNS: Final = {
    name: re.compile(
        rf"{{%[-+]?\s*end{name}\b(?:(?!%}}).)*%}}",
        re.I | re.S,
        cache_pattern=False,
    )
    for name in ("raw", "verbatim")
}
_CLOSING_RAW_TEXT_PATTERNS: Final = {
    name: re.compile(rf"</{name}\b", re.I, cache_pattern=False)
    for name in ("script", "style", "pre", "textarea")
}
_RULE_SEPARATOR_PATTERN: Final = re.compile(r"[\s,]+", cache_pattern=False)


def _region_end(html: str, start: int, closing: re.Pattern[str]) -> int:
    """Where a djlint:off region ends, its closing marker included.

    The marker is taken in so that it does not itself read as content: an
    `<!-- djlint:on -->` is an html comment, and this rule counts those.
    A region left open runs to the end of the file.
    """
    closed = closing.search(html, start)
    return closed.end() if closed else len(html)


def _turns_off(rules: str, name: str) -> bool:
    """Whether a djlint:off marker turns off this rule, or every rule."""
    listed = [x for x in _RULE_SEPARATOR_PATTERN.split(rules) if x]
    return not listed or name in listed


def _span(
    html: str, opening: re.Match[str], name: str, exhausted: set[str]
) -> tuple[int, int] | None:
    """The part of the file this opening skips, or None if it skips none.

    Each closing is looked for with a single search starting at the
    opening, and an opening whose kind has no closing left in the file
    marks that kind exhausted, so a file of unclosed openings costs one
    pass over it rather than one pass for each opening.
    """
    start, after = opening.span()

    if opening.group("off_html"):
        if _turns_off(opening.group("off_html_rules"), name):
            return (start, _region_end(html, after, _ON_HTML_PATTERN))
        return (start, after)

    if opening.group("on_html"):
        return (start, after)

    if opening.group("off_hash"):
        if _turns_off(opening.group("off_hash_rules"), name):
            return (start, _region_end(html, after, _ON_HASH_PATTERN))
        return (start, after)

    if opening.group("off_comment"):
        if _turns_off(opening.group("off_comment_rules"), name):
            return (start, _region_end(html, after, _ON_COMMENT_PATTERN))
        return (start, after)

    if opening.group("hash"):
        if "hash" in exhausted:
            return None
        closed = html.find("#}", after)
        if closed < 0:
            exhausted.add("hash")
            return None
        return (start, closed + 2)

    if opening.group("comment"):
        return _block_span(html, start, after, "comment", exhausted)

    if opening.group("literal"):
        return _block_span(
            html, start, after, opening.group("literal_name").lower(), exhausted
        )

    return _raw_text_span(
        html, after, opening.group("raw_text_name").lower(), exhausted
    )


def _block_span(
    html: str, start: int, after: int, name: str, exhausted: set[str]
) -> tuple[int, int] | None:
    """The span of a `{% comment %}`, `{% raw %}` or `{% verbatim %}`.

    It runs through the closing tag, which the shared patterns stop short
    of, and the closing tag is matched by name alone so that a named
    `{% verbatim x %}` is closed by its `{% endverbatim x %}`.
    """
    if name in exhausted:
        return None
    opening_end = html.find("%}", after)
    if opening_end < 0:
        exhausted.add(name)
        return None
    closing = (
        _END_COMMENT_PATTERN
        if name == "comment"
        else _END_LITERAL_PATTERNS[name]
    ).search(html, opening_end + 2)
    if closing is None:
        exhausted.add(name)
        return None
    return (start, closing.end())


def _raw_text_span(
    html: str, after: int, name: str, exhausted: set[str]
) -> tuple[int, int] | None:
    """The body of a script, style, pre or textarea element.

    The opening tag is left out, as it is in the shared lint patterns: it
    is markup of its own, and a template whose first tag is a `<script>`
    has content ahead of its `{% extends %}` whatever the body holds.
    """
    if "raw_text" in exhausted:
        return None
    body = html.find(">", after)
    if body < 0:
        exhausted.add("raw_text")
        return None
    closing = _CLOSING_RAW_TEXT_PATTERNS[name].search(html, body + 1)
    return (body + 1, closing.start() if closing else len(html))


def _skipped_spans(html: str, name: str) -> tuple[tuple[int, int], ...]:
    """The parts of the file that write nothing into the page.

    Scanning left to right and restarting each search where the last span
    ended keeps the whole pass linear, and leaves the spans sorted and
    free of overlaps, so a lookup can bisect them.
    """
    spans: list[tuple[int, int]] = []
    position = 0

    if front_matter := _FRONT_MATTER_PATTERN.match(html):
        spans.append(front_matter.span())
        position = front_matter.end()

    exhausted: set[str] = set()
    while opening := _OPENING_PATTERN.search(html, position):
        position = opening.end()
        if span := _span(html, opening, name, exhausted):
            spans.append(span)
            position = span[1]

    return tuple(spans)


def _skipped(spans: tuple[tuple[int, int], ...], start: int, end: int) -> bool:
    """Whether a span of the file lies inside a skipped one."""
    index = bisect_right(spans, (start, _AFTER_EVERY_SPAN)) - 1
    return index >= 0 and spans[index][0] <= start and end <= spans[index][1]


def _first_extends(
    html: str, spans: tuple[tuple[int, int], ...]
) -> re.Match[str] | None:
    """Find the first `{% extends %}` that runs.

    One inside a `{% comment %}`, `{% raw %}` or `{% verbatim %}` block,
    a `{# #}` comment or a djlint:off region never runs, so the search
    goes on past it.
    """
    for match in _EXTENDS_PATTERN.finditer(html):
        if not _skipped(spans, *match.span()):
            return match
    return None


def _holds_content(
    html: str, start: int, end: int, skippable: re.Pattern[str]
) -> bool:
    """Whether the slice holds anything the page will show."""
    position = start
    while position < end:
        skipped = skippable.match(html, position, end)
        if skipped is None:
            return True
        position = skipped.end()
    return False


def _something_precedes(
    html: str,
    spans: tuple[tuple[int, int], ...],
    end: int,
    skippable: re.Pattern[str],
) -> bool:
    """Whether anything the page will show comes before the extends.

    Only the gaps between the skipped spans are read, and the first
    character in one of them that the profile does not allow settles it,
    so no gap is scanned twice.
    """
    position = 0
    for span_start, span_end in spans:
        if span_start >= end:
            break
        if _holds_content(html, position, min(span_start, end), skippable):
            return True
        position = max(position, span_end)
        if position >= end:
            return False
    return _holds_content(html, position, end, skippable)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that the extends tag is the first tag in the template.

    Only the first `{% extends %}` that runs is checked. A second one is
    an error of its own, and not this rule's to report.
    """
    skippable = (
        _BLANK_PATTERN
        if config.profile in _PROFILES_REJECTING_A_BRANCHED_EXTENDS
        else _BLANK_OR_BRANCH_PATTERN
    )
    spans = _skipped_spans(html, rule["name"])
    extends = _first_extends(html, spans)
    if extends is None or not _something_precedes(
        html, spans, extends.start(), skippable
    ):
        return ()

    return (
        {
            "code": rule["name"],
            "line": get_line(extends.start(), line_ends),
            "match": extends.group().strip()[:20],
            "message": rule["message"],
        },
    )
