"""Djlint tests specific to --stdin-filename.

uv run pytest tests/test_config/test_stdin_filename/test_config.py
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner

_HTML = "<div>\n    <div></div>"
_CONFIG = "tests/test_config/test_stdin_filename/pyproject.toml"


def test_stdin_filename_matches_per_file_ignores(runner: CliRunner) -> None:
    """A --stdin-filename matching a per-file-ignores pattern suppresses it."""
    result = runner.invoke(
        djlint,
        ("-", "--stdin-filename", "myfile.html", "--configuration", _CONFIG),
        input=_HTML,
    )
    assert "H025" not in result.output
    assert "H020" in result.output


def test_stdin_filename_not_matching_per_file_ignores(
    runner: CliRunner,
) -> None:
    """A --stdin-filename that matches no pattern reports every rule."""
    result = runner.invoke(
        djlint,
        ("-", "--stdin-filename", "other.html", "--configuration", _CONFIG),
        input=_HTML,
    )
    assert "H025" in result.output
    assert "H020" in result.output


def test_stdin_filename_default_unchanged(runner: CliRunner) -> None:
    """Without --stdin-filename, per-file-ignores still match against "-"."""
    result = runner.invoke(
        djlint, ("-", "--configuration", _CONFIG), input=_HTML
    )
    assert "H020" not in result.output
    assert "H025" in result.output


def test_stdin_filename_uses_native_separators(runner: CliRunner) -> None:
    """A native-separator path matches a pattern written with "/"."""
    result = runner.invoke(
        djlint,
        (
            "-",
            "--stdin-filename",
            str(Path("templates", "index.html")),
            "--configuration",
            _CONFIG,
        ),
        input=_HTML,
    )
    assert "H025" not in result.output
    assert "H020" in result.output


def test_stdin_filename_used_in_lint_message(runner: CliRunner) -> None:
    """The --stdin-filename value is used as the error dict's filename key."""
    result = runner.invoke(
        djlint,
        (
            "-",
            "--stdin-filename",
            "myfile.html",
            "--configuration",
            _CONFIG,
            "--linter-output-format",
            "{filename} {code}",
        ),
        input=_HTML,
    )
    assert "myfile.html H020" in result.output
