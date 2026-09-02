"""Djlint tests for exit codes.

uv run pytest tests/test_djlint/test_exit_codes.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint import main as djlint
from djlint.settings import _PROFILES  # noqa: PLC2701
from djlint.src import _PRAGMA_PATTERNS  # noqa: PLC2701

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


DIRTY = "<div><p>x</p>   </div>"


def _project(tmp_path: Path, config: str = "") -> None:
    (tmp_path / "pyproject.toml").write_text(
        f"[tool]\n[tool.djlint]\n{config}", encoding="utf-8"
    )


def test_profile_sets_agree() -> None:
    """Rule excludes and pragma patterns must cover the same profiles.

    Config validates against _PROFILES; has_pragma indexes _PRAGMA_PATTERNS
    directly. A profile in one and not the other is a KeyError waiting for
    a --require-pragma user.
    """
    assert frozenset(_PRAGMA_PATTERNS) == _PROFILES


def test_unknown_profile_is_a_usage_error(
    runner: CliRunner, tmp_path: Path
) -> None:
    """A typo'd profile must not lint with a silently different rule set."""
    _project(tmp_path)
    (tmp_path / "a.html").write_text(DIRTY, encoding="utf-8")

    result = runner.invoke(
        djlint, (str(tmp_path), "--lint", "--profile", "djangoo")
    )

    assert result.exit_code == 2
    assert "Invalid profile 'djangoo'" in result.output
    assert "django" in result.output


def test_unknown_profile_from_config_is_a_usage_error(
    runner: CliRunner, tmp_path: Path
) -> None:
    """Config files reach the same validation as the command line."""
    _project(tmp_path, 'profile = "djangoo"\n')
    (tmp_path / "a.html").write_text(DIRTY, encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--lint"))

    assert result.exit_code == 2
    assert "Invalid profile 'djangoo'" in result.output


@pytest.mark.parametrize("profile", sorted(_PROFILES))
def test_every_profile_survives_require_pragma(
    runner: CliRunner, tmp_path: Path, profile: str
) -> None:
    """No accepted profile may raise on the pragma lookup."""
    _project(tmp_path)

    result = runner.invoke(
        djlint,
        ("-", "--lint", "--require-pragma", "--profile", profile),
        input=DIRTY,
    )

    assert result.exit_code == 0


def test_unreadable_file_does_not_look_like_a_finding(
    runner: CliRunner, tmp_path: Path
) -> None:
    """A file djLint cannot decode is a failure, not a lint error.

    Exiting 1 here would be indistinguishable from "found 1 problem". The
    traceback is kept, so a bug report still has something to go on.
    """
    _project(tmp_path)
    (tmp_path / "latin.html").write_bytes(
        "<div>caf\xe9</div>".encode("latin-1")
    )

    result = runner.invoke(djlint, (str(tmp_path), "--lint"))

    assert result.exit_code == 2
    assert "djLint failed and did not finish checking" in result.output
    assert "UnicodeDecodeError" in result.output


def test_undecodable_first_line_has_no_pragma(
    runner: CliRunner, tmp_path: Path
) -> None:
    """A file --require-pragma cannot read the first line of is skipped.

    The pragma is ascii, so a byte that does not decode is not it. The
    run used to abort on the read, before any file was checked.
    """
    _project(tmp_path)
    (tmp_path / "binary.html").write_bytes(b"\xff\xfe<div></div>")
    (tmp_path / "real.html").write_text(
        "{# djlint:on #}" + chr(10) + DIRTY, encoding="utf-8"
    )

    result = runner.invoke(
        djlint, (str(tmp_path), "--check", "--require-pragma")
    )

    assert result.exit_code == 1
    assert "1 file would be updated." in result.output
    assert "UnicodeDecodeError" not in result.output


def test_directory_matching_the_extension_is_skipped(
    runner: CliRunner, tmp_path: Path
) -> None:
    """A directory named *.html is not a template, and must not crash.

    The real template is still checked, and it needs reformatting.
    """
    _project(tmp_path)
    (tmp_path / "build.html").mkdir()
    (tmp_path / "real.html").write_text(DIRTY, encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--check"))

    assert result.exit_code == 1
    assert "1 file would be updated." in result.output


def test_directory_matching_the_extension_alone_is_not_a_candidate(
    runner: CliRunner, tmp_path: Path
) -> None:
    """A directory must not be counted as a file that got excluded.

    Nothing was found, and nothing was skipped by configuration either.
    """
    _project(tmp_path)
    (tmp_path / "build.html").mkdir()

    result = runner.invoke(djlint, (str(tmp_path), "--check"))

    assert result.exit_code == 2
    assert "skipped by the configuration" not in result.stderr
