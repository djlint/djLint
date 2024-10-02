"""Test for cli inputs.

uv run pytest tests/test_cli.py
"""

from __future__ import annotations

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
