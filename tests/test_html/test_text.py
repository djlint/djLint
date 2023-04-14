"""Test text.

pytest tests/test_html/test_text.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<a-long-long-long-element>foo bar foo bar\n"
            "  foo bar foo bar foo bar foo bar foo bar\n"
            "  foo bar foo bar</a-long-long-long-element>\n"
            "<!-- The end tag should stay in 80 print width -->\n"
        ),
        (
            "<a-long-long-long-element\n"
            "    >foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo bar foo\n"
            "    bar</a-long-long-long-element\n"
            ">\n"
            "<!-- The end tag should stay in 80 print width -->\n"
        ),
        id="tag_should_in_fill",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
