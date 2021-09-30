"""Djlint html linter."""
from pathlib import Path
from typing import Dict, List

import regex as re
import yaml

from .settings import Config

rules = yaml.load(
    (Path(__file__).parent / "rules.yaml").read_text(encoding="utf8"),
    Loader=yaml.SafeLoader,
)
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


def lint_file(config: Config, this_file: Path) -> Dict:
    """Check file for formatting errors."""
    file_name = str(this_file)
    errors: dict = {file_name: []}
    html = this_file.read_text(encoding="utf8")

    # build list of line ends for file
    line_ends = [
        {"start": m.start(), "end": m.end()}
        for m in re.finditer(r"(?:.*\n)|(?:[^\n]+$)", html)
    ]

    for rule in list(
        filter(
            lambda x: x["rule"]["name"] not in config.ignore.split(",")
            and x["rule"]["name"][0] not in config.profile_code
            and config.profile not in x["rule"].get("exclude", []),
            rules,
        )
    ):
        rule = rule["rule"]

        for pattern in rule["patterns"]:

            for match in re.finditer(
                pattern, html, flags=build_flags(rule.get("flags", "re.DOTALL"))
            ):
                errors[file_name].append(
                    {
                        "code": rule["name"],
                        "line": get_line(match.start(), line_ends),
                        "match": match.group()[:20].strip(),
                        "message": rule["message"],
                    }
                )

    # remove duplicate matches
    for file_name, error_dict in errors.items():
        unique_errors = []
        for dict_ in error_dict:
            if dict_ not in unique_errors:
                unique_errors.append(dict_)
        errors[file_name] = unique_errors
    return errors
