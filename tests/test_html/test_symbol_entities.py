"""Test symbol entities.

poetry run pytest tests/test_html/test_symbol_entities.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

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


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
