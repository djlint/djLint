"""Djlint tests for runs that end up with no files to check.

An empty file list has two very different causes, and they get different
exit codes: the configuration deliberately skipping every candidate is a
success, while matching nothing at all means the run checked nothing it
was asked to check.

run::

   pytest tests/test_config/test_no_files/test_config.py --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


# content that --check would report on, so a passing run proves the file
# was skipped rather than that there was nothing to report
UNFORMATTED = "<div><p>x</p>   </div>"


def _project(tmp_path: Path, config: str = "") -> None:
    (tmp_path / "pyproject.toml").write_text(
        f"[tool]\n[tool.djlint]\n{config}", encoding="utf-8"
    )


def test_explicit_file_excluded_by_config(
    runner: CliRunner, tmp_path: Path
) -> None:
    """A named file that the config excludes is skipped, not failed.

    This is how pre-commit calls djLint: it passes the staged file names,
    and the exclude in pyproject.toml is what narrows them down.
    """
    _project(tmp_path, 'extend_exclude = "excluded"\n')
    excluded = tmp_path / "excluded"
    excluded.mkdir()
    template = excluded / "a.html"
    template.write_text(UNFORMATTED, encoding="utf-8")

    result = runner.invoke(djlint, (str(template), "--check"))

    assert result.exit_code == 0
    assert "No files to check!" in result.stderr
    assert "skipped by the configuration" in result.stderr
    assert template.read_text(encoding="utf-8") == UNFORMATTED


def test_directory_with_every_file_excluded(
    runner: CliRunner, tmp_path: Path
) -> None:
    """Excluding every file found under a directory is still a success."""
    _project(tmp_path, 'extend_exclude = "excluded"\n')
    excluded = tmp_path / "excluded"
    excluded.mkdir()
    (excluded / "a.html").write_text(UNFORMATTED, encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--check"))

    assert result.exit_code == 0
    assert "skipped by the configuration" in result.stderr


def test_no_matching_files_exits_two(runner: CliRunner, tmp_path: Path) -> None:
    """Matching nothing at all is a usage error, and keeps its own code.

    Exit 2 rather than 1 so that a wrapper can tell "your templates have
    problems" apart from "I checked nothing". See issue #1112.
    """
    _project(tmp_path)
    (tmp_path / "notes.txt").write_text("not a template", encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--check"))

    assert result.exit_code == 2
    assert "No files to check!" in result.stderr
    # nothing was excluded, so the message must not blame the configuration
    assert "skipped by the configuration" not in result.stderr


def test_no_matching_files_with_allow_empty_input(
    runner: CliRunner, tmp_path: Path
) -> None:
    """--allow-empty-input opts back into the pre-1.39.5 exit code."""
    _project(tmp_path)

    result = runner.invoke(djlint, (str(tmp_path), "--check"))
    assert result.exit_code == 2

    result = runner.invoke(
        djlint, (str(tmp_path), "--check", "--allow-empty-input")
    )
    assert result.exit_code == 0
    # the run is still explained, it just does not fail
    assert "No files to check!" in result.stderr


def test_allow_empty_input_from_pyproject(
    runner: CliRunner, tmp_path: Path
) -> None:
    """The flag is settable in config, for pipelines that cannot pass args."""
    _project(tmp_path, "allow_empty_input = true\n")

    result = runner.invoke(djlint, (str(tmp_path), "--check"))

    assert result.exit_code == 0


def test_warn_does_not_cover_an_empty_run(
    runner: CliRunner, tmp_path: Path
) -> None:
    """--warn downgrades findings, not "nothing was checked".

    Folding the two together would put every --warn user back in the
    silent no-op that #1112 reported.
    """
    _project(tmp_path)

    result = runner.invoke(djlint, (str(tmp_path), "--check", "--warn"))

    assert result.exit_code == 2


def test_no_files_message_stays_off_stdout(
    runner: CliRunner, tmp_path: Path
) -> None:
    """stdout carries formatted code, so diagnostics may not go there."""
    _project(tmp_path)

    result = runner.invoke(djlint, (str(tmp_path), "--reformat"))

    assert not result.stdout
    assert "No files to check!" in result.stderr
