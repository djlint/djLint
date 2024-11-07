"""rule H025: Check for orphans html tags."""

from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING

import regex as re

from djlint import regex_utils
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
    regex_str = r"<(/?(\w+))\s*(" + config.attribute_pattern + r"|\s*)*\s*?>"
    for match in regex_utils.finditer(regex_str, html, flags=re.X):
        if match.group(1) and not regex_utils.search(
            rf"^/?{config.always_self_closing_html_tags}\b",
            match.group(1),
            flags=RE_FLAGS_IX,
        ):
            # close tags should equal open tags
            if match.group(1)[0] != "/":
                open_tags.insert(0, match)
            else:
                to_pop: int | None = None
                for i, tag in enumerate(open_tags):
                    if tag.group(2) == match.group(1)[1:]:
                        to_pop = i
                        break
                if to_pop is None:
                    # there was no open tag matching the close tag
                    orphan_tags.append(match)
                else:
                    open_tags.pop(to_pop)

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
    )
