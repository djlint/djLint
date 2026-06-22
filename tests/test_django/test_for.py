"""Test django for tag.

uv run pytest tests/test_django/test_for.py
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
        (
            "<ul>{% for athlete in athlete_list %}<li>{{ athlete.name }}</li>{% empty %}<li>Sorry, no athletes in this list.</li>{% endfor %}</ul>"
        ),
        (
            "<ul>\n"
            "    {% for athlete in athlete_list %}\n"
            "        <li>{{ athlete.name }}</li>\n"
            "    {% empty %}\n"
            "        <li>Sorry, no athletes in this list.</li>\n"
            "    {% endfor %}\n"
            "</ul>\n"
        ),
        id="for_tag",
    ),
    pytest.param(
        (
            "{% for i in items %}\n"
            "    <div>{% formfield i %}</div>\n"
            "{% endfor %}"
        ),
        (
            "{% for i in items %}\n"
            "    <div>{% formfield i %}</div>\n"
            "{% endfor %}\n"
        ),
        id="test nested formfield",
    ),
    pytest.param(
        (
            '<div class="form-inputs plans-form">\n'
            '    <div class="trans-wrapper pos-comparator-flex">\n'
            "        {% for field in POSOptimizer %}\n"
            "            <div>\n"
            "                <label>{{ field.label }}</label>\n"
            "                {% formfield field show_label=False %}\n"
            "            </div>\n"
            "        {% endfor %}\n"
            "        <div>\n"
            "            <label>&nbsp</label>\n"
            '            <button type="submit">{% trans "Calcola" %}</button>\n'
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
        ),
        (
            '<div class="form-inputs plans-form">\n'
            '    <div class="trans-wrapper pos-comparator-flex">\n'
            "        {% for field in POSOptimizer %}\n"
            "            <div>\n"
            "                <label>{{ field.label }}</label>\n"
            "                {% formfield field show_label=False %}\n"
            "            </div>\n"
            "        {% endfor %}\n"
            "        <div>\n"
            "            <label>&nbsp</label>\n"
            '            <button type="submit">{% trans "Calcola" %}</button>\n'
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="test nested formfield inside for",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output


def test_issue_2098_child_template_inline_for_idempotent(
    django_config: Config,
) -> None:
    source = (
        '    <form id="my-form"\n'
        "          action=\"{% url 'some-view-name' object.identifier %}{% if request.GET.show_extra == 'true' %}?show_extra=true{% endif %}\"\n"
        '              {{ form.first_field|add_class:"form-control"|add_error_class:"is-invalid" }}\n'
        '              {% for error in form.first_field.errors %}<div class="invalid-feedback">{{ error }}</div>{% endfor %}\n'
        "              {% for error in extra_errors.first_field %}\n"
        '                <div class="form-text text-danger">{{ error }}</div>\n'
        "              {% endfor %}\n"
        '              {% for error in extra_errors.second_field %}<div class="form-text text-danger">{{ error }}</div>{% endfor %}\n'
        '              {% for error in form.third_field.errors %}<div class="invalid-feedback">{{ error }}</div>{% endfor %}\n'
        '              {% for error in extra_errors.third_field %}<div class="form-text text-danger">{{ error }}</div>{% endfor %}\n'
    )

    output = formatter(django_config, source)
    second_output = formatter(django_config, output)

    printer(output, source, second_output)
    assert output == second_output
