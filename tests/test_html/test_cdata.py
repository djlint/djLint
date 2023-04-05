"""Test cdata.

poetry run pytest tests/test_html/test_cdata.py
"""
import pytest

from src.djlint.reformat import formatter
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
            "<span><![CDATA[1]]>\n"
            "    <br>\n"
            "<![CDATA[2]]></span>\n"
        ),
        id="cdata",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
