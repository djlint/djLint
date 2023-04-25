"""Test for cli inputs.

poetry run pytest tests/test_cli.py
"""
from click.testing import CliRunner

from src.djlint import main as djlint


def test_cli(runner: CliRunner) -> None:
    # missing options:
    result = runner.invoke(
        djlint,
        [
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
        ],
        input="<div></div>\n",
    )

    print(result.output)

    assert result.exit_code == 0
