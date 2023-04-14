"""Test html figure tag.

pytest tests/test_html/test_tag_fig_caption.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        ('<figure><img src="" alt=""><figcaption>caption</figcaption></figure>'),
        (
            "<figure>\n"
            '    <img src="" alt="" />\n'
            "    <figcaption>caption</figcaption>\n"
            "</figure>\n"
        ),
        id="figure_figcaption_tags",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
