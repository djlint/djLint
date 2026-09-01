"""Djlint html linter."""

from __future__ import annotations

import importlib
from bisect import bisect_right
from collections.abc import Sequence
from operator import itemgetter
from types import MappingProxyType
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    inside_html_attribute,
    inside_ignored_linter_block,
    inside_ignored_rule,
    inside_template_block,
    overlaps_ignored_block,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path
    from typing import Any, Final

    from djlint.settings import Config
    from djlint.types import LintError


flags: Final = MappingProxyType({
    "re.A": re.A,
    "re.ASCII": re.ASCII,
    "re.I": re.I,
    "re.IGNORECASE": re.IGNORECASE,
    "re.M": re.M,
    "re.MULTILINE": re.MULTILINE,
    "re.S": re.S,
    "re.DOTALL": re.DOTALL,
    "re.X": re.X,
    "re.VERBOSE": re.VERBOSE,
    "re.L": re.L,
    "re.LOCALE": re.LOCALE,
})
_LINE_PATTERN: Final = re.compile(r"(?:.*\n)|(?:[^\n]+$)", cache_pattern=False)
_line_end: Final = itemgetter("end")


def build_flags(flag_list: str | int) -> int:
    """Build list of regex flags."""
    if isinstance(flag_list, int):
        return flag_list
    split_flags = flag_list.split("|")
    combined_flags = 0
    for flag in split_flags:
        combined_flags |= flags[flag.strip()]
    return combined_flags


def get_line(start: int, line_ends: Sequence[Mapping[str, int]]) -> str:
    """Get the line number and index of match."""
    if not line_ends:
        return f"1:{start}"
    index = min(
        bisect_right(line_ends, start, key=_line_end), len(line_ends) - 1
    )
    line = line_ends[index]

    return f"{index + 1}:{start - line['start']}"


def _is_html_inside_template_tag(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Whether the match is markup written inside a template tag.

    Html-like content in a template tag, such as a string argument, is not
    part of the document. Rules that target template syntax itself match
    starting at the tag delimiters, so they still apply.
    """
    return not match.group().startswith(("{%", "{{")) and inside_template_block(
        config, html, match
    )


def _is_reported(
    config: Config, html: str, match: re.Match[str], rule: Mapping[str, Any]
) -> bool:
    """Whether a pattern match is a finding rather than ignored content.

    A rule looking for a tag sets `skip_in_attributes`, because markup
    written inside an attribute value, as in `<p title="a<br>b">`, is text
    rather than a tag of its own.
    """
    if rule.get("skip_in_attributes") and inside_html_attribute(html, match):
        return False
    return (
        not overlaps_ignored_block(config, html, match)
        and not _is_html_inside_template_tag(config, html, match)
        and not inside_ignored_rule(config, html, match, rule["name"])
        and not inside_ignored_linter_block(config, html, match)
    )


def linter(
    config: Config, html: str, filename: str, filepath: str
) -> dict[str, list[LintError]]:
    """Lint a html string."""
    file_errors: list[LintError] = []
    line_ends = [
        {"start": m.start(), "end": m.end()}
        for m in _LINE_PATTERN.finditer(html)
    ]

    ignored_rules: set[str] = set()

    for pattern, rules in config.per_file_ignores.items():
        if re.search(pattern, filepath, flags=re.X):
            ignored_rules.update(x.strip() for x in rules.split(","))

    for rule in config.linter_rules:
        rule = rule["rule"]  # noqa: PLW2901

        if rule["name"] in ignored_rules:
            continue

        if "python_module" in rule:
            rule_module = importlib.import_module(rule["python_module"])
            module_errors = rule_module.run(
                rule=rule,
                config=config,
                html=html,
                filepath=filepath,
                line_ends=line_ends,
            )
            if not isinstance(module_errors, Sequence):
                msg = (
                    f"Error: {rule['name']} python_module run() should return"
                    " a sequence of dict with keys: code, line, match, message."
                )
                raise AssertionError(msg)
            file_errors.extend(module_errors)

        else:
            flags = build_flags(rule.get("flags", "re.S"))
            for pattern in rule["patterns"]:
                file_errors.extend(
                    {
                        "code": rule["name"],
                        "line": get_line(match.start(), line_ends),
                        "match": match.group().strip()[:20],
                        "message": rule["message"],
                    }
                    for match in re.finditer(pattern, html, flags=flags)
                    if _is_reported(config, html, match, rule)
                )

    seen: set[tuple[str, ...]] = set()
    unique_errors = []
    for error in file_errors:
        key = (error["code"], error["line"], error["match"], error["message"])
        if key not in seen:
            seen.add(key)
            unique_errors.append(error)
    return {filename: unique_errors}


def lint_file(config: Config, this_file: Path) -> dict[str, list[LintError]]:
    """Check file for formatting errors."""
    filename = str(this_file)

    html = this_file.read_text(encoding="utf-8")

    return linter(config, html, filename, this_file.as_posix())
