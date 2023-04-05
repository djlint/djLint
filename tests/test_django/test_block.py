"""Test django block tag.

poetry run pytest tests/test_django/test_block.py
"""

import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% block content %}{% block scripts %}{% endblock %}{% endblock %}"),
        (
            "{% block content %}\n"
            "    {% block scripts %}{% endblock %}\n"
            "{% endblock %}\n"
        ),
        id="asset_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
