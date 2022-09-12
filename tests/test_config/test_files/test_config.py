"""Djlint tests specific to custom file path.

run::

   pytest tests/test_config/test_files/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_files/test_config.py::test_check_custom_file_src

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_check_custom_file_src(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "-",
            "--check",
            "--configuration",
            "tests/test_config/test_files/.djlintrc",
        ],
    )
    assert """Checking 2/2 files""" in result.output


def test_lint_custom_file_src(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "-",
            "--lint",
            "--configuration",
            "tests/test_config/test_files/.djlintrc",
        ],
    )
    assert """Linting 2/2 files""" in result.output


def test_reformat_custom_file_src(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "-",
            "--reformat",
            "--configuration",
            "tests/test_config/test_files/.djlintrc",
        ],
    )
    assert """Reformatting 2/2 files""" in result.output
