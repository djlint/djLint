"""Test that a setting taking regexes reports a glob instead of crashing.

uv run pytest tests/test_config/test_invalid_regex.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from click import UsageError

from djlint.settings import Config

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("toml", "setting"),
    [
        ('exclude = ["*.min.html"]', "exclude"),
        ('extend_exclude = ["vendor", "*.min.html"]', "extend_exclude"),
        ('per-file-ignores = { "*.html" = "H013" }', "per-file-ignores"),
    ],
)
def test_a_glob_where_a_regex_goes_is_a_usage_error(
    tmp_path: Path, toml: str, setting: str
) -> None:
    (tmp_path / "djlint.toml").write_text(f"{toml}\n", encoding="utf-8")

    with pytest.raises(UsageError, match=rf"^Invalid {setting} .*\.\*\\\.min\\\.html\.$"):
        Config(str(tmp_path))


@pytest.mark.parametrize("toml", ['exclude = "legacy\\\\"', 'exclude = ["legacy\\\\"]'])
def test_a_trailing_backslash_is_a_usage_error(tmp_path: Path, toml: str) -> None:
    (tmp_path / "djlint.toml").write_text(f"{toml}\n", encoding="utf-8")

    with pytest.raises(UsageError, match=r"^Invalid exclude 'legacy\\\\'"):
        Config(str(tmp_path))


def test_a_comment_ends_with_its_entry(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text(
        'exclude = ["vendor # third-party", "build"]\nextend_exclude = ["legacy # old"]\n',
        encoding="utf-8",
    )

    pattern = Config(str(tmp_path)).exclude_pattern

    assert [
        path
        for path in ("vendor/a.html", "build/a.html", "legacy/a.html")
        if not pattern.search(path)
    ] == []
    assert not pattern.search("templates/a.html")


def test_regexes_still_work(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text(
        'extend_exclude = [".*\\\\.min\\\\.html"]\nper-file-ignores = { ".*\\\\.html" = "H013" }\n',
        encoding="utf-8",
    )

    config = Config(str(tmp_path))

    assert config.exclude_pattern.search("static/app.min.html")
    assert config.per_file_ignores == {r".*\.html": "H013"}
