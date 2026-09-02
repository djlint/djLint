"""Djlint tests specific to pyproject.toml configuration.

uv run pytest tests/test_config/test_extension/test_config.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_extension(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_extension", "--check")
    )
    assert """Checking""" in result.output
    assert """1/1""" in result.output
    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0


def test_progress_uses_stderr(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_extension", "--check")
    )
    assert "Checking 1/1 files" in result.stderr
    assert "Checking 1/1 files" not in result.stdout
    assert "0 files would be updated." in result.stdout


def test_no_color(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ("tests/test_config/test_extension", "--check"),
        color=True,
        env={"NO_COLOR": "1"},
    )
    assert "\x1b[" not in result.output


def test_color(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_extension", "--check"), color=True
    )
    assert "\x1b[" in result.output
