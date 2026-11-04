"""Djlint tests specific to custom file path.

uv run pytest tests/test_config/test_config_pyproject/test_config_pyproject.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_check_pyproject_as_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--check",
            "--configuration",
            "tests/test_config/test_config_pyproject/subfolder/pyproject.toml",
        ),
    )
    assert """Checking 2/2 files""" in result.output
