"""Test text.

poetry run pytest tests/test_html/test_text.py
"""
import pytest

from src.djlint.reformat import formatter
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
            "<a-long-long-long-element>foo bar foo bar\n"
            "    foo bar foo bar foo bar foo bar foo bar\n"
            "    foo bar foo bar</a-long-long-long-element>\n"
            "    <!-- The end tag should stay in 80 print width -->\n"
        ),
        id="tag_should_in_fill",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
