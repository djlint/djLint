"""Test for custom html.

poetry run pytest tests/test_config/test_close_void_tags.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("<img><meta>"),
        ("<img>\n" "<meta>\n"),
        ({}),
        id="default",
    ),
    pytest.param(
        ("<img><div><meta>"),
        ("<img />\n" "<div>\n" "    <meta />\n"),
        ({"close_void_tags": True}),
        id="config",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
