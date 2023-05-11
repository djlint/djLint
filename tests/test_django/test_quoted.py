"""Test django quoted tags.

poetry run pytest tests/test_django/test_filter.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<h1>\n"
            '    {% if condition1 %}<span class="cls"></span>{% endif %}\n'
            ' {% if condition2 %}"{{ text }}"{% endif %}\n'
            "     </h1>\n"
        ),
        (
            "<h1>\n"
            '    {% if condition1 %}<span class="cls"></span>{% endif %}\n'
            '    {% if condition2 %}"{{ text }}"{% endif %}\n'
            "</h1>\n"
        ),
        id="issue #640",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
