"""Djlint base tests.

uv run pytest tests/test_djlint/test_djlint.py
"""

from __future__ import annotations

import errno
import subprocess
import sys
import tempfile
from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING

import djlint as djlint_module
from djlint import main as djlint, output as djlint_output
from tests.conftest import write_to_file

if TYPE_CHECKING:
    from tempfile import _TemporaryFileWrapper

    import pytest
    from click.testing import CliRunner


def test_help(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-h",))
    assert result.exit_code == 0
    assert "djLint · HTML template linter and formatter." in result.output


def test_bad_args(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-a",))
    assert result.exit_code == 2
    assert "Error: No such option '-a'" in result.output

    result = runner.invoke(djlint, ("--aasdf",))
    assert result.exit_code == 2
    assert "Error: No such option '--aasdf'" in result.output


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


def test_overlapping_paths_are_checked_once(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        (
            "tests/test_djlint/multiple_files/b",
            "tests/test_djlint/multiple_files/b/b1.html",
            "tests/test_djlint/multiple_files/b",
            "--check",
        ),
    )
    assert result.exit_code == 1
    assert "2 files would be updated." in result.output


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
    """Nothing matched at all, so the run checked nothing it was asked to."""
    result = runner.invoke(
        djlint, ("tests/test_djlint/", "-e", "html.alphabet")
    )
    assert result.exit_code == 2
    assert "No files to check!" in result.stderr
    assert not result.stdout


def test_good_path_with_bad_ext_allow_empty_input(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ("tests/test_djlint/", "-e", "html.alphabet", "--allow-empty-input"),
    )
    assert result.exit_code == 0
    assert "No files to check!" in result.stderr


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
    assert "1/1 files" not in result.stderr

    result = runner.invoke(
        djlint, ("-", "-"), input='<div><p id="a"></p></div>'
    )
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output

    result = runner.invoke(djlint, ("-", "--reformat"), input="<div></div>")
    assert result.exit_code == 0
    assert result.output == "<div></div>\n"

    result = runner.invoke(djlint, ("-", "--check"), input="<div></div>")
    assert result.exit_code == 0
    assert result.output == "<div></div>\n"

    # check require pragma
    result = runner.invoke(
        djlint, ("-", "--require-pragma"), input="<div></div>"
    )
    assert result.exit_code == 0
    assert "No files to check!" in result.stderr
    assert not result.stdout

    # input skipped by require-pragma must come back byte for byte, and the
    result = runner.invoke(
        djlint,
        ("-", "--reformat", "--require-pragma"),
        input="<div>   <p>x</p></div>\n\n\n",
    )
    assert result.exit_code == 0
    assert result.stdout == "<div>   <p>x</p></div>\n\n\n"
    assert "No files to check!" in result.stderr


def test_stdin_filename_option(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ("-", "--stdin-filename", "custom.html"),
        input='<div><p id="a"></p></div>',
    )
    assert result.exit_code == 0
    assert "Linted 1 file" in result.output


def test_stdin_reformat_without_temp_file(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_named_temp_file(*_args: object, **_kwargs: object) -> None:
        raise AssertionError

    monkeypatch.setattr(tempfile, "NamedTemporaryFile", fail_named_temp_file)

    result = runner.invoke(
        djlint, ("-", "--check"), input="<div><p>nice stuff here</p></div>"
    )

    assert result.exit_code == 1
    assert result.output == "<div>\n    <p>nice stuff here</p>\n</div>\n"


def test_stdin_non_ascii(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("-", "--reformat"), input="必須")
    assert result.output == "必須\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input="Вход")
    assert result.output == "Вход\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input="çéâêîôûàèìòùëïü")
    assert result.output == "çéâêîôûàèìòùëïü\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input="😀😂🤣😆🥰")
    assert result.output == "😀😂🤣😆🥰\n"


def test_stdin_lint_output_stream(runner: CliRunner) -> None:
    """Lint output moves to stderr only when stdout is carrying the file."""
    src = '<div style="color:red"></div>'

    result = runner.invoke(djlint, ("-",), input=src)
    assert "H021" in result.stdout
    assert "Linted 1 file" in result.stdout

    result = runner.invoke(djlint, ("-", "--reformat", "--lint"), input=src)
    assert result.stdout == src + "\n"
    assert "H021" in result.stderr
    assert "Linted 1 file" in result.stderr

    result = runner.invoke(
        djlint, ("-", "--check", "--lint", "--statistics"), input=src
    )
    assert result.stdout == src + "\n"
    assert "H021" in result.stderr
    assert "Statistics" in result.stderr


def test_stdin_invalid_utf8(runner: CliRunner) -> None:
    """Undecodable input is bad data, not a djLint crash."""
    result = runner.invoke(
        djlint, ("-", "--reformat"), input=b"<div>\xff</div>"
    )
    assert result.exit_code == 2
    assert not result.stdout
    assert "not valid UTF-8" in result.stderr
    assert "Traceback" not in result.stderr
    assert "report unexpected failures" not in result.stderr


def test_stdin_preserves_line_endings(runner: CliRunner) -> None:
    """A CRLF buffer comes back CRLF, exactly as it does through a file.

    An LF buffer is left alone.
    """
    crlf = b"<div>\r\n<p>hi</p>\r\n</div>\r\n"

    result = runner.invoke(djlint, ("-", "--reformat"), input=crlf)
    assert result.stdout_bytes == b"<div>\r\n    <p>hi</p>\r\n</div>\r\n"

    # the pragma passthrough really is byte for byte
    result = runner.invoke(
        djlint, ("-", "--reformat", "--require-pragma"), input=crlf
    )
    assert result.stdout_bytes == crlf

    result = runner.invoke(
        djlint, ("-", "--reformat"), input=b"<div>\n<p>hi</p>\n</div>\n"
    )
    assert result.stdout_bytes == b"<div>\n    <p>hi</p>\n</div>\n"


def test_closed_pipe_is_not_a_crash(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`djlint . | head` is the consumer's choice, not a djLint failure.

    No traceback, and no invitation to file a bug against djLint.
    """

    def hang_up(*_args: object, **_kwargs: object) -> int:
        raise BrokenPipeError(errno.EPIPE, "broken pipe")

    monkeypatch.setattr(djlint_output, "print_output", hang_up)

    result = runner.invoke(djlint, ("-", "--lint"), input="<div></div>")

    assert result.exit_code == 2
    assert "Traceback" not in result.stderr
    assert "report unexpected failures" not in result.stderr


def test_check(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    write_to_file(tmp_file.name, b"<div></div>")
    result = runner.invoke(djlint, (tmp_file.name, "--check"))
    assert result.exit_code == 0


def test_single_worker_skips_executor(
    runner: CliRunner,
    tmp_file: _TemporaryFileWrapper[bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_to_file(tmp_file.name, b"<div></div>")
    monkeypatch.setattr(djlint_module, "process_cpu_count", lambda: 1)

    result = runner.invoke(djlint, (tmp_file.name, "--check"))

    assert result.exit_code == 0


def test_import_skips_runtime_helpers() -> None:
    src_path = str(Path(__file__).parents[2] / "src")
    code = (
        "import sys; "
        f"sys.path.insert(0, {src_path!r}); "
        "import djlint; "
        "blocked = {'concurrent.futures', 'cssbeautifier', 'jsbeautifier', "
        "'djlint.lint', 'djlint.reformat'}; "
        "loaded = sorted(blocked & sys.modules.keys()); "
        "print('\\n'.join(loaded)); "
        "raise SystemExit(bool(loaded))"
    )
    py_sub = subprocess.run(  # noqa: S603
        (sys.executable, "-c", code),
        capture_output=True,
        check=False,
        text=True,
    )

    assert py_sub.returncode == 0, py_sub.stdout


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
    if sys.platform != "win32":
        py_sub = subprocess.run(
            ("python", "-m", "djlint", "-h"),  # noqa: S607
            capture_output=True,
            check=False,
        )
        print(py_sub.stdout)
        print(py_sub.returncode)
        assert b"python -m djlint [OPTIONS] SRC ..." in py_sub.stdout
        assert py_sub.returncode == 0

        py_sub = subprocess.run(
            ("python", "-m", "djlint", "__init__", "-h"),  # noqa: S607
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
    text_in = "<div></div>\r\n"
    Path(tmp_file.name).write_text(text_in, encoding="utf-8", newline="")

    assert Path(tmp_file.name).read_bytes().decode("utf-8") == text_in

    result = runner.invoke(djlint, (tmp_file.name, "--check", "--quiet"))

    assert result.exit_code == 0
