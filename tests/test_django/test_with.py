"""Test django with tag.

poetry run pytest tests/test_django/test_with.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "{% with total=business.employees.count %}{{ total }}<div>employee</div>{{ total|pluralize }}{% endwith %}"
        ),
        (
            "{% with total=business.employees.count %}\n"
            "    {{ total }}\n"
            "    <div>employee</div>\n"
            "    {{ total|pluralize }}\n"
            "{% endwith %}\n"
        ),
        id="with_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
