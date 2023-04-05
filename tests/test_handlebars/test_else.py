"""Test handlebars else tag.

poetry run pytest tests/test_handlebars/test_else.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{{^}}"),
        ("{{^}}\n"),
        id="else_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, handlebars_config):
    output = formatter(handlebars_config, source)

    printer(expected, source, output)
    assert expected == output
