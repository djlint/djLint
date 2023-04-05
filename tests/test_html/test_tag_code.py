"""Test html code tag.

poetry run pytest tests/test_html/test_tag_code.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("<ol>\n" "    <li>\n" "        <code>a</code> b\n" "    </li>\n" "</ol>\n"),
        ("<ol>\n" "    <li>\n" "        <code>a</code> b\n" "    </li>\n" "</ol>\n"),
        id="code_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
