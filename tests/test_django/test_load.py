"""Test django load tag.

poetry run pytest tests/test_django/test_load.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% block content %}{% load i18n %}{% endblock %}"),
        ("{% block content %}\n" "    {% load i18n %}\n" "{% endblock %}\n"),
        id="load_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
