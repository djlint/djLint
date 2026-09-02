"""Test for github output."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_github_output_flag(runner: CliRunner) -> None:
    """Test that --github-output flag produces ::error/warning:: output."""
    result = runner.invoke(
        djlint,
        ("-", "--lint", "--github-output"),
        input="<div></div>",
        env={"GITHUB_ACTIONS": ""},
    )
    assert "::warning" in result.output
    assert "H020" in result.output
    assert "Statistics" not in result.output


def test_github_output_stdin_reformat_stream(runner: CliRunner) -> None:
    """Annotations keep off stdout while stdout is carrying the file."""
    src = '<div style="color:red"></div>'

    result = runner.invoke(
        djlint,
        ("-", "--lint", "--github-output"),
        input=src,
        env={"GITHUB_ACTIONS": ""},
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
        djlint,
        ("-", "--reformat", "--lint"),
        input=src,
        env={"GITHUB_ACTIONS": "true"},
    )
    assert result.stdout == src + "\n"
    assert "::warning" in result.stderr


def test_github_output_env_var(runner: CliRunner) -> None:
    """Test that GITHUB_ACTIONS env var triggers github output."""
    result = runner.invoke(
        djlint,
        ("-", "--lint"),
        input="<div></div>",
        env={"GITHUB_ACTIONS": "true"},
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


def test_escaping(runner: CliRunner) -> None:
    """Test character escaping in GitHub output."""
    result = runner.invoke(
        djlint,
        ("-", "--lint", "--github-output"),
        input="<div></div>",
        env={"GITHUB_ACTIONS": ""},
    )
    assert "::warning line=1,col=1::H020" in result.output
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
