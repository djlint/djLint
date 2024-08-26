"""Djlint tests specific to custom file path.

run::

   pytest tests/test_config/test_files/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_files/test_config.py::test_global_override

"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from src.djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_check_custom_file_src(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--check",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
        ),
    )
    assert """Checking 2/2 files""" in result.output


def test_lint_custom_file_src(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
        ),
    )
    assert """Linting 2/2 files""" in result.output


def test_reformat_custom_file_src(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--reformat",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
        ),
    )
    assert """Reformatting 2/2 files""" in result.output


def test_global_override(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
        ),
    )
    # fails
    assert result.exit_code == 1

    # check cli override
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
            "--ignore",
            "H025,H020",
        ),
    )
    # passes
    assert result.exit_code == 0

    # check project settings override

    # create project settings folder
    # add a gitignore file
    djlintrc_path = Path("tests", "test_config", "test_files", ".djlintrc")
    djlintrc_path.write_text('{ "ignore":"H025"}', encoding="utf-8")

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_files/test_two.html",
            "--lint",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
        ),
    )

    result_two = runner.invoke(
        djlint,
        (
            "tests/test_config/test_files/test.html",
            "--lint",
            "--configuration",
            "tests/test_config/test_files/.djlintrc_global",
        ),
    )
    try:
        djlintrc_path.unlink()
    except Exception as e:
        print("cleanup failed")
        print(e)

    # H025 should be ignored, but H022 not
    assert "H025" not in result.output
    assert "H020" in result_two.output
