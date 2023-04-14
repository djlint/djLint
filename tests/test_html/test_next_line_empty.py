"""Test next line empty.

poetry run pytest tests/test_html/test_next_line_empty.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<div></div\n"
            ">\n"
            "<span></span>\n"
            "<div></div\n"
            "\n"
            "\n"
            "           >\n"
            "<span></span>\n"
            "<div></div\n"
            ">\n"
            "<span></span>\n"
            "<div>\n"
            '  <a href="#123123123123123131231312321312312312312312312312312313123123123123123"\n'
            "    >123123123123</a\n"
            "  >\n"
            "  123123\n"
            "</div>\n"
        ),
        (
            "<div></div>\n"
            "<span></span>\n"
            "<div></div>\n"
            "<span></span>\n"
            "<div></div>\n"
            "<span></span>\n"
            "<div>\n"
            "    <a\n"
            '        href="#123123123123123131231312321312312312312312312312312313123123123123123"\n'
            "        >123123123123</a\n"
            "    >\n"
            "    123123\n"
            "</div>\n"
        ),
        id="standalone_end_marker",
    )
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
