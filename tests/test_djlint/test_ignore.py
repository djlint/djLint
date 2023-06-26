"""Test disable.

poetry run pytest tests/test_djlint/test_ignore.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{# djlint:off #}\n" "<img \n" "/>"),
        ("{# djlint:off #}\n" "<img \n" "/>\n"),
        id="don't compress",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
