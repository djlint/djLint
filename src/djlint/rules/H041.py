"""Rule H041: Check for html tags closed in a different template block."""

from __future__ import annotations

from bisect import bisect_right
from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_VOID_ELEMENTS
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    RE_FLAGS_IS,
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


_BLOCK_PATTERN: Final = re.compile(
    r"{%-?\s*(?P<closing>end)?block(?!trans)\b(?:(?!%}).)*?-?%}",
    RE_FLAGS_IS,
    cache_pattern=False,
)


def _block_paths(
    config: Config, html: str
) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    """Map document offsets to the stack of {% block %} tags around them."""
    boundaries = [0]
    paths: list[tuple[int, ...]] = [()]
    stack: list[int] = []
    counter = 0

    for match in _BLOCK_PATTERN.finditer(html):
        if overlaps_ignored_block(
            config, html, match
        ) or inside_ignored_linter_block(config, html, match):
            # block tags inside {# #}/{% comment %}/{% verbatim %}/{% raw %}
            # never execute, matching the token filtering below
            continue
        if match.group("closing"):
            if stack:
                stack.pop()
        else:
            counter += 1
            stack.append(counter)
        boundaries.append(match.end())
        paths.append(tuple(stack))

    return tuple(boundaries), tuple(paths)


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for html tags closed in a different template block."""
    boundaries, paths = _block_paths(config, html)
    if len(boundaries) == 1:
        # no {% block %} tags in the file
        return ()

    def path_at(pos: int) -> tuple[int, ...]:
        return paths[bisect_right(boundaries, pos) - 1]

    errors: list[LintError] = []
    open_tags: list[tuple[str, tuple[int, ...]]] = []

    for token in tokenize_tags(html):
        tag_name = token.name.lower()
        if (
            token.declaration
            or token.self_closing
            or tag_name in HTML_VOID_ELEMENTS
            or overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
            or inside_template_block(config, html, token)
        ):
            continue

        if not token.closing:
            open_tags.append((tag_name, path_at(token.start)))
            continue

        for index in range(len(open_tags) - 1, -1, -1):
            if open_tags[index][0] == tag_name:
                open_path = open_tags[index][1]
                del open_tags[index:]
                if open_path != path_at(token.start):
                    errors.append({
                        "code": rule["name"],
                        "line": get_line(token.start, line_ends),
                        "match": html[token.start : token.end].strip()[:20],
                        "message": rule["message"],
                    })
                break

    return tuple(errors)
