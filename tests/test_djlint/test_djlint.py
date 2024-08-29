"""Djlint base tests.

run::

    pytest tests/test_djlint/test_djlint.py --cov=src/djlint --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_djlint/test_djlint.py::test_hyphen_file

or::

    tox

"""

from __future__ import annotations

import subprocess
import sys
from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING

from djlint import main as djlint
from tests.conftest import write_to_file

if TYPE_CHECKING:
    from tempfile import _TemporaryFileWrapper

    from click.testing import CliRunner


def test_help(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-h",))
    assert result.exit_code == 0
    assert "djLint · HTML template linter and formatter." in result.output


def test_bad_args(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-a",))
    assert result.exit_code == 2
    assert "Error: No such option: -a" in result.output

    result = runner.invoke(djlint, ("--aasdf",))
    assert result.exit_code == 2
    assert "Error: No such option: --aasdf" in result.output


def test_nonexisting_file(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("not_a_file.html",))
    assert result.exit_code == 2
    assert "Path 'not_a_file.html' does not exist." in result.output


def test_existing_file(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_djlint/bad.html",))
    assert result.exit_code == 1
    assert str(Path("tests", "test_djlint", "bad.html")) in result.output


def test_hyphen_file(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_djlint/-.html",))
    assert result.exit_code == 1
    print(result.output)
    assert str(Path("tests", "test_djlint", "-.html")) in result.output


def test_multiple_files(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "tests/test_djlint/multiple_files/a",
            "tests/test_djlint/multiple_files/b",
            "--check",
        ),
    )
    assert result.exit_code == 1
    assert "3 files would be updated." in result.output


def test_bad_path(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/nowhere",))
    assert result.exit_code == 2
    assert "does not exist." in result.output


def test_good_path_with_e(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_djlint/", "-e", "html"))
    assert result.exit_code == 1
    assert str(Path("tests", "test_djlint", "bad.html")) in result.output


def test_good_path_with_extension(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_djlint/", "--extension", "html*")
    )
    assert result.exit_code == 1
    assert str(Path("tests", "test_djlint", "bad.html")) in result.output
    assert str(Path("tests", "test_djlint", "bad.html.dj")) in result.output


def test_good_path_with_bad_ext(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_djlint/", "-e", "html.alphabet")
    )
    assert result.exit_code == 0
    assert "No files to check!" in result.output


def test_empty_file(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"")
    result = runner.invoke(djlint, (tmp_file.name,))
    assert result.exit_code == 0


def test_stdin(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-",), input='<div><p id="a"></p></div>')
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    # check with multiple inputs
    result = runner.invoke(
        djlint, ("-", "-"), input='<div><p id="a"></p></div>'
    )
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    # check with reformat
    result = runner.invoke(djlint, ("-", "--reformat"), input="<div></div>")
    assert result.output == "<div></div>\n"

    # check with check
    result = runner.invoke(djlint, ("-", "--check"), input="<div></div>")
    assert result.output == "<div></div>\n"


def test_stdin_non_ascii(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-", "--reformat"), input="必須")
    assert result.output == "必須\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input="Вход")
    assert result.output == "Вход\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input="çéâêîôûàèìòùëïü")
    assert result.output == "çéâêîôûàèìòùëïü\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input="😀😂🤣😆🥰")
    assert result.output == "😀😂🤣😆🥰\n"


def test_check(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, (tmp_file.name, "--check"))
    assert result.exit_code == 0


def test_check_non_existing_file(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_djlint/nothing.html", "--check")
    )
    assert result.exit_code == 2


def test_check_non_existing_folder(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/nothing", "--check"))
    assert result.exit_code == 2


def test_check_reformatter_simple_error(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, (tmp_file.name, "--check"))
    assert result.exit_code == 1
    assert "1 file would be updated." in result.output


def test_reformatter_simple_error(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, (tmp_file.name, "--reformat"))
    assert result.exit_code == 1
    assert "1 file was updated." in result.output


def test_reformatter_no_error(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div>\n    <p>nice stuff here</p>\n</div>\n")
    old_mtime = Path(tmp_file.name).stat().st_mtime
    result = runner.invoke(djlint, (tmp_file.name, "--reformat"))
    assert result.exit_code == 0
    assert "0 files were updated." in result.output
    new_mtime = Path(tmp_file.name).stat().st_mtime
    assert new_mtime == old_mtime


def test_check_reformatter_simple_error_quiet(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div><p>nice stuff here</p></div>")
    result = runner.invoke(djlint, (tmp_file.name, "--check", "--quiet"))
    assert result.exit_code == 1
    assert "1 file would be updated." not in result.output


def test_check_reformatter_no_error(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div>\n    <p>nice stuff here</p>\n</div>")
    result = runner.invoke(djlint, (tmp_file.name, "--check"))
    assert result.exit_code == 0
    assert "0 files would be updated." in result.output


def test_warn(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(
        tmp_file.name, b"<div style='color:pink;'><p>nice stuff here</p></div>"
    )
    result = runner.invoke(djlint, (tmp_file.name, "--lint", "--warn"))
    assert result.exit_code == 0


def test_version(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("--version",))
    assert metadata.version("djlint") in result.output


def test_python_call() -> None:
    # give up fighting windows lol
    if sys.platform != "win32":
        py_sub = subprocess.run(  # noqa: S603
            ("python", "-m", "djlint", "-h"), capture_output=True, check=False
        )
        print(py_sub.stdout)
        print(py_sub.returncode)
        assert b"python -m djlint [OPTIONS] SRC ..." in py_sub.stdout
        assert py_sub.returncode == 0

        py_sub = subprocess.run(  # noqa: S603
            ("python", "-m", "djlint", "__init__", "-h"),
            capture_output=True,
            check=False,
        )
        print(py_sub.stdout)
        print(py_sub.returncode)
        assert b"python -m djlint [OPTIONS] SRC ..." in py_sub.stdout
        assert py_sub.returncode == 0


def test_line_ending(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    # write a windows line ending to file
    text_in = "<div></div>\r\n"
    with Path(tmp_file.name).open("w", encoding="utf-8", newline="") as windows:
        windows.write(text_in)

    # make sure line ending was still there
    assert Path(tmp_file.name).read_bytes().decode("utf-8") == text_in

    # check formatting
    result = runner.invoke(djlint, (tmp_file.name, "--check", "--quiet"))

    assert result.exit_code == 0
