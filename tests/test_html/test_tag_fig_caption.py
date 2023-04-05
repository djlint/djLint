"""Test html figure tag.

poetry run pytest tests/test_html/test_tag_fig_caption.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ('<figure><img src="" alt=""><figcaption>caption</figcaption></figure>'),
        (
            "<figure>\n"
            '    <img src="" alt="">\n'
            "    <figcaption>caption</figcaption>\n"
            "</figure>\n"
        ),
        id="figure_figcaption_tags",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
