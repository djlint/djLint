"""Djlint tests specific to pyproject.toml configuration.

uv run pytest tests/test_config/test_excludes/test_config.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_exclude(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_excludes", "--profile", "django")
    )
    print(result.output)
    assert """html.html""" in result.output
    assert """excluded.html""" not in result.output
    assert """foo/excluded.html""" not in result.output
    assert result.exit_code == 1
