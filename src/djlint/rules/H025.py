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

_CONDITIONAL_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*(endif|elseif|elif|else|if)\b", cache_pattern=False
)


def _conditional_branches(html: str) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Branch spans of every complete {% if %}...{% endif %} block."""
    complete: list[tuple[tuple[int, int], ...]] = []
    open_blocks: list[tuple[list[tuple[int, int]], int]] = []
    for match in _CONDITIONAL_PATTERN.finditer(html):
        keyword = match.group(1)
        if keyword == "if":
            open_blocks.append(([], match.end()))
        elif not open_blocks:
            continue
        elif keyword == "endif":
            branches, start = open_blocks.pop()
            branches.append((start, match.start()))
            complete.append(tuple(branches))
        else:
            branches, start = open_blocks[-1]
            branches.append((start, match.start()))
            open_blocks[-1] = (branches, match.end())
    return tuple(complete)


def _branch_context(
    conditionals: tuple[tuple[tuple[int, int], ...], ...], pos: int
) -> dict[int, int]:
    """Map each conditional containing pos to the branch pos is in."""
    return {
        index: branch
        for index, branches in enumerate(conditionals)
        for branch, (start, end) in enumerate(branches)
        if start <= pos < end
    }


def _mutually_exclusive(a: dict[int, int], b: dict[int, int]) -> bool:
    """Whether two positions are in sibling branches of a conditional."""
    return any(b.get(cond, branch) != branch for cond, branch in a.items())


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check for orphans html tags."""
    open_tags: list[TagToken] = []
    orphan_tags: list[TagToken] = []
    p_child_tags: list[TagToken] = []
    matched_closes: list[TagToken] = []
    conditionals = _conditional_branches(html)

    def context(token: TagToken) -> dict[int, int]:
        return _branch_context(conditionals, token.start)

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

        # close tags should equal open tags
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
                # the same tag opened in a sibling branch of a conditional;
                # only one branch renders, so they share one close tag.
                continue
            open_tags.insert(0, token)
        else:
            for i, tag in enumerate(open_tags):
                if tag.name.lower() != tag_name:
                    continue
                close_context = context(token)
                remaining: list[TagToken] = []
                for crossed in open_tags[:i]:
                    if context(crossed) == close_context:
                        # opened after the tag being closed but not closed
                        # inside it, e.g. <h1>a <b>b</h1>: mis-nested.
                        orphan_tags.append(crossed)
                    else:
                        remaining.append(crossed)
                open_tags[: i + 1] = remaining
                matched_closes.append(token)
                break
            else:
                # no open tag matches the close tag; a close tag in a
                # sibling branch of a conditional may share the open tag.
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
