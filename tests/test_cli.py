"""Test for cli inputs.

uv run pytest tests/test_cli.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

import click

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner

_CLI_DOCS = Path("docs/src/_includes/cli.md")
_CONFIGURATION_DOCS = Path("docs/src/_data/configuration.json")
_HELP_WIDTH = 80


def test_help_snapshot_matches_docs(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("--help",), prog_name="djlint", terminal_width=_HELP_WIDTH
    )
    assert result.exit_code == 0

    snapshot = re.search(
        r"```bash\n(.*?)\n```", _CLI_DOCS.read_text(encoding="utf-8"), re.DOTALL
    )
    assert snapshot is not None, f"no help block found in {_CLI_DOCS}"
    assert snapshot.group(1) == result.output.rstrip("\n"), (
        f"{_CLI_DOCS} is out of date; regenerate it from `djlint --help`"
    )


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
            "--format-attribute-js-json",
            "--format-attribute-js-json-pattern",
            "^(on[a-z]+|x-[a-z-]+)$",
            "--format-attribute-js-json-min-props",
            "3",
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
            "--preserve-class-newlines",
            "--preserve-leading-space",
            "--profile",
            "django",
            "--require-pragma",
            "--single-attribute-per-line",
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
        input="{# djlint:on #}\n<div>\n</div>\n",
    )

    print(result.output)

    assert result.exit_code == 0


def test_documented_options_exist() -> None:
    """Every flag the configuration page shows has to be a real one."""
    flags = {
        option
        for param in djlint.params
        if isinstance(param, click.Option)
        for option in param.opts
    }
    documented = {
        word
        for entry in json.loads(_CONFIGURATION_DOCS.read_text(encoding="utf-8"))
        for usage in entry["usage"]
        if usage["name"] == "cli"
        for word in usage["value"].split()
        if word.startswith("--")
    }

    assert documented <= flags, (
        f"{_CONFIGURATION_DOCS} documents flags djLint does not have: "
        f"{sorted(documented - flags)}"
    )
