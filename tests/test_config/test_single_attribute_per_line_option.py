"""Test for single_attribute_per_line.

uv run pytest tests/test_config/test_single_attribute_per_line_option.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any


test_data = [
    pytest.param(
        (
            '<input type="text" name="firstName" id="first-name" '
            'autocomplete="given-name" class="form-input mt-1" '
            'value="{{ user.firstName }}" />\n'
        ),
        (
            "<input\n"
            '  type="text"\n'
            '  name="firstName"\n'
            '  id="first-name"\n'
            '  autocomplete="given-name"\n'
            '  class="form-input mt-1"\n'
            '  value="{{ user.firstName }}"\n'
            "/>\n"
        ),
        {"indent": 2, "max_line_length": 1},
        id="prettier_like",
    ),
    pytest.param(
        (
            '<link rel="apple-touch-icon" sizes="180x180" '
            'href="{% static "img/fav/apple-touch-icon.png" %}" />\n'
        ),
        (
            "<link\n"
            '  rel="apple-touch-icon"\n'
            '  sizes="180x180"\n'
            '  href="{% static "img/fav/apple-touch-icon.png" %}"\n'
            "/>\n"
        ),
        {"indent": 2, "max_attribute_length": 1, "profile": "django"},
        id="issue_1877",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    args = {**args, "single_attribute_per_line": True}
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output


def test_default_keeps_hanging_indent() -> None:
    source = (
        '<input type="text" name="firstName" id="first-name" '
        'autocomplete="given-name" class="form-input mt-1" />\n'
    )
    output = formatter(
        config_builder({"indent": 2, "max_line_length": 1}), source
    )

    assert output.startswith('<input type="text"\n       name=')
