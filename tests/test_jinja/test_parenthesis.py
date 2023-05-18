"""Test jinja parenthesis.

poetry run pytest tests/test_jinja/test_parenthesis.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{{ url('foo')}}"),
        ('{{ url("foo") }}\n'),
        id="parenthesis_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, jinja_config):
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
