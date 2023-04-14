"""Test self closing tags.

poetry run pytest tests/test_html/test_selfclosing.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<p><span>Hello</span> <br /><input /><link /><img /><source /><meta /> <span>World</span></p>\n"
        ),
        (
            "<p>\n"
            "    <span>Hello</span> <br /><input /><link /><img />\n"
            "    <source />\n"
            "    <meta /> <span>World</span>\n"
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
            "    <span>Hello</span> <br /><input /><link /><img />\n"
            "    <source />\n"
            "    <meta /> <span>World</span>\n"
            "</p>\n"
        ),
        id="void_self_closing",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
