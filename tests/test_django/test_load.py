"""Test django load tag.

uv run pytest tests/test_django/test_load.py
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
        ("{% block content %}{% load i18n %}{% endblock %}"),
        ("{% block content %}\n    {% load i18n %}\n{% endblock %}\n"),
        id="load_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
