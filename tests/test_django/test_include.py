"""Test django include tag.

poetry run pytest tests/test_django/test_include.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ('{% include "this" %}{% include "that" %}'),
        ('{% include "this" %}\n' '{% include "that" %}\n'),
        id="include_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
