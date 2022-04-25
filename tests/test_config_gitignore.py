"""Djlint tests specific to gitignore configuration.

run::

   pytest tests/test_config_gitignore.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_gitignore.py::test_ignored_path --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116
import os
import shutil
from pathlib import Path

from click.testing import CliRunner

from src.djlint import main as djlint


def test_cli(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_gitignore/html_two.html", "--lint"])
    assert result.exit_code == 1

    # create .git folder to make root
    Path("tests/config_gitignore/.git").mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    with open("tests/config_gitignore/.gitignore", "w") as git:
        git.write("html_two.html")

    result = runner.invoke(
        djlint, ["tests/config_gitignore/html_two.html", "--check", "--use-gitignore"]
    )

    assert result.exit_code == 0

    result = runner.invoke(djlint, ["tests/config_gitignore/html_two.html", "--check"])
    assert result.exit_code == 1

    os.remove("tests/config_gitignore/.gitignore")
    shutil.rmtree("tests/config_gitignore/.git")


def test_pyproject(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_gitignore/html_two.html", "--check"])
    assert result.exit_code == 1

    # make a root
    Path("tests/config_gitignore/.git").mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    with open("tests/config_gitignore/.gitignore", "w") as git:
        git.write("html_two.html")

    with open("tests/config_gitignore/pyproject.toml", "w") as git:
        git.write("[tool]\n[tool.djlint]\nuse_gitignore=true")

    result = runner.invoke(djlint, ["tests/config_gitignore/html_two.html", "--check"])

    assert result.exit_code == 0

    with open("tests/config_gitignore/pyproject.toml", "w") as git:
        git.write("[tool]\n[tool.djlint]\nuse_gitignore=false")

    result = runner.invoke(djlint, ["tests/config_gitignore/html_two.html", "--check"])
    assert result.exit_code == 1

    # verify cli overrides pyproject
    result = runner.invoke(
        djlint, ["tests/config_gitignore/html_two.html", "--check", "--use-gitignore"]
    )
    assert result.exit_code == 0

    os.remove("tests/config_gitignore/.gitignore")
    os.remove("tests/config_gitignore/pyproject.toml")
    shutil.rmtree("tests/config_gitignore/.git")

def test_ignored_path(runner: CliRunner) -> None:
    # test for https://github.com/Riverside-Healthcare/djLint/issues/224
    # create .git folder to make root
    Path("tests/config_gitignore/.git").mkdir(parents=True, exist_ok=True)
    # add a gitignore file
    with open("tests/config_gitignore/.gitignore", "w") as git:
        git.write("var")

    result = runner.invoke(djlint, ["-", "--use-gitignore"], input='<div><p id="a"></p></div>')
    print(result.output)
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    os.remove("tests/config_gitignore/.gitignore")
    shutil.rmtree("tests/config_gitignore/.git")
