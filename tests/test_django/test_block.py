"""Test django block tag.

uv run pytest tests/test_django/test_block.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

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
        id="nested_block_tag",
    ),
    pytest.param(
        ("{% block title %}Prijava{% endblock title %}"),
        ("{% block title %}Prijava{% endblock title %}\n"),
        id="named_block_with_text",
    ),
    pytest.param(
        (
            "{% block title %}Nema nalog? "
            '<a href="{% url \'register\' %}">Registruj se</a>'
            "{% endblock title %}"
        ),
        (
            "{% block title %}Nema nalog? "
            '<a href="{% url \'register\' %}">Registruj se</a>'
            "{% endblock title %}\n"
        ),
        id="named_block_with_inline_html",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output


def test_named_block_with_text_ignores_multiline_tag_break() -> None:
    source = "{% block title %}Prijava{% endblock title %}\n"
    output = formatter(
        config_builder(
            {"profile": "django", "line_break_after_multiline_tag": True}
        ),
        source,
    )

    printer(source, source, output)
    assert source == output


def test_named_block_with_text_ignores_max_line_length() -> None:
    source = "{% block title %}Prijava{% endblock title %}\n"
    output = formatter(
        config_builder({"profile": "django", "max_line_length": 1}),
        source,
    )

    printer(source, source, output)
    assert source == output
