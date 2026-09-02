"""Djlint tests specific to pyproject.toml configuration.

uv run pytest tests/test_linter/test_custom_rules_bad/test_linter.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_custom_rules_bad_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ("tests/test_linter/test_custom_rules_bad", "--profile", "django"),
    )
    assert """Linting""" in result.output
    assert """1/1""" in result.output
    assert """T001 1:""" in result.output
    assert result.exit_code == 1
