"""Test html hr tag.

pytest tests/test_html/test_tag_hr.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<div>\n" "    <div>\n" "        <hr>\n" "    </div>\n" "</div>\n"),
        ("<div>\n" "    <div>\n" "        <hr />\n" "    </div>\n" "</div>\n"),
        id="hr",
    ),
    pytest.param(
        ("<div>\n" "    <div>\n" "        <hr />\n" "    </div>\n" "</div>\n"),
        ("<div>\n" "    <div>\n" "        <hr />\n" "    </div>\n" "</div>\n"),
        id="hr_void",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
