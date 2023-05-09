"""Tests html details/summary tag.

poetry run pytest tests/test_html/test_tag_details_summary.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            '<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">string</div>\n'
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
        ),
        ({}),
        id="no_line_break_after_multiline_tag",
    ),
    pytest.param(
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    string\n"
            "</div>\n"
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
        ),
        ({}),
        id="no_line_break_after_multiline_tag_when_already_split",
    ),
    pytest.param(
        (
            '<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">string</div>\n'
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    string\n"
            "</div>\n"
        ),
        ({"line_break_after_multiline_tag": True}),
        id="line_break_after_multiline_tag",
    ),
    pytest.param(
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    string\n"
            "</div>\n"
        ),
        ({"line_break_after_multiline_tag": True}),
        id="line_break_after_multiline_tag_when_already_condensed",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
