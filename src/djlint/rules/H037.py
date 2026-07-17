"""Rule H037: Check for duplicate HTML attributes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    RE_FLAGS_IX,
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_EVENT_PATTERN = re.compile(
    r""""[^"]*"|'[^']*'|"""
    r"(?P<template>{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|{\#(?:(?!\#}).)*\#})|"
    r"(?P<attribute>[-:a-z_][-:\w]*)(?=\s*=(?:\s*)(?:\"|'|{{|{%|{\#|[\w-]))",
    re.I | re.S,
    cache_pattern=False,
)


def _exclusive(
    left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...]
) -> bool:
    """Return whether two attributes are in different conditional branches."""
    right_branches = dict(right)
    return any(
        block in right_branches and branch != right_branches[block]
        for block, branch in left
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
    """Check for duplicate attributes that can occur on the same element."""
    errors: list[LintError] = []

    for token in tokenize_tags(html):
        if (
            token.closing
            or token.declaration
            or token.name_end == token.attributes_end
            or overlaps_ignored_block(config, html, token)
            or inside_ignored_rule(config, html, token, rule["name"])
            or inside_ignored_linter_block(config, html, token)
        ):
            continue

        attributes = html[token.name_end : token.attributes_end]
        blocks: list[list[int]] = []
        occurrences: dict[
            str, list[tuple[int, str, tuple[tuple[int, int], ...]]]
        ] = {}
        next_block = 0

        for match in _EVENT_PATTERN.finditer(attributes):
            if name := match.group("attribute"):
                occurrences.setdefault(name.lower(), []).append((
                    token.name_end + match.start("attribute"),
                    name,
                    tuple((block, branch) for block, branch in blocks),
                ))
                continue

            template_tag = match.group("template")
            if not template_tag:
                continue
            if re.match(config.tag_unindent_line, template_tag, RE_FLAGS_IX):
                if blocks:
                    blocks[-1][1] += 1
            elif re.match(config.template_unindent, template_tag, RE_FLAGS_IX):
                if blocks:
                    blocks.pop()
            elif re.match(config.template_indent, template_tag, RE_FLAGS_IX):
                blocks.append([next_block, 0])
                next_block += 1

        for repeated in occurrences.values():
            for index, (start, name, branches) in enumerate(repeated[:-1]):
                if any(
                    not _exclusive(branches, later_branches)
                    for _, _, later_branches in repeated[index + 1 :]
                ):
                    errors.append({
                        "code": rule["name"],
                        "line": get_line(start, line_ends),
                        "match": name,
                        "message": rule["message"],
                    })
                    break

    return tuple(errors)
