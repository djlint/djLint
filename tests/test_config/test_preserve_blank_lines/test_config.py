"""Djlint tests specific to --preserve-leading-space option.

run::

   pytest tests/test_config/test_preserve_blank_lines/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_preserve_blank_lines/test_config.py::test_whitespace

"""
# pylint: disable=C0116
from click.testing import CliRunner

from src.djlint import main as djlint


def test_config(runner: CliRunner) -> None:

    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_preserve_blank_lines/html.html",
            "--check",
            "--preserve-leading-space",
            "--preserve-blank-lines",
        ],
    )

    assert result.exit_code == 0


def test_whitespace(runner: CliRunner) -> None:
    # blank line should not be added before template tags
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_preserve_blank_lines/html_one.html",
            "--check",
            "--preserve-blank-lines",
        ],
    )

    assert result.exit_code == 0

    # blank line should not be added before html tags
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_preserve_blank_lines/html_two.html",
            "--check",
            "--preserve-blank-lines",
        ],
    )
    print(result.output)
    assert result.exit_code == 0
