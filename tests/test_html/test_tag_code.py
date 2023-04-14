"""Test html code tag.

pytest tests/test_html/test_tag_code.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<ol>\n" "    <li>\n" "        <code>a</code> b\n" "    </li>\n" "</ol>\n"),
        ("<ol>\n" "    <li><code>a</code> b</li>\n" "</ol>\n"),
        id="code_tag",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
