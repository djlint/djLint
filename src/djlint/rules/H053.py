"""Rule H053: Check for an id used more than once in the file.

An id names one element. A second element carrying the same id breaks
`getElementById`, `<label for>`, fragment links and `aria-labelledby`:
the browser takes the first and silently ignores the rest.

Two ids in exclusive branches of one `{% if %}...{% else %}...{% endif %}`
are never both rendered, so they are not a duplicate. A `{% for %}` loop
or a `{% block %}` is a block but not a branch: an id inside one and the
same id outside it both render, and the later one is reported. A mako
line statement, as `% else:`, branches just as `{% else %}` does and is
read the same way.

A value holding template syntax is unknowable and is left alone, and so
is an empty value.
"""

from __future__ import annotations

from bisect import bisect_right
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    mutually_exclusive,
    overlaps_ignored_block,
    tokenize_markup,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_NAME_CHAR: Final = r"[-.:\w]"
_TEMPLATE_TAG: Final = r"{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|{#(?:(?!#}).)*#}"
_ATTRIBUTE_PATTERN: Final = re.compile(
    rf"(?P<attribute>(?<!{_NAME_CHAR})id\s*=\s*"
    r"(?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)'|(?P<uq>[^\s\"'<>`=]+)))"
    rf"|{_TEMPLATE_TAG}"
    rf"|{_NAME_CHAR}+\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'<>`=]+)"
    r"|\"[^\"]*\"|'[^']*'",
    re.I | re.S,
    cache_pattern=False,
)
_BLOCK_TAG_PATTERN: Final = re.compile(
    r"{%(?:(?!%}).)*%}|{{(?:(?!}}).)*}}"
    r"|^[ \t]*%[ \t]*(?P<statement>if|elif|else|endif|for|endfor)\b[^\n]*",
    re.M | re.S,
    cache_pattern=False,
)
_OPEN_NAME_PATTERN: Final = re.compile(
    r"(?:\{%[-+]?|\{\{[#^][*>]?)\s*([\w.-]+)", cache_pattern=False
)
_END_NAME_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*end([\w.-]*)|\{\{/\s*([\w.-]+)", cache_pattern=False
)
_BRANCH_STATEMENTS: Final = frozenset(("elif", "else"))
_TEMPLATE_SYNTAX: Final = ("{{", "{%", "{#", "${")


def _role(config: Config, match: re.Match[str]) -> tuple[str, str] | None:
    """The part a tag plays in branching, with the block name it carries.

    A tag that neither opens, closes nor branches a block, as an
    `{% include %}` or a `{{ variable }}`, plays no part and gives None.
    """
    statement = match.group("statement")
    if statement:
        if statement in _BRANCH_STATEMENTS:
            return "branch", ""
        if statement.startswith("end"):
            return "close", statement[3:]
        return "open", statement
    tag = match.group()
    if config.tag_unindent_line_ix_pattern.match(tag):
        return "branch", ""
    if config.template_unindent_ix_pattern.match(tag):
        end_name = _END_NAME_PATTERN.match(tag)
        if end_name is None:
            return "close", ""
        return "close", end_name.group(1) or end_name.group(2) or ""
    if config.template_indent_ix_pattern.match(tag):
        open_name = _OPEN_NAME_PATTERN.match(tag)
        return "open", open_name.group(1) if open_name else ""
    return None


def _closed_depth(stack: list[tuple[str, int, int]], name: str) -> int:
    """How many open blocks an end tag closes, or 0 for an orphan.

    An end tag naming a block that was never opened, as the closer of a
    custom block djLint does not model, closes nothing, so it cannot pop
    the `{% if %}` around it. An unnamed closer, as go's `{{ end }}`,
    closes the innermost block.
    """
    if not name:
        return 1
    for depth, (open_name, _, _) in enumerate(reversed(stack), start=1):
        if open_name == name:
            return depth
    return 0


def _branch_paths(
    config: Config, html: str
) -> tuple[tuple[int, ...], tuple[dict[int, int], ...]]:
    """Map document offsets to the branch of each block around them.

    A path maps every open block to the branch in force, so two offsets
    are in exclusive branches when they disagree on a block they share.
    A block tag inside an ignored block never executes and opens nothing,
    matching the token filtering the rule itself applies.
    """
    boundaries = [0]
    paths: list[dict[int, int]] = [{}]
    stack: list[tuple[str, int, int]] = []
    next_block = 0

    for match in _BLOCK_TAG_PATTERN.finditer(html):
        if overlaps_ignored_block(
            config, html, match
        ) or inside_ignored_linter_block(config, html, match):
            continue
        role = _role(config, match)
        if role is None:
            continue
        part, name = role
        if part == "branch":
            if not stack:
                continue
            open_name, block, branch = stack[-1]
            stack[-1] = (open_name, block, branch + 1)
        elif part == "close":
            closed = _closed_depth(stack, name)
            if not closed:
                continue
            del stack[-closed:]
        else:
            stack.append((name, next_block, 0))
            next_block += 1
        boundaries.append(match.end())
        paths.append({block: branch for _, block, branch in stack})

    return tuple(boundaries), tuple(paths)


def _ids(
    html: str, name_end: int, attributes_end: int
) -> list[tuple[re.Match[str], str]]:
    """The literal, non-empty id values written between two offsets.

    Other attributes, stray quoted strings and template tags are consumed
    whole, so an `id=` written inside a title, or a `data-id`, is not read
    as an id. A value holding template syntax is unknowable and skipped.
    """
    return [
        (match, value)
        for match in _ATTRIBUTE_PATTERN.finditer(html, name_end, attributes_end)
        if match.group("attribute")
        for value in (
            match.group("dq") or match.group("sq") or match.group("uq") or "",
        )
        if value and not any(marker in value for marker in _TEMPLATE_SYNTAX)
    ]


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for an id used more than once in the file."""
    errors: list[LintError] = []
    boundaries, paths = _branch_paths(config, html)
    seen: dict[str, list[dict[int, int]]] = {}

    for token in tokenize_markup(html):
        if (
            token.closing
            or token.declaration
            or token.name_end == token.attributes_end
        ):
            continue

        ids = _ids(html, token.name_end, token.attributes_end)
        if not ids:
            continue

        if (
            overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            continue

        for match, value in ids:
            path = paths[bisect_right(boundaries, match.start()) - 1]
            earlier = seen.setdefault(value, [])
            if any(
                not mutually_exclusive(previous, path) for previous in earlier
            ):
                errors.append({
                    "code": rule["name"],
                    "line": get_line(match.start(), line_ends),
                    "match": match.group()[:20],
                    "message": rule["message"],
                })
            earlier.append(path)

    return tuple(errors)
