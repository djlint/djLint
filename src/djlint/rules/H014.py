"""Rule H014: Check for more blank lines than the configuration keeps."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Final

    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError

# a run of lines holding nothing but whitespace, anchored so the report
# points at the first of them rather than at the content line above
_BLANK_LINES_PATTERN: Final = re.compile(
    r"(?:(?<=\n)|\A)(?:[ \t]*\n)+", cache_pattern=False
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
    """Check for more blank lines than the configuration keeps.

    `--preserve-blank-lines` asks for every one of them, so nothing is
    reported under it. Otherwise the run has to be longer than
    `max_blank_lines`, which is what `--reformat` would collapse it to, so
    the linter never rejects the formatter's own output. One blank line is
    a paragraph break rather than an extra, so it is left alone even where
    the formatter would drop it.
    """
    if config.preserve_blank_lines:
        return ()

    keep = max(config.max_blank_lines, 1)
    errors: list[LintError] = []
    for match in _BLANK_LINES_PATTERN.finditer(html):
        if match.group().count("\n") <= keep:
            continue

        if (
            overlaps_ignored_block(config, html, match)
            or inside_ignored_rule(config, html, match, rule["name"])
            or inside_ignored_linter_block(config, html, match)
        ):
            continue

        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": "",
            "message": rule["message"],
        })
    return tuple(errors)
