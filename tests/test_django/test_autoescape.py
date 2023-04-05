"""Test django autoescape tag.

poetry run pytest tests/test_django/test_autoescape.py
"""

import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% autoescape on %}{{ body }}{% endautoescape %}"),
        ("{% autoescape on %}\n" "    {{ body }}\n" "{% endautoescape %}\n"),
        id="autoescape_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
