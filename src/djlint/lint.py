"""Djlint html linter."""
import re
from pathlib import Path

import yaml

rules = yaml.load(
    (Path(__file__).parent / "rules.yaml").read_text(encoding="utf8"),
    Loader=yaml.SafeLoader,
)


def get_line(start, line_ends):
    """Get the line number and index of match."""
    line = list(filter(lambda pair: pair["end"] > start, line_ends))[0]

    return "%d:%d" % (line_ends.index(line) + 1, start - line["start"])


def lint_file(this_file: Path):
    """Check file for formatting errors."""
    file_name = str(this_file)
    errors: dict = {file_name: []}
    html = this_file.read_text(encoding="utf8")

    # build list of line ends for file
    line_ends = [
        {"start": m.start(), "end": m.end()}
        for m in re.finditer(r"(?:.*\n)|(?:[^\n]+$)", html)
    ]

    for rule in rules:
        rule = rule["rule"]

        for pattern in rule["patterns"]:
            for match in re.finditer(pattern, html, re.DOTALL):
                errors[file_name].append(
                    {
                        "code": rule["name"],
                        "line": get_line(match.start(), line_ends),
                        "match": match.group()[:20].strip(),
                        "message": rule["message"],
                    }
                )

    return errors
