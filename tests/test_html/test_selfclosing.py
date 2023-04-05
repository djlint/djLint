"""Test self closing tags.

poetry run pytest tests/test_html/test_selfclosing.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

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
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
