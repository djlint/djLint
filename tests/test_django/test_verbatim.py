"""Test django verbatim tag.

poetry run pytest tests/test_django/test_verbatim.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% verbatim %}Still alive.{% endverbatim %}"),
        ("{% verbatim %}\n" "    Still alive.\n" "{% endverbatim %}\n"),
        id="verbatim_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
