"""Tests html details/summary tag.

poetry run pytest tests/test_html/test_tag_details_summary.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<details><summary>summary</summary>body</details>"),
        ("<details>\n" "    <summary>summary</summary>\n" "    body\n" "</details>\n"),
        id="details_summary_tags",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
