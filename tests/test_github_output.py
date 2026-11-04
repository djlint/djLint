"""Test for github output."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint._cli import main as djlint

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


def test_github_output_flag(runner: CliRunner) -> None:
    """Test that --github-output flag produces ::error/warning:: output."""
    result = runner.invoke(
        djlint, ("-", "--lint", "--github-output"), input="<div></div>", env={"GITHUB_ACTIONS": ""}
    )
    assert "::warning" in result.output
    assert "H020" in result.output
    assert "Statistics" not in result.output


def test_github_output_stdin_reformat_stream(runner: CliRunner) -> None:
    """Annotations keep off stdout while stdout is carrying the file."""
    src = '<div style="color:red"></div>'

    result = runner.invoke(
        djlint, ("-", "--lint", "--github-output"), input=src, env={"GITHUB_ACTIONS": ""}
    )
    assert "::warning" in result.stdout

    result = runner.invoke(
        djlint,
        ("-", "--reformat", "--lint", "--github-output"),
        input=src,
        env={"GITHUB_ACTIONS": ""},
    )
    assert result.stdout == src + "\n"
    assert "::warning" in result.stderr

    result = runner.invoke(
        djlint, ("-", "--reformat", "--lint"), input=src, env={"GITHUB_ACTIONS": "true"}
    )
    assert result.stdout == src + "\n"
    assert "::warning" in result.stderr


def test_github_output_env_var(runner: CliRunner) -> None:
    """Test that GITHUB_ACTIONS env var triggers github output."""
    result = runner.invoke(
        djlint, ("-", "--lint"), input="<div></div>", env={"GITHUB_ACTIONS": "true"}
    )
    assert "::warning" in result.output
    assert "Statistics" not in result.output


def test_no_github_output_flag(runner: CliRunner) -> None:
    """Test that --no-github-output overrides GITHUB_ACTIONS."""
    result = runner.invoke(
        djlint,
        ("-", "--lint", "--no-github-output"),
        input="<div></div>",
        env={"GITHUB_ACTIONS": "true"},
    )
    assert "::warning" not in result.output
    assert "H020" in result.output
    assert "Linted 1 file" in result.output


def test_an_annotation_over_several_lines_has_no_end_column(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("-", "--lint", "--profile", "django", "--github-output"), input='<img\n  src="x">'
    )
    assert "::warning line=1,col=1,endLine=2::H013" in result.output


def test_escaping(runner: CliRunner) -> None:
    """Test character escaping in GitHub output."""
    result = runner.invoke(
        djlint, ("-", "--lint", "--github-output"), input="<div></div>", env={"GITHUB_ACTIONS": ""}
    )
    assert "::warning line=1,col=1,endLine=1,endColumn=11::H020" in result.output
    assert "file=" not in result.output


def test_statistics_are_reported(runner: CliRunner) -> None:
    """Test that --statistics is not swallowed by the github output."""
    result = runner.invoke(
        djlint,
        ("-", "--lint", "--github-output", "--statistics"),
        input="<div></div>",
        env={"GITHUB_ACTIONS": ""},
    )
    assert "::warning" in result.output
    assert "Statistics" in result.output
    assert "H020" in result.output


def test_annotations_name_the_file(runner: CliRunner, tmp_path: Path) -> None:
    """A file name is a property of the annotation, escaped as one."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "a,b%.html").write_text("<div><p>hi</p>\n</div>\n", encoding="utf-8")
    (tmp_path / "formatted.html").write_text("<div>\n    <p>hi</p>\n</div>\n", encoding="utf-8")
    (tmp_path / "img.html").write_text('<img src="x">\n', encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--check", "--lint", "--github-output"))

    assert result.exit_code == 1
    assert result.output == (
        "::error file=a%2Cb%25.html::Formatting changes required\n"
        "::warning file=img.html,line=1,col=1,endLine=1,endColumn=13"
        "::H013 Img tag should have an alt attribute.\n"
    )


def test_a_check_of_stdin_fails_without_an_annotation(runner: CliRunner) -> None:
    """Stdin has no file to annotate, so the change only sets the exit code."""
    result = runner.invoke(
        djlint, ("-", "--check", "--github-output"), input="<div><p>hi</p>\n</div>\n"
    )

    assert result.exit_code == 1
    assert result.stdout == "<div>\n    <p>hi</p>\n</div>\n"
    assert not result.stderr
