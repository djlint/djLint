"""Djlint tests specific to pyproject.toml configuration.

uv run pytest tests/test_config/test_profile/test_config.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint._cli import main as djlint  # noqa: PLC2701
from djlint.settings import Config

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


def test_profile(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_config/test_profile/html.html"))

    assert "T001" in result.output
    assert "J018" not in result.output
    assert "D018" in result.output

    result = runner.invoke(
        djlint, ("tests/test_config/test_profile/html.html", "--profile", "jinja")
    )
    assert "T001" in result.output
    assert "J018" in result.output
    assert "D018" not in result.output

    result = runner.invoke(
        djlint, ("tests/test_config/test_profile/html.html", "--profile", "handlebars")
    )
    assert "T001" not in result.output
    assert "J018" not in result.output
    assert "D018" not in result.output

    result = runner.invoke(
        djlint, ("tests/test_config/test_profile/html.html", "--check", "--profile", "handlebars")
    )

    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ("tests/test_config/test_profile/html.html", "--check", "--profile", "jinja")
    )
    assert result.exit_code == 1
    assert (
        """-{{test}}
+{{ test }}"""
        in result.output
    )


@pytest.mark.parametrize(
    ("profile", "include", "rule", "runs"),
    [
        pytest.param(None, "", "T003", False, id="no profile leaves T rules out"),
        pytest.param(None, "T003", "T003", True, id="include runs T003 without a profile"),
        pytest.param("html", "T003", "T003", True, id="include beats the html profile"),
        pytest.param(
            "angular", "H012", "H012", False, id="include never beats a code the profile names"
        ),
        pytest.param(None, "T028", "T028", True, id="include runs T028 without a profile"),
        pytest.param("all", "", "T028", False, id="all leaves out a rule excluded anywhere"),
        pytest.param("all", "T028", "T028", True, id="include beats all leaving a rule out"),
        pytest.param("django", "T028", "T028", False, id="include never beats the rule's exclude"),
    ],
)
def test_include_turns_on_a_rule_the_profile_leaves_out(
    profile: str | None, include: str, rule: str, *, runs: bool
) -> None:
    config = Config("dummy/source.html", profile=profile, include=include)

    assert (rule in {x["rule"]["name"] for x in config.linter_rules}) is runs


@pytest.mark.parametrize(
    ("profile", "runs"),
    [
        pytest.param(None, True, id="no profile lints as html"),
        pytest.param("html", True, id="html"),
        pytest.param("all", False, id="all leaves it out"),
        pytest.param("django", False, id="the profile it excludes"),
    ],
)
def test_no_profile_picks_the_rules_html_does(
    tmp_path: Path, profile: str | None, *, runs: bool
) -> None:
    rules = tmp_path / ".djlint_rules.yaml"
    rules.write_text(
        """- rule:
    name: C001
    message: x
    exclude:
      - django
    patterns:
      - x
""",
        encoding="utf-8",
    )
    config = Config(str(tmp_path / "a.html"), profile=profile, rules=rules)

    assert ("C001" in {x["rule"]["name"] for x in config.linter_rules}) is runs
