"""Test attributes guarded by a template tag under single_attribute_per_line.

uv run pytest tests/test_config/test_guarded_attributes_per_line.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        '<div class="list-group-item" {% if comments is None %}'
        ' hx-get="{% url "blog:comments" post.pk %}" hx-trigger="revealed"'
        ' hx-swap="afterend" {% endif %}>x</div>\n',
        "<div\n"
        '  class="list-group-item"\n'
        "  {% if comments is None %}\n"
        '    hx-get="{% url "blog:comments" post.pk %}"\n'
        '    hx-trigger="revealed"\n'
        '    hx-swap="afterend"\n'
        "  {% endif %}\n"
        ">x</div>\n",
        id="guarded_attributes_take_a_line_each",
    ),
    pytest.param(
        '<div class="list-group-item card shadow-sm border-0 rounded-3 p-4"'
        ' {% if comments is None %} hx-trigger="revealed" {% endif %}>x</div>\n',
        "<div\n"
        '  class="list-group-item card shadow-sm border-0 rounded-3 p-4"\n'
        "  {% if comments is None %}\n"
        '    hx-trigger="revealed"\n'
        "  {% endif %}\n"
        ">x</div>\n",
        id="a_single_guarded_attribute_still_takes_one_line",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_guarded_attributes_per_line(source: str, expected: str) -> None:
    config = config_builder({
        "profile": "django",
        "indent": 2,
        "max_line_length": 80,
        "format_attribute_template_tags": True,
        "single_attribute_per_line": True,
    })

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
