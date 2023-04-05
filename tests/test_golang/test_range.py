"""Test golang range tag.

poetry run pytest tests/test_golang/test_range.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{{ range .Items }} {{ end }}"),
        ("{{ range .Items }} {{ end }}\n"),
        id="range_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
