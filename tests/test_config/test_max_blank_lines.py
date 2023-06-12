"""Test for max blank lines.

poetry run pytest tests/test_config/test_max_blank_lines.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("<img>\n\n\n\n\n\n\n\n\n\n<meta>"),
        ("<img>\n" "<meta>\n"),
        ({}),
        id="default",
    ),
    pytest.param(
        ("<img>\n\n\n\n\n\n\n\n\n\n<meta>"),
        ("<img>\n\n\n\n\n\n" "<meta>\n"),
        ({"max_blank_lines": 5}),
        id="5",
    ),
    pytest.param(
        ("<img>\n\n\n\n\n\n\n\n\n\n<meta>"),
        ("<img>\n\n" "<meta>\n"),
        ({"max_blank_lines": 1}),
        id="1",
    ),
    pytest.param(
        ("<img>\n\n\n\n\n\n\n\n\n\n<meta>"),
        ("<img>\n" "<meta>\n"),
        ({"max_blank_lines": -1}),
        id="-1",
    ),
    pytest.param(
        ("<img>\n\n\n\n\n\n\n\n\n\n<meta>"),
        ("<img>\n\n\n\n\n\n\n\n\n\n" "<meta>\n"),
        ({"max_blank_lines": 30}),
        id="30",
    ),
    pytest.param(
        ("<img>\n\n<div>\n\n<p>\n\n</p>\n\n</div>\n\n<meta>"),
        ("<img>\n" "\n" "<div>\n" "\n" "    <p></p>\n" "\n" "</div>\n" "\n" "<meta>\n"),
        ({"max_blank_lines": 30}),
        id="div",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
