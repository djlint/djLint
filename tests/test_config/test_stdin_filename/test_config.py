"""Djlint tests specific to --stdin-filename.

run::

   pytest tests/test_config/test_stdin_filename/test_config.py --cov=src/djlint \
          --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config/test_stdin_filename/test_config.py::test_stdin_filename_matches_per_file_ignores \
     --cov=src/djlint --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner

# the pyproject.toml in this directory has:
#   "myfile.html" = "H025"
#   "^-$"         = "H020"
# and the html below triggers both H025 and H020 when neither is ignored.
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
