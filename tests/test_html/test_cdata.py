"""Test cdata.

poetry run pytest tests/test_html/test_cdata.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<span><![CDATA[<sender>John Smith</sender>]]></span>\n"
            "<span><![CDATA[1]]> a <![CDATA[2]]></span>\n"
            "<span><![CDATA[1]]> <br> <![CDATA[2]]></span>\n"
        ),
        (
            "<span><![CDATA[<sender>John Smith</sender>]]></span>\n"
            "<span><![CDATA[1]]> a <![CDATA[2]]></span>\n"
            "<span\n"
            "    ><![CDATA[1]]> <br />\n"
            "    <![CDATA[2]]></span\n"
            ">\n"
        ),
        id="cdata",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
