"""Write findings as a SARIF 2.1.0 document.

SARIF is the format GitHub code scanning, Azure DevOps and most editors
take findings in, so a run can be uploaded and shown in the Security tab
with history rather than only as annotations on one pull request.
"""

from __future__ import annotations

import json
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING

from click import echo

from djlint.output import (
    build_relative_path,
    count_format_errors,
    finding_position,
    first_filename,
    report_on_stderr,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from typing import Any, Final

    from djlint.settings import Config
    from djlint.types import LintError, ProcessResult

_SCHEMA: Final = "https://json.schemastore.org/sarif-2.1.0.json"
_DOCS: Final = "https://djlint.com/docs/linter/"
_FORMATTING_RULE: Final = "formatting"


def _artifact(filename: str, config: Config) -> dict[str, Any]:
    if config.stdin:
        return {"uri": "stdin"}
    relative = build_relative_path(filename, config.project_root)
    return {"uri": Path(relative).as_posix()}


def _lint_results(
    error: Mapping[str, Sequence[LintError]],
    config: Config,
    rule_index: Mapping[str, int],
) -> list[dict[str, Any]]:
    filename = next(iter(error))
    artifact = _artifact(filename, config)
    results = []
    for finding in sorted(next(iter(error.values())), key=finding_position):
        line, column = finding_position(finding)
        code = finding["code"]
        results.append({
            "ruleId": code,
            "ruleIndex": rule_index[code],
            "level": "error" if code.startswith("E") else "warning",
            "message": {"text": finding["message"]},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": artifact,
                        "region": {
                            "startLine": line,
                            "startColumn": column + 1,
                        },
                    }
                }
            ],
        })
    return results


def _format_result(
    errors: Mapping[str, Sequence[str]], config: Config, rule_index: int
) -> dict[str, Any]:
    return {
        "ruleId": _FORMATTING_RULE,
        "ruleIndex": rule_index,
        "level": "error",
        "message": {"text": "Formatting changes required."},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": _artifact(next(iter(errors)), config)
                }
            }
        ],
    }


def build_sarif(
    config: Config, file_errors: Sequence[ProcessResult]
) -> tuple[dict[str, Any], int]:
    """Build the SARIF document and count the findings it holds."""
    rules: list[dict[str, Any]] = []
    rule_index: dict[str, int] = {}
    for entry in config.linter_rules:
        rule = entry["rule"]
        rule_index[rule["name"]] = len(rules)
        rules.append({
            "id": rule["name"],
            "shortDescription": {"text": rule["message"]},
            "helpUri": f"{_DOCS}#{rule['name'].lower()}",
        })

    results: list[dict[str, Any]] = []
    count = 0
    for error in sorted(file_errors, key=first_filename):
        if lint := error.get("lint_message"):
            found = _lint_results(lint, config, rule_index)
            results.extend(found)
            count += len(found)
        if (formatting := error.get("format_message")) and next(
            iter(formatting.values())
        ):
            if _FORMATTING_RULE not in rule_index:
                rule_index[_FORMATTING_RULE] = len(rules)
                rules.append({
                    "id": _FORMATTING_RULE,
                    "shortDescription": {"text": "File would be reformatted."},
                    "helpUri": "https://djlint.com/docs/formatter/",
                })
            results.append(
                _format_result(formatting, config, rule_index[_FORMATTING_RULE])
            )
            count += count_format_errors(formatting)

    document = {
        "$schema": _SCHEMA,
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "djLint",
                        "version": version("djlint"),
                        "informationUri": "https://djlint.com",
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }
    return document, count


def print_sarif_output(
    config: Config, file_errors: Sequence[ProcessResult], _file_count: int
) -> int:
    """Print the SARIF document and return how many findings it holds."""
    document, count = build_sarif(config, file_errors)
    echo(json.dumps(document, indent=2), err=report_on_stderr(config))
    return count
