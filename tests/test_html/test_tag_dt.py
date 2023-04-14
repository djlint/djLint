"""Test html dt tag.

pytest tests/test_html/test_tag_dt.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        "<dt>text</dt>",
        ("<dt>text</dt>\n"),
        id="dt_tag",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
