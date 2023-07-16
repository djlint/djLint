"""Test jinja parenthesis.

poetry run pytest tests/test_jinja/test_parenthesis.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        "{{ url('foo') }}",
        "{{ url('foo') }}\n",
        '{{ url("foo") }}\n',
        id="parenthesis_tag",
    )
]


@pytest.mark.parametrize(("source", "expected1", "expected2"), test_data)
def test_base(source, expected1, expected2, jinja_config):
    output = formatter(jinja_config, source)

    printer(expected1, source, output)
    assert expected1 == output or expected2 == output

    output = formatter(jinja_config, source)

    printer(expected2, source, output)
    assert expected1 == output or expected2 == output
