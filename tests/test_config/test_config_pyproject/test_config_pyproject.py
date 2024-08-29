"""Djlint tests specific to custom file path.

run::

   pytest tests/test_config/test_config_pyproject/test.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_config_pyproject/test.py::test_check_pyproject_as_config

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
