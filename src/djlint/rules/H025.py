"""rule H025: Check for orphans html tags."""

from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IX,
    child_of_unformatted_block,
    inside_ignored_block,
    inside_ignored_linter_block,
    inside_ignored_rule,
    inside_template_block,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


P_LIST_CHILD_MESSAGE = "List tags should not be nested inside p tags."
P_LIST_CHILD_TAGS = frozenset(("ol", "ul"))


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
    open_tags: list[re.Match[str]] = []
    orphan_tags: list[re.Match[str]] = []
    p_child_tags: list[re.Match[str]] = []

    html_tag_pattern = re.compile(
        r"<(/?(\w+))\s*(" + config.attribute_pattern + r"|\s*)*\s*/?>", re.X
    )
    void_tag_pattern = re.compile(
        rf"^/?{config.always_self_closing_html_tags}\b", RE_FLAGS_IX
    )

    for match in html_tag_pattern.finditer(html):
        if match.group().rstrip().endswith("/>") or void_tag_pattern.search(
            match.group(1)
        ):
            continue

        in_unformatted_block = child_of_unformatted_block(config, html, match)
        if (
            (
                not in_unformatted_block
                and (
                    inside_ignored_block(config, html, match)
                    or inside_ignored_rule(config, html, match, rule["name"])
                )
            )
            or inside_ignored_linter_block(config, html, match)
            or inside_template_block(config, html, match)
        ):
            continue

        # close tags should equal open tags
        if match.group(1)[0] != "/":
            if match.group(2) in P_LIST_CHILD_TAGS and any(
                tag.group(2) == "p" for tag in open_tags
            ):
                p_child_tags.append(match)
            open_tags.insert(0, match)
        else:
            for i, tag in enumerate(open_tags):
                if tag.group(2) == match.group(1)[1:]:
                    open_tags.pop(i)
                    break
            else:
                # there was no open tag matching the close tag
                orphan_tags.append(match)

    return tuple(
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in chain(open_tags, orphan_tags)
        if (
            not overlaps_ignored_block(config, html, match)
            and not inside_ignored_rule(config, html, match, rule["name"])
            and not inside_ignored_linter_block(config, html, match)
        )
    ) + tuple(
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": P_LIST_CHILD_MESSAGE,
        }
        for match in p_child_tags
        if (
            not overlaps_ignored_block(config, html, match)
            and not inside_ignored_rule(config, html, match, rule["name"])
            and not inside_ignored_linter_block(config, html, match)
        )
    )
