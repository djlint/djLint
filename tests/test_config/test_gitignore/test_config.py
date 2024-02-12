"""Djlint tests specific to gitignore configuration.

run::

   pytest tests/test_config_gitignore.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_gitignore.py::test_ignored_path --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116,W0702,W0703,C0103
import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from src.djlint import main as djlint


@pytest.mark.xdist_group(name="group1")
def test_cli(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/test_config/test_gitignore/html_two.html", "--lint"]
    )
    assert result.exit_code == 1

    # create .git folder to make root
    Path("tests/test_config/test_gitignore/.git").mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    with open(
        "tests/test_config/test_gitignore/.gitignore", "w", encoding="utf8"
    ) as git:
        git.write("html_two.html")

    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_gitignore/html_two.html",
            "--check",
            "--use-gitignore",
        ],
    )

    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ["tests/test_config/test_gitignore/html_two.html", "--check"]
    )
    assert result.exit_code == 1

    try:
        os.remove("tests/test_config/test_gitignore/.gitignore")
        shutil.rmtree("tests/test_config/test_gitignore/.git")
    except BaseException as e:
        print("cleanup failed")
        print(e)

    # @pytest.mark.xdist_group(name="group1")
    # def test_pyproject(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/test_config/test_gitignore/html_two.html", "--check"]
    )
    assert result.exit_code == 1

    # make a root
    Path("tests/test_config/test_gitignore/.git").mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    with open(
        "tests/test_config/test_gitignore/.gitignore", "w", encoding="utf8"
    ) as git:
        git.write("html_two.html")

    with open(
        "tests/test_config/test_gitignore/pyproject.toml", "w", encoding="utf8"
    ) as git:
        git.write("[tool]\n[tool.djlint]\nuse_gitignore=true")

    result = runner.invoke(
        djlint, ["tests/test_config/test_gitignore/html_two.html", "--check"]
    )

    assert result.exit_code == 0

    with open(
        "tests/test_config/test_gitignore/pyproject.toml", "w", encoding="utf8"
    ) as git:
        git.write("[tool]\n[tool.djlint]\nuse_gitignore=false")

    result = runner.invoke(
        djlint, ["tests/test_config/test_gitignore/html_two.html", "--check"]
    )
    assert result.exit_code == 1

    # verify cli overrides pyproject
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_gitignore/html_two.html",
            "--check",
            "--use-gitignore",
        ],
    )
    print(result.output)
    assert result.exit_code == 0

    try:
        os.remove("tests/test_config/test_gitignore/.gitignore")
        os.remove("tests/test_config/test_gitignore/pyproject.toml")
        shutil.rmtree("tests/test_config/test_gitignore/.git")
    except BaseException as e:
        print("cleanup failed")
        print(e)

    # @pytest.mark.xdist_group(name="group1")
    # def test_ignored_path(runner: CliRunner) -> None:
    # test for https://github.com/djlint/djLint/issues/224
    # create .git folder to make root
    Path("tests/test_config/test_gitignore/.git").mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    with open(
        "tests/test_config/test_gitignore/.gitignore", "w", encoding="utf8"
    ) as git:
        git.write("var")

    result = runner.invoke(
        djlint, ["-", "--use-gitignore"], input='<div><p id="a"></p></div>'
    )
    print(result.output)
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    try:
        os.remove("tests/test_config/test_gitignore/.gitignore")
        shutil.rmtree("tests/test_config/test_gitignore/.git")
    except BaseException as e:
        print("cleanup failed")
        print(e)
