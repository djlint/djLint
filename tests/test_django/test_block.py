"""Test django block tag.

uv run pytest tests/test_django/test_block.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        ("{% block content %}{% block scripts %}{% endblock %}{% endblock %}"),
        (
            "{% block content %}\n"
            "    {% block scripts %}{% endblock %}\n"
            "{% endblock %}\n"
        ),
        id="asset_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
