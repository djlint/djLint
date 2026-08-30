"""Rule H037: Check for duplicate HTML attributes.

An attribute name is read as a whole run of name characters, never from
the middle of one. Html allows "." in a name and frameworks build names
around it (alpine's x-on:click.prevent, vue's @keyup.enter); read from the
middle, data-a.checked and data-b.checked would both come out as "checked"
and look like a duplicate.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


_NAME_CHAR = r"[-.:\w]"
_EVENT_PATTERN = re.compile(
    r""""[^"]*"|'[^']*'|"""
    r"(?P<template>{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|{\#(?:(?!\#}).)*\#})|"
    rf"(?P<attribute>(?<!{_NAME_CHAR}){_NAME_CHAR}+)"
    r"(?=\s*=(?:\s*)(?:\"|'|{{|{%|{\#|[\w-]))",
    re.I | re.S,
    cache_pattern=False,
)
_NAME_CHAR_PATTERN = re.compile(_NAME_CHAR, cache_pattern=False)
_HANDLEBARS_OR_GOLANG_COMMENT_PATTERN = re.compile(
    r"\{\{-?\s*(?:!|/\*)", cache_pattern=False
)


def _exclusive(
    left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...]
) -> bool:
    """Return whether two attributes are in different conditional branches."""
    right_branches = dict(right)
    for block, branch in left:
        if block in right_branches and branch != right_branches[block]:
            return True
    return False


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for duplicate attributes that can occur on the same element.

    A name reached after a template tag that renders text, as in
    `{% if x %}data-{% endif %}srcset`, has a template-generated prefix
    glued onto it, so it is not a definite duplicate of a plain occurrence
    of the name. A template comment renders as nothing and glues on
    nothing, so it does not count.
    """
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

        prefixed_from = -1

        for match in _EVENT_PATTERN.finditer(attributes):
            if name := match.group("attribute"):
                if match.start("attribute") == prefixed_from:
                    continue
                occurrences.setdefault(name.lower(), []).append((
                    token.name_end + match.start("attribute"),
                    name,
                    tuple((block, branch) for block, branch in blocks),
                ))
                continue

            template_tag = match.group("template")
            if not template_tag:
                continue
            prefixed_from = -1
            if config.tag_unindent_line_ix_pattern.match(template_tag):
                if blocks:
                    blocks[-1][1] += 1
            elif config.template_unindent_ix_pattern.match(template_tag):
                if blocks:
                    blocks.pop()
                if match.start() and _NAME_CHAR_PATTERN.match(
                    attributes[match.start() - 1]
                ):
                    prefixed_from = match.end()
            elif config.template_indent_ix_pattern.match(template_tag):
                blocks.append([next_block, 0])
                next_block += 1
            elif template_tag.startswith(
                "{{"
            ) and not _HANDLEBARS_OR_GOLANG_COMMENT_PATTERN.match(template_tag):
                prefixed_from = match.end()

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
