"""Test the SARIF output.

uv run pytest tests/test_sarif_output.py
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from click.testing import CliRunner


def _document(output: str) -> dict[str, Any]:
    document: dict[str, Any] = json.loads(output)
    assert document["version"] == "2.1.0"
    assert document["$schema"].endswith("sarif-2.1.0.json")
    assert len(document["runs"]) == 1
    return document


def test_lint_finding_is_a_result(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("-", "--lint", "--sarif"), input="<div></div>"
    )
    assert result.exit_code == 1

    run = _document(result.output)["runs"][0]
    assert run["tool"]["driver"]["name"] == "djLint"
    assert run["tool"]["driver"]["version"]

    (finding,) = [r for r in run["results"] if r["ruleId"] == "H020"]
    assert finding["level"] == "warning"
    assert finding["message"]["text"]
    location = finding["locations"][0]["physicalLocation"]
    assert location["artifactLocation"] == {"uri": "stdin"}
    assert location["region"] == {"startLine": 1, "startColumn": 1}

    rule = run["tool"]["driver"]["rules"][finding["ruleIndex"]]
    assert rule["id"] == "H020"
    assert rule["helpUri"] == "https://djlint.com/docs/linter/#h020"


def test_every_enabled_rule_is_listed(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ("-", "--lint", "--sarif", "--profile", "django"),
        input="<p>x</p>",
    )

    run = _document(result.output)["runs"][0]
    ids = {rule["id"] for rule in run["tool"]["driver"]["rules"]}
    assert {"H005", "H020", "T001"} <= ids
    assert all(
        rule["shortDescription"]["text"]
        for rule in run["tool"]["driver"]["rules"]
    )


def test_clean_input_has_no_results(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("-", "--lint", "--sarif"), input="<p>x</p>\n"
    )
    assert result.exit_code == 0
    assert _document(result.output)["runs"][0]["results"] == []


def test_file_needing_formatting_is_a_result(
    runner: CliRunner, tmp_path: Path
) -> None:
    page = tmp_path / "page.html"
    page.write_text("<div><p>x</p></div>\n", encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--check", "--sarif"))
    assert result.exit_code == 1

    run = _document(result.output)["runs"][0]
    (finding,) = run["results"]
    assert finding["ruleId"] == "formatting"
    assert finding["level"] == "error"
    uri = finding["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
    assert uri.endswith("page.html")
    assert "\\" not in uri
    assert "region" not in finding["locations"][0]["physicalLocation"]
    assert (
        run["tool"]["driver"]["rules"][finding["ruleIndex"]]["id"]
        == "formatting"
    )


def test_statistics_do_not_break_the_document(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("-", "--lint", "--sarif", "--statistics"), input="<div></div>"
    )
    _document(result.output)


def test_document_keeps_off_stdout_while_it_carries_the_file(
    runner: CliRunner,
) -> None:
    result = runner.invoke(
        djlint,
        ("-", "--reformat", "--lint", "--sarif"),
        input="<div><p>x</p></div>",
    )
    assert result.stdout.startswith("<div>")
    _document(result.stderr)
