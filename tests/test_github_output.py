"""Test for github output."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_github_output_flag(runner: CliRunner) -> None:
    """Test that --github-output flag produces ::error/warning:: output."""
    # Ensure GITHUB_ACTIONS is unset or overridden by flag
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--github-output",
        ),
        input="<div></div>",
        env={"GITHUB_ACTIONS": ""},
    )
    # H020 or similar error should appear
    assert "::warning" in result.output
    assert "H020" in result.output
    # Normal output should be suppressed
    assert "Statistics" not in result.output


def test_github_output_env_var(runner: CliRunner) -> None:
    """Test that GITHUB_ACTIONS env var triggers github output."""
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
        ),
        input="<div></div>",
        env={"GITHUB_ACTIONS": "true"},
    )
    assert "::warning" in result.output
    assert "Statistics" not in result.output


def test_no_github_output_flag(runner: CliRunner) -> None:
    """Test that --no-github-output overrides GITHUB_ACTIONS."""
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--no-github-output",
        ),
        input="<div></div>",
        env={"GITHUB_ACTIONS": "true"},
    )
    assert "::warning" not in result.output
    assert "H020" in result.output  # Error still there
    # Should look like normal output
    assert "Linted 1 file" in result.output


def test_escaping(runner: CliRunner) -> None:
    """Test character escaping in GitHub output."""
    result = runner.invoke(
        djlint,
        (
            "-",
            "--lint",
            "--github-output",
        ),
        input="<div></div>",
        env={"GITHUB_ACTIONS": ""},
    )
    # ::warning file=...,line=1::H020 ...
    assert "::warning file=" in result.output
    assert ",line=1::H020" in result.output
