"""rule H025: Check for orphans html tags."""

from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_VOID_ELEMENTS
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    child_of_unformatted_block,
    inside_ignored_block,
    inside_ignored_linter_block,
    inside_ignored_rule,
    inside_template_block,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config
    from djlint.types import LintError


P_LIST_CHILD_MESSAGE: Final = "List tags should not be nested inside p tags."
P_LIST_CHILD_TAGS: Final = frozenset(("ol", "ul"))

_BRANCHED_BLOCK_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*(endif|endfor|elseif|elif|else|empty|if|for)\b",
    cache_pattern=False,
)
_BLOCK_OPENINGS: Final = frozenset(("if", "for"))
_BLOCK_ENDINGS: Final = frozenset(("endif", "endfor"))


def _branched_blocks(html: str) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Branch spans of every complete if or for block.

    A for block takes branches of its own, since jinja spells its empty
    case {% else %} and django spells it {% empty %}. Without that, the
    else of a for nested in an if would end the if's own branch.
    """
    complete: list[tuple[tuple[int, int], ...]] = []
    open_blocks: list[tuple[list[tuple[int, int]], int]] = []
    for match in _BRANCHED_BLOCK_PATTERN.finditer(html):
        keyword = match.group(1)
        if keyword in _BLOCK_OPENINGS:
            open_blocks.append(([], match.end()))
        elif not open_blocks:
            continue
        elif keyword in _BLOCK_ENDINGS:
            branches, start = open_blocks.pop()
            branches.append((start, match.start()))
            complete.append(tuple(branches))
        else:
            branches, start = open_blocks[-1]
            branches.append((start, match.start()))
            open_blocks[-1] = (branches, match.end())
    return tuple(complete)


def _branch_context(
    blocks: tuple[tuple[tuple[int, int], ...], ...], pos: int
) -> dict[int, int]:
    """Map each block containing pos to the branch pos is in.

    Branches run in order and do not overlap, so a block that does not
    span pos at all is skipped without looking at its branches.
    """
    context: dict[int, int] = {}
    for index, branches in enumerate(blocks):
        if not branches[0][0] <= pos < branches[-1][1]:
            continue
        for branch, (start, end) in enumerate(branches):
            if start <= pos < end:
                context[index] = branch
                break
    return context


def _mutually_exclusive(a: dict[int, int], b: dict[int, int]) -> bool:
    """Whether two positions are in sibling branches of a block."""
    return any(b.get(block, branch) != branch for block, branch in a.items())


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for orphans html tags.

    A tag left open when its parent closes is mis-nested and reported, as
    the `<b>` in `<h1>a <b>b</h1>`.

    Tags in sibling branches of a block are not orphans of each
    other: only one branch renders, so several opens share one close, and
    a close in another branch shares an open already matched.
    """
    open_tags: list[TagToken] = []
    orphan_tags: list[TagToken] = []
    p_child_tags: list[TagToken] = []
    matched_closes: list[TagToken] = []
    blocks = _branched_blocks(html)
    branch_contexts: dict[int, dict[int, int]] = {}

    def context(token: TagToken) -> dict[int, int]:
        cached = branch_contexts.get(token.start)
        if cached is None:
            cached = branch_contexts[token.start] = _branch_context(
                blocks, token.start
            )
        return cached

    for token in tokenize_tags(html):
        tag_name = token.name.lower()
        if (
            token.declaration
            or token.self_closing
            or tag_name in HTML_VOID_ELEMENTS
        ):
            continue

        in_unformatted_block = child_of_unformatted_block(config, html, token)
        if (
            (
                not in_unformatted_block
                and (
                    inside_ignored_block(config, html, token)
                    or inside_ignored_rule(config, html, token, rule["name"])
                )
            )
            or inside_ignored_linter_block(config, html, token)
            or inside_template_block(config, html, token)
        ):
            continue

        if not token.closing:
            if tag_name in P_LIST_CHILD_TAGS:
                for tag in open_tags:
                    if tag.name.lower() == "p":
                        p_child_tags.append(token)
                        break
            if any(
                tag.name.lower() == tag_name
                and _mutually_exclusive(context(tag), context(token))
                for tag in open_tags
            ):
                continue
            open_tags.insert(0, token)
        else:
            for i, tag in enumerate(open_tags):
                if tag.name.lower() != tag_name:
                    continue
                close_context = context(token)
                still_open: list[TagToken] = []
                for crossed in open_tags[:i]:
                    if context(crossed) == close_context:
                        orphan_tags.append(crossed)
                    else:
                        still_open.append(crossed)
                open_tags[: i + 1] = still_open
                matched_closes.append(token)
                break
            else:
                close_context = context(token)
                for j, matched in enumerate(matched_closes):
                    if matched.name.lower() == tag_name and _mutually_exclusive(
                        context(matched), close_context
                    ):
                        matched_closes[j] = token
                        break
                else:
                    orphan_tags.append(token)

    return tuple(
        {
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": rule["message"],
        }
        for token in chain(open_tags, orphan_tags)
        if (
            not overlaps_ignored_block(config, html, token)
            and not inside_ignored_rule(config, html, token, rule["name"])
            and not inside_ignored_linter_block(config, html, token)
        )
    ) + tuple(
        {
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": P_LIST_CHILD_MESSAGE,
        }
        for token in p_child_tags
        if (
            not overlaps_ignored_block(config, html, token)
            and not inside_ignored_rule(config, html, token, rule["name"])
            and not inside_ignored_linter_block(config, html, token)
        )
    )
