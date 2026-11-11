"""Test configuration files and values djLint cannot read.

uv run pytest tests/test_config/test_unreadable_config.py
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from click import BadParameter, UsageError

from djlint._cli import main as djlint  # noqa: PLC2701
from djlint.settings import Config, find_project_root

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


@pytest.mark.parametrize(
    ("name", "content", "message"),
    [
        pytest.param(
            "pyproject.toml",
            "[tool.djlint\n",
            "Could not read pyproject.toml: Expected ']' at the end of a table declaration",
            id="pyproject.toml",
        ),
        pytest.param(
            "djlint.toml",
            "indent =\n",
            "Could not read djlint.toml: Invalid value",
            id="djlint.toml",
        ),
        pytest.param(
            ".djlint.toml",
            "indent =\n",
            "Could not read .djlint.toml: Invalid value",
            id=".djlint.toml",
        ),
        pytest.param(
            ".djlintrc",
            "{indent: 2}",
            "Could not read .djlintrc: Expecting property name enclosed in double quotes",
            id=".djlintrc",
        ),
        pytest.param(
            ".djlintrc", "[1]", "Could not read .djlintrc: ", id=".djlintrc holding no object"
        ),
    ],
)
def test_a_broken_project_file_is_a_usage_error(
    tmp_path: Path, name: str, content: str, message: str
) -> None:
    """Running on with the defaults would check against rules nobody chose."""
    (tmp_path / name).write_text(content, encoding="utf-8")

    with pytest.raises(UsageError, match=re.escape(message)):
        Config(str(tmp_path))


def test_a_broken_named_configuration_is_a_usage_error(tmp_path: Path) -> None:
    configuration = tmp_path / "settings.toml"
    configuration.write_text("indent =\n", encoding="utf-8")

    with pytest.raises(UsageError, match=re.escape(f"Could not read {configuration}: Invalid")):
        Config(str(tmp_path), configuration=configuration)


def test_a_broken_rules_file_is_a_usage_error(tmp_path: Path) -> None:
    rules = tmp_path / ".djlint_rules.yaml"
    rules.write_text("- rule: [\n", encoding="utf-8")

    with pytest.raises(UsageError, match=re.escape(f"Could not read {rules}: ")):
        Config(str(tmp_path))


def test_an_empty_rules_file_holds_no_rules(tmp_path: Path) -> None:
    (tmp_path / "with").mkdir()
    (tmp_path / "with" / ".djlint_rules.yaml").write_text("", encoding="utf-8")
    (tmp_path / "with" / ".git").mkdir()
    (tmp_path / "without").mkdir()
    (tmp_path / "without" / ".git").mkdir()

    assert (
        Config(str(tmp_path / "with")).linter_rules
        == Config(str(tmp_path / "without")).linter_rules
    )


def test_a_broken_config_fails_the_run(runner: CliRunner, tmp_path: Path) -> None:
    """Exit 2, as for a bad command line, whatever --warn says."""
    (tmp_path / "djlint.toml").write_text("indent =\n", encoding="utf-8")
    (tmp_path / "a.html").write_text("<div></div>\n", encoding="utf-8")

    result = runner.invoke(djlint, (str(tmp_path), "--lint", "--warn"))

    assert result.exit_code == 2
    assert "Error: Could not read djlint.toml: Invalid value" in result.stderr
    assert "Traceback" not in result.output


@pytest.mark.parametrize(
    ("name", "content"),
    [
        pytest.param(
            "pyproject.toml", '[tool.djlint]\nmax_line_length = "wide"\n', id="pyproject.toml"
        ),
        pytest.param("djlint.toml", 'max_line_length = "wide"\n', id="djlint.toml"),
        pytest.param(".djlint.toml", 'max_line_length = "wide"\n', id=".djlint.toml"),
        pytest.param(".djlintrc", '{"max_line_length": "wide"}', id=".djlintrc"),
    ],
)
def test_a_setting_that_is_no_number_is_a_usage_error(
    tmp_path: Path, name: str, content: str
) -> None:
    (tmp_path / name).write_text(content, encoding="utf-8")

    with pytest.raises(UsageError, match=re.escape(f"Invalid {name} max_line_length value wide")):
        Config(str(tmp_path))


@pytest.mark.parametrize("prefer_configuration", [False, True])
def test_a_setting_that_is_no_number_names_the_file_it_came_from(
    tmp_path: Path, *, prefer_configuration: bool
) -> None:
    (tmp_path / "djlint.toml").write_text('indent = "wide"\n', encoding="utf-8")
    configuration = tmp_path / "settings.toml"
    configuration.write_text('indent = "deep"\n', encoding="utf-8")
    expected = (
        f"Invalid {configuration} indent value deep"
        if prefer_configuration
        else "Invalid djlint.toml indent value wide"
    )

    with pytest.raises(UsageError, match=re.escape(expected)):
        Config(
            str(tmp_path), configuration=configuration, prefer_configuration=prefer_configuration
        )


def test_a_quote_style_from_a_file_is_checked(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text('quote_style = "backtick"\n', encoding="utf-8")

    with pytest.raises(BadParameter, match=r"Invalid quote style 'backtick'\. Choose from"):
        Config(str(tmp_path))


def test_a_mercurial_checkout_is_a_project_root(tmp_path: Path) -> None:
    (tmp_path / ".hg").mkdir()
    templates = tmp_path / "templates"
    templates.mkdir()

    assert find_project_root(templates) == tmp_path
