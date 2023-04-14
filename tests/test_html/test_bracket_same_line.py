"""Test bracket on same line flag.

poetry run pytest tests/test_html/test_bracket_same_line.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
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
            "<div\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            ">\n"
            "    text\n"
            "</div>\n"
            "<div\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            "></div>\n"
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
            "<div\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "    text\n"
            "</div>\n"
            "<div\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></div>\n'
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
            "<script\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            ">\n"
            "    alert(1);\n"
            "</script>\n"
            "<style\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            ">\n"
            "    .a {\n"
            "      color: #f00;\n"
            "    }\n"
            "</style>\n"
            "<script>\n"
            "    alert(1);\n"
            "</script>\n"
            "<style>\n"
            "    .a {\n"
            "      color: #f00;\n"
            "    }\n"
            "</style>\n"
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
            "<script\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "    alert(1);\n"
            "</script>\n"
            "<style\n"
            '  long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "  .a {\n"
            "    color: #f00;\n"
            "  }\n"
            "</style>\n"
            "<script>\n"
            "    alert(1);\n"
            "</script>\n"
            "<style>\n"
            "  .a {\n"
            "    color: #f00;\n"
            "  }\n"
            "</style>\n"
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
            "<span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            ">\n"
            "    text\n"
            "</span>\n"
            "<span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            "></span>\n"
            '<span class="a">text</span>\n'
            "<span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            ">\n"
            "    text\n"
            "</span>\n"
            '<span class="a">text</span\n'
            "><span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            ">\n"
            "    text\n"
            "</span>\n"
            '<span class="a">text</span><span class="a">text</span><span class="a">text</span\n'
            '><span class="a">text</span><span class="a">text</span>\n'
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
            "<span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "    text\n"
            "</span>\n"
            "<span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"></span>\n'
            '<span class="a">text</span>\n'
            "<span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "    text\n"
            "</span>\n"
            '<span class="a">text</span\n'
            "><span\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value">\n'
            "    text\n"
            "</span>\n"
            '<span class="a">text</span><span class="a">text</span><span class="a">text</span\n'
            '><span class="a">text</span><span class="a">text</span>\n'
        ),
        id="inline_bracket_same_line",
    ),
    pytest.param(
        (
            '<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value" src="./1.jpg"/>\n'
            '<img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/>\n'
        ),
        (
            "<img\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            '    src="./1.jpg" />\n'
            '<img src="./1.jpg" /><img src="./1.jpg" /><img src="./1.jpg" /><img\n'
            '    src="./1.jpg" /><img src="./1.jpg" />\n'
        ),
        id="void",
    ),
    pytest.param(
        (
            '<img long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value" src="./1.jpg"/>\n'
            '<img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/><img src="./1.jpg"/>\n'
        ),
        (
            "<img\n"
            '    long_long_attribute="long_long_long_long_long_long_long_long_long_long_long_value"\n'
            '    src="./1.jpg" />\n'
            '<img src="./1.jpg" /><img src="./1.jpg" /><img src="./1.jpg" /><img\n'
            '    src="./1.jpg" /><img src="./1.jpg" />\n'
        ),
        id="void_braket_same_line",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
