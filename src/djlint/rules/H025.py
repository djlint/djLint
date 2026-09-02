"""rule H025: Check for orphans html tags."""

from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

from djlint.const import HTML_VOID_ELEMENTS
from djlint.helpers import (
    branch_context,
    branched_blocks,
    child_of_unformatted_block,
    inside_ignored_linter_block,
    inside_ignored_rule,
    inside_template_block,
    mutually_exclusive,
    overlaps_ignored_block,
    tokenize_markup,
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
    blocks = branched_blocks(html)
    branch_contexts: dict[int, dict[int, int]] = {}

    def context(token: TagToken) -> dict[int, int]:
        cached = branch_contexts.get(token.start)
        if cached is None:
            cached = branch_contexts[token.start] = branch_context(
                blocks, token.start
            )
        return cached

    for token in tokenize_markup(html):
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
                    overlaps_ignored_block(config, html, token)
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
                and mutually_exclusive(context(tag), context(token))
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
                    if matched.name.lower() == tag_name and mutually_exclusive(
                        context(matched), close_context
                    ):
                        matched_closes[j] = token
                        break
                else:
                    orphan_tags.append(token)

    def reportable(token: TagToken) -> bool:
        return (
            not overlaps_ignored_block(config, html, token)
            and not inside_ignored_rule(config, html, token, rule["name"])
            and not inside_ignored_linter_block(config, html, token)
        )

    def error(token: TagToken, message: str) -> LintError:
        return {
            "code": rule["name"],
            "line": get_line(token.start, line_ends),
            "match": html[token.start : token.end].strip()[:20],
            "message": message,
        }

    return tuple(
        error(token, rule["message"])
        for token in chain(open_tags, orphan_tags)
        if reportable(token)
    ) + tuple(
        error(token, P_LIST_CHILD_MESSAGE)
        for token in p_child_tags
        if reportable(token)
    )
