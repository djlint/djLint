"""Test configuration files and values djLint cannot read.

uv run pytest tests/test_config/test_unreadable_config.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from click import BadParameter

from djlint.settings import Config, find_project_root

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("name", "content", "message"),
    [
        pytest.param(
            "pyproject.toml",
            "[tool.djlint\n",
            "Failed to load pyproject.toml file. Expected ']' at the end of a table declaration",
            id="pyproject.toml",
        ),
        pytest.param(
            "djlint.toml",
            "indent =\n",
            "Failed to load djlint.toml file. Invalid value",
            id="djlint.toml",
        ),
        pytest.param(
            ".djlint.toml",
            "indent =\n",
            "Failed to load .djlint.toml file. Invalid value",
            id=".djlint.toml",
        ),
        pytest.param(
            ".djlintrc",
            "{indent: 2}",
            "Failed to load .djlintrc file. Expecting property name enclosed in double quotes",
            id=".djlintrc",
        ),
        pytest.param(
            ".djlintrc", "[1]", "Failed to load .djlintrc file.", id=".djlintrc holding no object"
        ),
    ],
)
def test_a_broken_project_file_falls_back_to_the_defaults(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], name: str, content: str, message: str
) -> None:
    (tmp_path / name).write_text(content, encoding="utf-8")

    config = Config(str(tmp_path))

    assert message in capsys.readouterr().err
    assert config.indent == 4 * " "


def test_a_broken_named_configuration_falls_back_to_the_defaults(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    configuration = tmp_path / "settings.toml"
    configuration.write_text("indent =\n", encoding="utf-8")

    config = Config(str(tmp_path), configuration=configuration)

    assert f"Failed to load config file {configuration}. Invalid value" in capsys.readouterr().err
    assert config.indent == 4 * " "


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
def test_a_setting_that_is_no_number_keeps_its_default(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], name: str, content: str
) -> None:
    (tmp_path / name).write_text(content, encoding="utf-8")

    config = Config(str(tmp_path))

    assert f"Error: Invalid {name} max_line_length value wide" in capsys.readouterr().err
    assert config.max_line_length == 120


@pytest.mark.parametrize("prefer_configuration", [False, True])
def test_a_setting_that_is_no_number_names_the_file_it_came_from(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], *, prefer_configuration: bool
) -> None:
    (tmp_path / "djlint.toml").write_text('indent = "wide"\n', encoding="utf-8")
    configuration = tmp_path / "settings.toml"
    configuration.write_text('max_line_length = "long"\nindent = "deep"\n', encoding="utf-8")

    Config(str(tmp_path), configuration=configuration, prefer_configuration=prefer_configuration)

    err = capsys.readouterr().err
    assert f"Error: Invalid {configuration} max_line_length value long" in err
    if prefer_configuration:
        assert f"Error: Invalid {configuration} indent value deep" in err
    else:
        assert "Error: Invalid djlint.toml indent value wide" in err


def test_a_quote_style_from_a_file_is_checked(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text('quote_style = "backtick"\n', encoding="utf-8")

    with pytest.raises(BadParameter, match=r"Invalid quote style 'backtick'\. Choose from"):
        Config(str(tmp_path))


def test_a_mercurial_checkout_is_a_project_root(tmp_path: Path) -> None:
    (tmp_path / ".hg").mkdir()
    templates = tmp_path / "templates"
    templates.mkdir()

    assert find_project_root(templates) == tmp_path
