"""Test golang if tag.

poetry run pytest tests/test_golang/test_if.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{{ if .condition }} {{ else }} {{ end }}"),
        ("{{ if .condition }} {{ else }} {{ end }}\n"),
        id="if_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
