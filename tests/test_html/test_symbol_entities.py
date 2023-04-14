"""Test symbol entities.

pytest tests/test_html/test_symbol_entities.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

# seems to be a bug in the parser, it is returning symbol ents as the actual char.
test_data = [
    pytest.param(
        (
            "<p>I will display &euro;</p>\n"
            "<p>I will display &excl;</p>\n"
            "<p>I will display &#8364;</p>\n"
            "<p>I will display &#x20AC;</p>\n"
        ),
        (
            "<p>I will display &euro;</p>\n"
            "<p>I will display &excl;</p>\n"
            "<p>I will display &#8364;</p>\n"
            "<p>I will display &#x20AC;</p>\n"
        ),
        id="symbol_entities",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
