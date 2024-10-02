"""Test self closing tags.

uv run pytest tests/test_html/test_selfclosing.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        (
            "<p><span>Hello</span> <br /><input /><link /><img /><source /><meta /> <span>World</span></p>\n"
        ),
        (
            "<p>\n"
            "    <span>Hello</span>\n"
            "    <br />\n"
            "    <input />\n"
            "    <link />\n"
            "    <img />\n"
            "    <source />\n"
            "    <meta />\n"
            "    <span>World</span>\n"
            "</p>\n"
        ),
        id="self_closing",
    ),
    pytest.param(
        (
            "<p><span>Hello</span> <br><input><link><img><source><meta> <span>World</span></p>\n"
        ),
        (
            "<p>\n"
            "    <span>Hello</span>\n"
            "    <br>\n"
            "    <input>\n"
            "    <link>\n"
            "    <img>\n"
            "    <source>\n"
            "    <meta>\n"
            "    <span>World</span>\n"
            "</p>\n"
        ),
        id="void_self_closing",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
