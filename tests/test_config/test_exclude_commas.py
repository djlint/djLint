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
        # A bracket in a comment opens nothing, so the comma still ends it.
        ("legacy # generated {,vendor", ["legacy/a.html", "vendor/a.html"], ["a.html"]),
        ("legacy # see [1,vendor", ["legacy/a.html", "vendor/a.html"], ["a.html"]),
        # Verbose mode keeps an escaped space, so trimming leaves it too.
        ("legacy\\ ", ["legacy /a.html"], ["legacy/a.html"]),
        ("legacy\\ ,vendor", ["legacy /a.html", "vendor/a.html"], ["legacy/a.html"]),
        # A backslash in a comment escapes nothing, and a comment alone is no pattern.
        ("legacy # see \\,vendor", ["legacy/a.html", "vendor/a.html"], ["a.html"]),
        ("vendor, # note, build", ["vendor/a.html", "build/a.html"], ["templates/a.html"]),
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


def test_each_item_of_a_list_is_one_regex(tmp_path: Path) -> None:
    # A literal brace no longer pulls the next item into its regex.
    (tmp_path / "djlint.toml").write_text(
        'exclude = ["a{", "vendor", "b,c\\\\.html", "d\\\\ "]\n', encoding="utf-8"
    )

    pattern = Config(str(tmp_path)).exclude_pattern

    assert [
        path
        for path in ("a{/x.html", "vendor/x.html", "b,c.html", "d /x.html")
        if not pattern.search(path)
    ] == []
    assert not pattern.search("c.html")


@pytest.mark.parametrize(
    "setting",
    [
        'exclude = ""',
        "exclude = []",
        'extend_exclude = " "',
        'extend_exclude = [" "]',
        'exclude = ["# none yet"]',
    ],
)
def test_a_blank_list_excludes_nothing(tmp_path: Path, setting: str) -> None:
    (tmp_path / "djlint.toml").write_text(f"{setting}\n", encoding="utf-8")

    assert not Config(str(tmp_path)).exclude_pattern.search("templates/a.html")
