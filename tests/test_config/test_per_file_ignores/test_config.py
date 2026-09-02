"""Djlint tests specific to pyproject.toml configuration.

uv run pytest tests/test_config/test_per_file_ignores/test_config.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_config/test_per_file_ignores"))
    assert "H025" not in result.output
    assert "H020" in result.output
