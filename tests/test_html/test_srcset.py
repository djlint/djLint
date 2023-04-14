"""Test srcset.

pytest tests/test_html/test_srcset.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '<img src="a"\n'
            'srcset="\n'
            " should-not-format  400w 100h,\n"
            "       should-not-format  500w 200h\n"
            '"\n'
            ' alt=""/>\n'
            '<img src="a"\n'
            'srcset="\n'
            " should-not-format ,, should-not-format 0q,,,\n"
            '"\n'
            ' alt=""/>\n'
        ),
        (
            "<img\n"
            '    src="a"\n'
            '    srcset="\n'
            " should-not-format  400w 100h,\n"
            "       should-not-format  500w 200h\n"
            '"\n'
            '    alt=""\n'
            "/>\n"
            "<img\n"
            '    src="a"\n'
            '    srcset="\n'
            " should-not-format ,, should-not-format 0q,,,\n"
            '"\n'
            '    alt=""\n'
            "/>\n"
        ),
        id="invalid",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
