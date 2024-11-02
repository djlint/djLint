"""Djlint tests specific to custom file path.

run::

   pytest tests/test_config/test_files/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_files/test_config.py::test_global_override

"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


@pytest.mark.parametrize(
    "config_path", [".djlintrc_global", "djlint_toml_global.toml"]
)
def test_check_custom_file_src(runner: CliRunner, config_path: str) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--check",
            "--configuration",
            f"tests/test_config/test_files/{config_path}",
        ),
    )
    assert """Checking 2/2 files""" in result.output


@pytest.mark.parametrize(
    "config_path", [".djlintrc_global", "djlint_toml_global.toml"]
)
def test_lint_custom_file_src(runner: CliRunner, config_path: str) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--configuration",
            f"tests/test_config/test_files/{config_path}",
        ),
    )
    assert """Linting 2/2 files""" in result.output


@pytest.mark.parametrize(
    "config_path", [".djlintrc_global", "djlint_toml_global.toml"]
)
def test_reformat_custom_file_src(runner: CliRunner, config_path: str) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--reformat",
            "--configuration",
            f"tests/test_config/test_files/{config_path}",
        ),
    )
    assert """Reformatting 2/2 files""" in result.output


@pytest.mark.parametrize(
    ("config_path_local", "config_path_global", "config_data"),
    [
        ("djlint.toml", "djlint_toml_global.toml", b'ignore = "H025"'),
        (".djlintrc", ".djlintrc_global", b'{"ignore": "H025"}'),
    ],
)
def test_global_override(
    runner: CliRunner,
    config_path_local: str,
    config_path_global: str,
    config_data: bytes,
) -> None:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--configuration",
            f"tests/test_config/test_files/{config_path_global}",
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
            f"tests/test_config/test_files/{config_path_global}",
            "--ignore",
            "H025,H020",
        ),
    )
    # passes
    assert result.exit_code == 0

    # check project settings override

    # create project settings folder
    # add a gitignore file
    djlintrc_path = Path(
        "tests", "test_config", "test_files", config_path_local
    )
    djlintrc_path.write_bytes(config_data)

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_files/test_two.html",
            "--lint",
            "--configuration",
            f"tests/test_config/test_files/{config_path_global}",
        ),
    )

    result_two = runner.invoke(
        djlint,
        (
            "tests/test_config/test_files/test.html",
            "--lint",
            "--configuration",
            f"tests/test_config/test_files/{config_path_global}",
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
