"""Test bracket on same line flag.

poetry run pytest tests/test_html/test_bracket_same_line.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</div>\n"
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>\n'
            '<div class="a">\n'
            "text\n"
            "</div>\n"
            '<div class="a">text</div>\n'
        ),
        (
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</div>\n'
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>\n'
            '<div class="a">text</div>\n'
            '<div class="a">text</div>\n'
        ),
        id="block",
    ),
    pytest.param(
        (
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</div>\n"
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>\n'
            '<div class="a">\n'
            "text\n"
            "</div>\n"
            '<div class="a">text</div>\n'
        ),
        (
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</div>\n'
            '<div long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>\n'
            '<div class="a">text</div>\n'
            '<div class="a">text</div>\n'
        ),
        id="block_bracket_same_line",
    ),
    pytest.param(
        (
            '<script long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "alert(1)</script>\n"
            '<style long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            ".a{color: #f00}</style>\n"
            "<script>\n"
            "alert(1)</script>\n"
            "<style>\n"
            ".a{color: #f00}</style>\n"
        ),
        (
            '<script long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">alert(1)</script>\n'
            '<style long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">.a{color: #f00}</style>\n'
            "<script>alert(1)</script>\n"
            "<style>.a{color: #f00}</style>\n"
        ),
        id="embed",
    ),
    pytest.param(
        (
            '<script long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "alert(1)</script>\n"
            '<style long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            ".a{color: #f00}</style>\n"
            "<script>\n"
            "alert(1)</script>\n"
            "<style>\n"
            ".a{color: #f00}</style>\n"
        ),
        (
            '<script long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">alert(1)</script>\n'
            '<style long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">.a{color: #f00}</style>\n'
            "<script>alert(1)</script>\n"
            "<style>.a{color: #f00}</style>\n"
        ),
        id="embed_bracket_same_line",
    ),
    pytest.param(
        (
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</span>\n"
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>\n'
            '<span  class="a">text</span>\n'
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</span>\n"
            '<span  class="a">text</span><span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</span>\n"
            '<span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span>\n'
        ),
        (
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</span>\n'
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>\n'
            '<span class="a">text</span>\n'
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</span>\n'
            '<span class="a">text</span><span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</span>\n'
            '<span class="a">text</span><span class="a">text</span><span class="a">text</span><span class="a">text</span><span class="a">text</span>\n'
        ),
        id="inline",
    ),
    pytest.param(
        (
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</span>\n"
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>\n'
            '<span  class="a">text</span>\n'
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</span>\n"
            '<span  class="a">text</span><span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "text\n"
            "</span>\n"
            '<span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span><span  class="a">text</span>\n'
        ),
        (
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</span>\n'
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>\n'
            '<span class="a">text</span>\n'
            '<span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</span>\n'
            '<span class="a">text</span><span long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">text</span>\n'
            '<span class="a">text</span><span class="a">text</span><span class="a">text</span><span class="a">text</span><span class="a">text</span>\n'
        ),
        id="inline_bracket_same_line",
    ),
    pytest.param(
        (
            '<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value" src="./1.jpg"/>\n'
            '<img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/>\n'
        ),
        (
            '<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            '     src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
        ),
        id="void",
    ),
    pytest.param(
        (
            '<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value" src="./1.jpg"/>\n'
            '<img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/>\n'
        ),
        (
            '<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            '     src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
            '<img src="./1.jpg" />\n'
        ),
        id="void_braket_same_line",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
