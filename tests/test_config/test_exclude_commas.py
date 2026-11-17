"""Test that a comma inside an exclude regex stays in it.

uv run pytest tests/test_config/test_exclude_commas.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.settings import Config

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("value", "excluded", "kept"),
    [
        (r"report[0-9]{1,2}\.html", ["report1.html", "report12.html"], ["report123.html"]),
        (r"[,;]tmp\.html,vendor", [",tmp.html", "vendor/a.html"], ["tmp.html"]),
        (r"a\,b\.html,build", ["a,b.html", "build/a.html"], ["a.html"]),
    ],
)
def test_commas_inside_a_regex_belong_to_it(
    tmp_path: Path, value: str, excluded: list[str], kept: list[str]
) -> None:
    pattern = Config(str(tmp_path), exclude=value).exclude_pattern

    assert [path for path in excluded if not pattern.search(path)] == []
    assert [path for path in kept if pattern.search(path)] == []


def test_a_list_in_the_config_file_keeps_its_commas(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text(
        'extend_exclude = ["report[0-9]{1,2}\\\\.html"]\n', encoding="utf-8"
    )

    assert Config(str(tmp_path)).exclude_pattern.search("report12.html")
