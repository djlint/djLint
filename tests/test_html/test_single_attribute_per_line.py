"""Test single attribute per line.

pytest tests/test_html/test_single_attribute_per_line.py

"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '<div data-a="1">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="1" data-b="2" data-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="Lorem ipsum dolor sit amet" data-b="Lorem ipsum dolor sit amet" data-c="Lorem ipsum dolor sit amet">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-long-attribute-a="1" data-long-attribute-b="2" data-long-attribute-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            '<img src="/images/foo.png" alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />\n'
        ),
        (
            '<div data-a="1">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            "<div\n"
            '    data-a="1"\n'
            '    data-b="2"\n'
            '    data-c="3"\n'
            ">\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            "<div\n"
            '    data-a="Lorem ipsum dolor sit amet"\n'
            '    data-b="Lorem ipsum dolor sit amet"\n'
            '    data-c="Lorem ipsum dolor sit amet"\n'
            ">\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            "<div\n"
            '    data-long-attribute-a="1"\n'
            '    data-long-attribute-b="2"\n'
            '    data-long-attribute-c="3"\n'
            ">\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<img src="/images/foo.png" />\n'
            "<img\n"
            '    src="/images/foo.png"\n'
            '    alt="bar"\n'
            "/>\n"
            "<img\n"
            '    src="/images/foo.png"\n'
            '    alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit."\n'
            "/>\n"
        ),
        id="single_attrib_per_line_enabled",
    ),
    pytest.param(
        (
            '<div data-a="1">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="1" data-b="2" data-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="Lorem ipsum dolor sit amet" data-b="Lorem ipsum dolor sit amet" data-c="Lorem ipsum dolor sit amet">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-long-attribute-a="1" data-long-attribute-b="2" data-long-attribute-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            '<img src="/images/foo.png" alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />\n'
        ),
        (
            '<div data-a="1">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-a="1" data-b="2" data-c="3">\n'
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            "<div\n"
            '    data-a="Lorem ipsum dolor sit amet"\n'
            '    data-b="Lorem ipsum dolor sit amet"\n'
            '    data-c="Lorem ipsum dolor sit amet"\n'
            ">\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            "<div\n"
            '    data-long-attribute-a="1"\n'
            '    data-long-attribute-b="2"\n'
            '    data-long-attribute-c="3"\n'
            ">\n"
            "    Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            "<img\n"
            '    src="/images/foo.png"\n'
            '    alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit."\n'
            "/>\n"
        ),
        id="single_attrib_per_line_disabled",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
