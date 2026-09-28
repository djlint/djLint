"""Rule T001: Check that template tags are padded with whitespace."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line
from djlint.rules.T027 import _close_past_strings, _TemplateTagMatch

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError

_DELIMITERS: Final = (("{{", "}}"), ("{%", "%}"))
_MARKERS: Final = frozenset("-+")


def _iter_tags(html: str) -> Iterator[tuple[int, int, str]]:
    """Yield the span and closing delimiter of every template tag.

    A delimiter written inside a string belongs to the string, so
    `{{ x|default('}}') }}` is one tag rather than a tag cut in half.
    """
    pos = 0
    length = len(html)
    while pos < length:
        starts = [
            (found, close)
            for open_delimiter, close in _DELIMITERS
            if (found := html.find(open_delimiter, pos)) != -1
        ]
        if not starts:
            return
        start, close = min(starts)

        close_start = _close_past_strings(html, start, close)
        if close_start is None or close_start == -1:
            pos = start + 2
            continue
        yield start, close_start + 2, close
        pos = close_start + 2


def _is_padded(html: str, start: int, end: int) -> bool:
    """Whether the tag's contents are separated from both delimiters."""
    open_end = start + 2
    if open_end < end and html[open_end] in _MARKERS:
        open_end += 1
    close_start = end - 2
    if close_start > open_end and html[close_start - 1] in _MARKERS:
        close_start -= 1

    contents = html[open_end:close_start]
    if not contents.strip():
        return True
    return contents[0].isspace() and contents[-1].isspace()


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check that template tags are padded with whitespace.

    An empty tag has nothing to pad, and extra padding is `T032`'s to
    report, so only a tag whose contents touch a delimiter is reported.
    """
    errors: list[LintError] = []
    for start, end, _close in _iter_tags(html):
        if _is_padded(html, start, end):
            continue

        match = _TemplateTagMatch(html, start, end)
        if (
            overlaps_ignored_block(config, html, match)
            or inside_ignored_rule(config, html, match, rule["name"])
            or inside_ignored_linter_block(config, html, match)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(start, line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })
    return tuple(errors)
