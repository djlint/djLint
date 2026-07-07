"""Rule T003: Check Django/Jinja block names."""

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
    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


BLOCK_RE = re.compile(
    r"{%-?\s*(?P<closing>end)?block(?!trans)\b"
    r"(?:\s+(?P<name>[^\s%-][^\s%]*))?"
    r"(?:(?!%}).)*?-?%}",
    flags=re.I | re.S,
)
MISMATCH_MESSAGE = "Endblock name should match opening block name."
MISSING_OPEN_MESSAGE = "Endblock should have matching block."
MISSING_CLOSE_MESSAGE = "Block should have matching endblock."


def _ignored(
    rule: dict[str, Any], config: Config, html: str, match: re.Match[str]
) -> bool:
    return (
        overlaps_ignored_block(config, html, match)
        or inside_ignored_rule(config, html, match, rule["name"])
        or inside_ignored_linter_block(config, html, match)
    )


def _error(
    rule: dict[str, Any],
    match: re.Match[str],
    line_ends: list[dict[str, int]],
    message: str,
) -> LintError:
    return {
        "code": rule["name"],
        "line": get_line(match.start(), line_ends),
        "match": match.group().strip()[:20],
        "message": message,
    }


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Check block/endblock names."""
    errors: list[LintError] = []
    open_blocks: list[tuple[str, re.Match[str]]] = []

    for match in BLOCK_RE.finditer(html):
        if _ignored(rule, config, html, match):
            continue

        name = match.group("name")
        if not match.group("closing"):
            if name:
                open_blocks.append((name, match))
            continue

        if not name:
            errors.append(_error(rule, match, line_ends, rule["message"]))
            if open_blocks:
                open_blocks.pop()
            continue

        if not open_blocks:
            errors.append(_error(rule, match, line_ends, MISSING_OPEN_MESSAGE))
            continue

        open_name, _ = open_blocks.pop()
        if name != open_name:
            errors.append(_error(rule, match, line_ends, MISMATCH_MESSAGE))

    errors.extend(
        _error(rule, match, line_ends, MISSING_CLOSE_MESSAGE)
        for _, match in open_blocks
    )
    return tuple(errors)
