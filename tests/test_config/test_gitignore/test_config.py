"""Djlint tests specific to gitignore configuration.

run::

   pytest tests/test_config_gitignore.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_gitignore.py::test_ignored_path --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


@pytest.mark.xdist_group(name="group1")
def test_cli(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--lint")
    )
    assert result.exit_code == 1

    git_path = Path("tests", "test_config", "test_gitignore", ".git")
    gitignore_path = Path(
        "tests", "test_config", "test_gitignore", ".gitignore"
    )

    # create .git folder to make root
    git_path.mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    gitignore_path.write_text("html_two.html", encoding="utf-8")

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_gitignore/html_two.html",
            "--check",
            "--use-gitignore",
        ),
    )

    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )
    assert result.exit_code == 1

    try:
        gitignore_path.unlink()
        shutil.rmtree(git_path)
    except Exception as e:
        print("cleanup failed")
        print(e)

    # @pytest.mark.xdist_group(name="group1")
    # def test_pyproject(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )
    assert result.exit_code == 1

    # make a root
    git_path.mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    gitignore_path.write_text("html_two.html", encoding="utf-8")
    pyproject_path = Path(
        "tests", "test_config", "test_gitignore", "pyproject.toml"
    )
    pyproject_path.write_text(
        "[tool]\n[tool.djlint]\nuse_gitignore=true", encoding="utf-8"
    )

    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )

    assert result.exit_code == 0

    pyproject_path.write_text(
        "[tool]\n[tool.djlint]\nuse_gitignore=false", encoding="utf-8"
    )

    result = runner.invoke(
        djlint, ("tests/test_config/test_gitignore/html_two.html", "--check")
    )
    assert result.exit_code == 1

    # verify cli overrides pyproject
    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_gitignore/html_two.html",
            "--check",
            "--use-gitignore",
        ),
    )
    print(result.output)
    assert result.exit_code == 0

    try:
        gitignore_path.unlink()
        pyproject_path.unlink()
        shutil.rmtree(git_path)
    except Exception as e:
        print("cleanup failed")
        print(e)

    # @pytest.mark.xdist_group(name="group1")
    # def test_ignored_path(runner: CliRunner) -> None:
    # test for https://github.com/djlint/djLint/issues/224
    # create .git folder to make root
    git_path.mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    gitignore_path.write_text("var", encoding="utf-8")

    result = runner.invoke(
        djlint, ("-", "--use-gitignore"), input='<div><p id="a"></p></div>'
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    try:
        gitignore_path.unlink()
        shutil.rmtree(git_path)
    except Exception as e:
        print("cleanup failed")
        print(e)
