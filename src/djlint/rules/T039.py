"""Rule T039: Check for unclosed template tags."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line
from djlint.rules.T027 import _TemplateTagMatch

if TYPE_CHECKING:
    from collections.abc import Iterator

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


def _iter_unclosed_tags(html: str) -> Iterator[_TemplateTagMatch]:
    pos = 0
    length = len(html)
    while True:
        block_start = html.find("{%", pos)
        variable_start = html.find("{{", pos)
        if block_start == -1 and variable_start == -1:
            return
        if variable_start != -1 and (
            block_start == -1 or variable_start < block_start
        ):
            start, close = variable_start, "}}"
        else:
            start, close = block_start, "%}"

        scan = start + 2
        if close == "}}":
            if html.startswith("{{{{", start):
                # handlebars raw block delimiter: {{{{name}}}} / {{{{/name}}}}
                raw_end = html.find("}}}}", start + 4)
                pos = start + 4 if raw_end == -1 else raw_end + 4
                continue
            # skip comment tags: {{! }}, {{!-- --}}, {{/* */}} (golang)
            content_start = scan + 1 if html.startswith("-", scan) else scan
            if html.startswith("!--", content_start):
                comment_end = html.find("--}}", content_start + 3)
                pos = start + 2 if comment_end == -1 else comment_end + 4
                continue
            if html.startswith(("!", "/*"), content_start):
                comment_end = html.find("}}", content_start + 1)
                pos = start + 2 if comment_end == -1 else comment_end + 2
                continue

        quote = ""
        end = -1
        quoted_end = -1
        typo_end = -1
        while scan < length:
            char = html[scan]
            if quote:
                if char == "\\":
                    scan += 2
                    continue
                if char == quote:
                    quote = ""
                elif quoted_end == -1 and html.startswith(close, scan):
                    quoted_end = scan + 2
            elif char in {"'", '"'}:
                quote = char
            elif html.startswith(close, scan):
                end = scan + 2
                break
            elif close == "%}" and html.startswith("}%", scan):
                # {% ... }% is T034's typo; let T034 report it
                typo_end = scan + 2
                break
            elif html.startswith(("{%", "{{"), scan) or (
                close == "%}" and html.startswith("}}", scan)
            ):
                # another tag opens, or the wrong delimiter closes, before
                # this tag is closed
                break
            scan += 1

        if end != -1:
            pos = end
        elif typo_end != -1:
            pos = typo_end
        elif quoted_end != -1:
            # the tag's only close delimiter is inside an unclosed string;
            # T027 reports that
            pos = quoted_end
        else:
            yield _TemplateTagMatch(html, start, min(scan + 2, length))
            pos = start + 2


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for unclosed template tags."""
    errors: list[LintError] = []
    for match in _iter_unclosed_tags(html):
        if (
            overlaps_ignored_block(config, html, match)
            or inside_ignored_rule(config, html, match, rule["name"])
            or inside_ignored_linter_block(config, html, match)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })
    return tuple(errors)
