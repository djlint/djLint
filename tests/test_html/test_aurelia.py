"""Tests for Aurelia.

poetry run pytest tests/test_html/test_aurelia.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<template>\n" '    <i class.bind="icon"></i>\n' "</template>\n"),
        ("<template>\n" '    <i class.bind="icon"></i>\n' "</template>\n"),
        id="aurelia",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
