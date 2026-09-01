"""Rule T027: Check for unclosed strings in template syntax."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if sys.version_info >= (3, 11):
    from typing import final
else:
    from typing_extensions import final

if TYPE_CHECKING:
    from collections.abc import Iterator

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


@final
@dataclass(
    repr=False,
    eq=False,
    frozen=True,
    match_args=False,
    kw_only=False,
    slots=True,
)
class _TemplateTagMatch:
    _html: str
    _start: int
    _end: int

    def span(self) -> tuple[int, int]:
        return self._start, self._end

    def start(self) -> int:
        return self._start

    def group(self) -> str:
        return self._html[self._start : self._end]


def _is_comment_tag(html: str, start: int) -> bool:
    pos = start + 2
    if pos < len(html) and html[pos] == "-":
        pos += 1
    while pos < len(html) and html[pos].isspace():
        pos += 1
    return html.startswith(("!", "/*"), pos)


def _close_past_strings(html: str, start: int, close: str) -> int:
    """Index of the closing delimiter, skipping over quoted strings.

    Returns -1 when a string runs to the end of the file, which is the
    unterminated string this rule is looking for; the caller then falls
    back to the first delimiter so the tag still has an end to report.
    """
    quote = ""
    pos = start + 2
    length = len(html)
    while pos < length:
        char = html[pos]
        if quote:
            if char == "\\":
                pos += 2
                continue
            if char == quote:
                quote = ""
        elif char in {"'", '"'}:
            quote = char
        elif html.startswith(close, pos):
            return pos
        pos += 1
    return -1


def _iter_template_tags(html: str) -> Iterator[_TemplateTagMatch]:
    pos = 0
    while True:
        block_start = html.find("{%", pos)
        variable_start = html.find("{{", pos)
        if block_start == -1 and variable_start == -1:
            break
        if variable_start != -1 and (
            block_start == -1 or variable_start < block_start
        ):
            start, close = variable_start, "}}"
        else:
            start, close = block_start, "%}"

        end = _close_past_strings(html, start, close)
        if end == -1:
            end = html.find(close, start + 2)
        if end == -1:
            pos = start + 2
            continue
        end += 2
        if close == "%}" or not _is_comment_tag(html, start):
            yield _TemplateTagMatch(html, start, end)
        pos = end


def _has_unclosed_string(html: str, start: int, end: int) -> bool:
    quote = ""
    pos = start + 2
    end -= 2
    while pos < end:
        char = html[pos]
        if quote:
            if char == "\\":
                pos += 2
                continue
            if char == quote:
                quote = ""
        elif char in {"'", '"'}:
            quote = char
        pos += 1
    return bool(quote)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for unclosed strings in template syntax."""
    errors: list[LintError] = []
    for match in _iter_template_tags(html):
        start, end = match.span()
        if not _has_unclosed_string(html, start, end):
            continue

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
