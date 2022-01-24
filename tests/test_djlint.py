"""
Djlint base tests.

run::

    pytest --cov=src/djlint --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

for a single test::

    pytest tests/test_djlint.py::test_version --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

or::

    tox

"""
import subprocess
import sys

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore


# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint

from .conftest import write_to_file


def test_help(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["-h"])
    assert result.exit_code == 0
    assert "djLint · HTML template linter and formatter." in result.output


def test_bad_args(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["-a"])
    assert result.exit_code == 2
    assert "Error: No such option: -a" in result.output

    result = runner.invoke(djlint, ["--aasdf"])
    assert result.exit_code == 2
    assert "Error: No such option: --aasdf" in result.output


def test_nonexisting_file(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["not_a_file.html"])
    assert result.exit_code == 2
    assert "Path 'not_a_file.html' does not exist." in result.output


def test_existing_file(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/bad.html"])
    assert result.exit_code == 1
    assert str(Path("tests/bad.html")) in result.output


def test_multiple_files(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/multiple_files/a", "tests/multiple_files/b", "--check"]
    )
    assert result.exit_code == 1
    assert "3 files would be updated." in result.output


def test_bad_path(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/nowhere"])
    assert result.exit_code == 2
    assert "does not exist." in result.output


def test_good_path_with_e(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/", "-e", "html"])
    assert result.exit_code == 1
    assert str(Path("tests/bad.html")) in result.output


def test_good_path_with_extension(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/", "--extension", "html*"])
    assert result.exit_code == 1
    assert str(Path("tests/bad.html")) in result.output
    assert str(Path("tests/bad.html.dj")) in result.output


def test_good_path_with_bad_ext(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/", "-e", "html.alphabet"])
    assert result.exit_code == 0
    assert "No files to check!" in result.output


def test_empty_file(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"")
    result = runner.invoke(djlint, [tmp_file.name])
    assert result.exit_code == 0


def test_stdin(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["-"], input='<div><p id="a"></p></div>')
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    # check with multiple inputs
    result = runner.invoke(djlint, ["-", "-"], input='<div><p id="a"></p></div>')
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    # check with reformat
    result = runner.invoke(djlint, ["-", "--reformat"], input="<div></div>")
    assert "<div></div>\n" == result.output


def test_check(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--check"])
    assert result.exit_code == 0


def test_check_non_existing_file(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/nothing.html", "--check"])
    assert result.exit_code == 2


def test_check_non_existing_folder(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/nothing", "--check"])
    assert result.exit_code == 2


def test_check_reformatter_simple_error(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--check"])
    assert result.exit_code == 1
    assert "1 file would be updated." in result.output


def test_reformatter_simple_error(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert result.exit_code == 1
    assert "1 file was updated." in result.output


def test_check_reformatter_simple_error_quiet(
    runner: CliRunner, tmp_file: TextIO
) -> None:
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, [tmp_file.name, "--check", "--quiet"])
    assert result.exit_code == 1
    assert "1 file would be updated." in result.output


def test_check_reformatter_no_error(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name, b"<div>\n    <p>\n        nice stuff here\n    </p>\n</div>"
    )
    result = runner.invoke(djlint, [tmp_file.name, "--check"])
    assert result.exit_code == 0
    assert "0 files would be updated." in result.output


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["--version"])
    assert metadata.version("djlint") in result.output


def test_python_call() -> None:
    # give up fighting windows lol
    if sys.platform != "win32":
        x = subprocess.run(
            ["python", "-m", "djlint", "-h"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert b"python -m djlint [OPTIONS] SRC ..." in x.stdout
        assert x.returncode == 0

        x = subprocess.run(
            ["python", "-m", "djlint", "__init__", "-h"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert b"python -m djlint [OPTIONS] SRC ..." in x.stdout
        assert x.returncode == 0
