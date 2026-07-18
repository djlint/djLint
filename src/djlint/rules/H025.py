"""rule H025: Check for orphans html tags."""

from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

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
            open_tags.insert(0, token)
        else:
            for i, tag in enumerate(open_tags):
                if tag.name.lower() == tag_name:
                    open_tags.pop(i)
                    break
            else:
                # there was no open tag matching the close tag
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
