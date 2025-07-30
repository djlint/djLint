"""Test for cli inputs.

uv run pytest tests/test_cli.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_cli(runner: CliRunner) -> None:
    # missing options:
    result = runner.invoke(
        djlint,
        (
            "-",
            "--check",
            "--blank-line-after-tag",
            "p",
            "--blank-line-before-tag",
            "p",
            "--custom-blocks",
            "toc",
            "--custom-html",
            "asdf",
            "--exclude",
            ".asdf",
            "--extend-exclude",
            ".asdf",
            "--extension",
            "html.dj",
            "--format-attribute-template-tags",
            "--format-css",
            "--format-js",
            "--ignore",
            "H014,H015",
            "--ignore-blocks",
            "raw",
            "--ignore-case",
            "--include",
            "H014",
            "--indent",
            "4",
            "--linter-output-format",
            "{code}",
            "--max-attribute-length",
            "9",
            "--max-line-length",
            "100",
            "--preserve-blank-lines",
            "--preserve-leading-space",
            "--profile",
            "django",
            "--require-pragma",
            "--use-gitignore",
            "--per-file-ignores",
            "test.html",
            "H014",
            "--per-file-ignores",
            "test2.html",
            "H015",
            "--indent-css",
            "4",
            "--indent-js",
            "4",
        ),
        input="<div></div>\n",
    )

    print(result.output)

    assert result.exit_code == 0


def test_no_files_exit_code(runner: CliRunner) -> None:
    """Test that djLint exits with code 1 when no files are found."""
    # Create a temporary empty directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test with --lint flag
        result = runner.invoke(djlint, ["--lint", temp_dir])
        assert result.exit_code == 1
        assert "No files to check! 😢" in result.output

        # Test with --check flag  
        result = runner.invoke(djlint, ["--check", temp_dir])
        assert result.exit_code == 1
        assert "No files to check! 😢" in result.output

        # Test with --reformat flag
        result = runner.invoke(djlint, ["--reformat", temp_dir]) 
        assert result.exit_code == 1
        assert "No files to check! 😢" in result.output


def test_no_files_with_specific_extension(runner: CliRunner) -> None:
    """Test that djLint exits with code 1 when no files match the extension."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file with different extension
        Path(temp_dir, "test.txt").write_text("some content")
        
        # Should still exit with code 1 since no .html files found
        result = runner.invoke(djlint, ["--lint", temp_dir])
        assert result.exit_code == 1
        assert "No files to check! 😢" in result.output


def test_files_found_normal_exit(runner: CliRunner) -> None:
    """Test that djLint exits normally when files are found."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an HTML file
        html_file = Path(temp_dir, "test.html")
        html_file.write_text("<div></div>")
        
        # Should exit with code 0 when files are found (assuming no lint errors)
        result = runner.invoke(djlint, ["--lint", temp_dir])
        assert result.exit_code == 0
        assert "No files to check! 😢" not in result.output


def test_stdin_normal_operation(runner: CliRunner) -> None:
    """Test that djLint works normally with stdin input."""
    # Test with stdin content - should not exit with code 1
    result = runner.invoke(djlint, ["--lint", "-"], input="<div></div>")
    # Stdin should always work as it creates a temp file
    assert result.exit_code == 0
    assert "No files to check! 😢" not in result.output


def test_nonexistent_path_exit_code(runner: CliRunner) -> None:
    """Test that djLint exits with code 1 for nonexistent paths."""
    # This should fail before we even get to the file check logic
    # Click should handle this case, but let's test our understanding
    result = runner.invoke(djlint, ["--lint", "/tmp/nonexistent_directory_12345"])
    # Click will fail before our code is reached for nonexistent paths
    # because of exists=True in the path parameter
    assert result.exit_code != 0  # Could be 1 or 2 depending on Click's handling
