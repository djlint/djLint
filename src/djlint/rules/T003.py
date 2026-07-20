"""Rule T003: Check Django/Jinja block names."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IS,
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


_BLOCK_PATTERN: Final = re.compile(
    r"{%-?\s*(?P<closing>end)?block(?!trans)\b"
    r"(?:\s+(?P<name>[^\s%-][^\s%]*))?"
    r"(?:(?!%}).)*?-?%}",
    RE_FLAGS_IS,
    cache_pattern=False,
)
# pairing and name-mismatch correctness is checked by T038; this rule
# only enforces the style demand that a multi-line endblock is named


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

    for match in _BLOCK_PATTERN.finditer(html):
        if _ignored(rule, config, html, match):
            continue

        name = match.group("name")
        if not match.group("closing"):
            if name:
                open_blocks.append((name, match))
            continue

        if not name:
            if open_blocks:
                _, open_match = open_blocks.pop()
                if "\n" not in html[open_match.end() : match.start()]:
                    # {% block foo %}{% endblock %} on one line is what the
                    # formatter produces; don't require a name here.
                    continue
            errors.append(_error(rule, match, line_ends, rule["message"]))
            continue

        if open_blocks:
            open_blocks.pop()

    return tuple(errors)
