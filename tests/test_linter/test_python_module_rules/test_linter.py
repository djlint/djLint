"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_linter/test_python_module_rules/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_custom_rules(runner: CliRunner) -> None:
    """Test that our python_module is properly loaded and run."""
    result = runner.invoke(
        djlint,
        ("tests/test_linter/test_python_module_rules/", "--profile", "django"),
    )
    print(result.output)
    assert """Linting""" in result.output
    assert """2/2""" in result.output
    assert """T001 2:4""" in result.output
    assert """Linted 2 files, found 1 error.""" in result.output
    assert result.exit_code == 1
