"""Test .editorconfig defaults.

uv run pytest tests/test_config/test_editorconfig/test_config.py
"""

from __future__ import annotations

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import printer


def test_editorconfig_supplies_defaults() -> None:
    config = Config("tests/test_config/test_editorconfig/html.html")

    assert config.indent_size == 2
    assert config.max_line_length == 80

    output = formatter(config, "<div>\n<p>x</p>\n</div>\n")
    expected = "<div>\n  <p>x</p>\n</div>\n"
    printer(expected, "<div>...", output)
    assert output == expected


def test_cli_overrides_editorconfig() -> None:
    config = Config("tests/test_config/test_editorconfig/html.html", indent=4)

    assert config.indent_size == 4
    assert config.max_line_length == 80


def test_config_file_overrides_editorconfig() -> None:
    config = Config("tests/test_config/test_editorconfig_precedence/html.html")

    # pyproject.toml indent=3 beats .editorconfig indent_size=2
    assert config.indent_size == 3
    # not set anywhere else: built-in default
    assert config.max_line_length == 120
