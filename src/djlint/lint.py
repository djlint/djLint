"""Djlint html linter."""
import importlib
from pathlib import Path
from typing import Dict, List

import regex as re

from .helpers import (
    inside_ignored_linter_block,
    inside_ignored_rule,
    overlaps_ignored_block,
)
from .settings import Config

flags = {
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
}


def build_flags(flag_list: str) -> int:
    """Build list of regex flags."""
    split_flags = flag_list.split("|")

    combined_flags = 0
    for flag in split_flags:
        combined_flags |= flags[flag.strip()]
    return combined_flags


def get_line(start: int, line_ends: List) -> str:
    """Get the line number and index of match."""
    line = list(filter(lambda pair: pair["end"] > start, line_ends))[0]

    # pylint: disable=C0209
    return "%d:%d" % (line_ends.index(line) + 1, start - line["start"])


def linter(config: Config, html: str, filename: str, filepath: str) -> Dict:
    """Lint a html string."""
    errors: dict = {filename: []}
    # build list of line ends for file
    line_ends = [
        {"start": m.start(), "end": m.end()}
        for m in re.finditer(r"(?:.*\n)|(?:[^\n]+$)", html)
    ]

    ignored_rules: List[str] = []

    # remove ignored rules for file
    for pattern, rules in config.per_file_ignores.items():
        if re.search(pattern, filepath, re.VERBOSE):
            ignored_rules += [x.strip() for x in rules.split(",")]

    for rule in config.linter_rules:
        rule = rule["rule"]

        # skip ignored rules
        if rule["name"] in ignored_rules:
            continue

        # rule based on python module
        if "python_module" in rule:
            rule_module = importlib.import_module(rule["python_module"])
            module_errors = rule_module.run(
                rule=rule,
                config=config,
                html=html,
                filepath=filepath,
                line_ends=line_ends,
            )
            assert isinstance(module_errors, list), (
                f"Error: {rule['name']} python_module run() should return a list of "
                "dict with keys: code, line, match, message."
            )
            errors[filename].extend(module_errors)

        # rule based on patterns
        else:
            for pattern in rule["patterns"]:
                for match in re.finditer(
                    re.compile(
                        pattern, flags=build_flags(rule.get("flags", "re.DOTALL"))
                    ),
                    html,
                ):
                    if (
                        overlaps_ignored_block(config, html, match) is False
                        and inside_ignored_rule(config, html, match, rule["name"])
                        is False
                        and inside_ignored_linter_block(config, html, match) is False
                    ):
                        errors[filename].append(
                            {
                                "code": rule["name"],
                                "line": get_line(match.start(), line_ends),
                                "match": match.group().strip()[:20],
                                "message": rule["message"],
                            }
                        )

    # remove duplicate matches
    for filename, error_dict in errors.items():
        unique_errors = []
        for dict_ in error_dict:
            if dict_ not in unique_errors:
                unique_errors.append(dict_)
        errors[filename] = unique_errors
    return errors


def lint_file(config: Config, this_file: Path) -> Dict:
    """Check file for formatting errors."""
    filename = str(this_file)

    html = this_file.read_text(encoding="utf8")

    return linter(config, html, filename, this_file.as_posix())
