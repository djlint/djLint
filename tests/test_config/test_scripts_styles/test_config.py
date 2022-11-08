"""Djlint tests specific to .djlintrc configuration.

run::

   pytest tests/test_config/test_scripts_styles/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_scripts_styles/test_config.py::test_ignore

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_scripts_styles/html.html",
            "--check",
        ],
    )
    assert result.exit_code == 0


def test_ignore(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_scripts_styles/ignore.html",
            "--check",
        ],
    )
    assert result.exit_code == 0


def text_blank_lines(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_scripts_styles/blank_lines.html",
            "--check",
        ],
    )
    assert result.exit_code == 0
