"""Test where each linter finding ends.

uv run pytest tests/test_linter/test_ranges.py
"""

from __future__ import annotations

import importlib
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter as djlint_linter
from djlint.settings import Config

if TYPE_CHECKING:
    from collections.abc import Iterator

    from djlint.types import LintError


def _offset(text: str, position: str) -> int:
    line, column = (int(part) for part in position.split(":"))
    lines = text.splitlines(keepends=True)
    return sum(len(x) for x in lines[: line - 1]) + column


@cache
def _config(profile: str) -> Config:
    return Config("-", profile=profile)


def _findings(text: str, profile: str = "django") -> list[LintError]:
    return djlint_linter(_config(profile), text, "t.html", "t.html")["t.html"]


def _spanned(text: str, finding: LintError) -> str:
    return text[_offset(text, finding["line"]) : _offset(text, finding["end"])]


@pytest.mark.parametrize(
    ("source", "code", "expected"),
    [
        pytest.param('<img src="x">', "H013", '<img src="x">', id="a pattern"),
        pytest.param(
            '<p>text</p>\n<img src="x">',
            "H013",
            '<img src="x">',
            id="a pattern on line 2",
        ),
        pytest.param(
            "<div>\n</section>",
            "H025",
            "<div>",
            id="a rule module with a token",
        ),
        pytest.param("<IMG>", "H009", "IMG", id="the match of a rule module"),
        pytest.param(
            "<div>{{a}}</div>", "T001", "{{a}}", id="a rule module with a match"
        ),
    ],
)
def test_finding_covers(source: str, code: str, expected: str) -> None:
    findings = [x for x in _findings(source) if x["code"] == code]
    assert findings
    assert _spanned(source, findings[0]) == expected


def test_a_finding_can_end_on_a_later_line() -> None:
    source = '<img\n  src="x">'
    (finding,) = [x for x in _findings(source) if x["code"] == "H013"]
    assert (finding["line"], finding["end"]) == ("1:0", "2:10")


def test_trailing_whitespace_is_left_out() -> None:
    source = '<img src="x">   \n<p>text</p>'
    (finding,) = [x for x in _findings(source) if x["code"] == "H013"]
    assert finding["end"] == "1:13"


def _rule_sources() -> Iterator[str]:
    for file in sorted(Path("tests/test_linter").glob("test_*.py")):
        module = importlib.import_module(f"tests.test_linter.{file.stem}")
        for param in getattr(module, "test_data", ()):
            source = param.values[0]
            if isinstance(source, str):
                yield source


def test_every_finding_has_a_range_inside_the_text() -> None:
    sources = tuple(_rule_sources())
    assert len(sources) > 100
    codes = set()
    for source in sources:
        for profile in ("django", "jinja", "handlebars"):
            for finding in _findings(source, profile):
                start = _offset(source, finding["line"])
                end = _offset(source, finding["end"])
                assert start <= end <= len(source), (source, finding)
                codes.add(finding["code"])
    assert len(codes) > 40
