"""Djlint tests specific to custom file path.

run::

   pytest tests/test_config/test_config_pyproject/test.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_config_pyproject/test.py::test_check_pyproject_as_config

"""

import os

from click.testing import CliRunner

from src.djlint import main as djlint


def test_check_pyproject_as_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "-",
            "--check",
            "--configuration",
            "tests/test_config/test_config_pyproject/subfolder/pyproject.toml",
        ],
    )
    assert """Checking 2/2 files""" in result.output
