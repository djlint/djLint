"""Rewrites that clear a lint finding.

Each fixer is keyed by the rule it satisfies and runs only while that rule is
enabled, so `--ignore=H023` turns off both the report and the rewrite and a
project that disagrees with a rule is not formatted into obeying it.
"""

from __future__ import annotations

from html import unescape
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import inside_ignored_block
from djlint.lint import build_flags

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Final

    from djlint.settings import Config


def _rule_pattern(rule: dict[str, Any]) -> re.Pattern[str]:
    """Compile a pattern rule the way the linter does."""
    return re.compile(
        rule["patterns"][0], build_flags(rule.get("flags", "re.S"))
    )


def _write_entities_as_characters(
    html: str, config: Config, rule: dict[str, Any]
) -> str:
    """Replace an entity reference with the character it names (H023).

    Only what the rule reports is rewritten, and the entities it allows are
    exactly the ones that must survive: `&lt;`, `&amp;` and the rest carry
    syntax, and the invisible ones cannot be written as a literal. An
    entity naming nothing, such as the misspelled `&mdsah;`, is left as
    written for the rule to go on reporting.
    """

    def replace(match: re.Match[str]) -> str:
        if inside_ignored_block(config, html, match):
            return match.group()
        character = unescape(match.group())
        return match.group() if character == match.group() else character

    return _rule_pattern(rule).sub(replace, html)


_FIXERS: Final[dict[str, Callable[[str, Config, dict[str, Any]], str]]] = {
    "H023": _write_entities_as_characters
}


def apply_autofixes(html: str, config: Config) -> str:
    """Apply every fixer whose rule is enabled."""
    for entry in config.linter_rules:
        rule = entry["rule"]
        fixer = _FIXERS.get(rule["name"])
        if fixer is not None and "patterns" in rule:
            html = fixer(html, config, rule)
    return html
