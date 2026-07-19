"""Test pyproject.toml config with list values.

https://github.com/djlint/djLint/issues/776

uv run pytest tests/test_config/test_pyproject_list

"""

from __future__ import annotations

from pathlib import Path

from djlint.settings import Config


def test_list_settings() -> None:
    config = Config(str(Path(__file__) / "blank.html"))

    assert config.exclude == "foo/excluded.html | excluded.html"
    assert config.blank_line_after_tag == "load,extends,include"
    assert config.blank_line_before_tag == "load,extends,include"
    assert config.custom_blocks == r"|endexample\b|endtoc\b|example\b|toc\b"
    assert config.custom_html == r"|mjml|simple-greeting|mj-\w+|c-[\w.-]+"
    assert config.ignore == "H014,H015"
    assert config.ignore_blocks == r"endexample\b|endraw\b|example\b|raw\b"
    assert config.include == "H014,H015"
    assert all(
        rule["rule"]["name"] not in {"H014", "H015"}
        for rule in config.linter_rules
    )
