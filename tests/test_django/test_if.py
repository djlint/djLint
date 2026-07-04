"""Test django if tag.

uv run pytest tests/test_django/test_if.py
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
        (
            "{% if athlete_list %}Number of athletes: {{ athlete_list|length }}{% elif athlete_in_locker_room_list %}Athletes should be out of the locker room soon!{% else %}No athletes.{% endif %}"
        ),
        (
            "{% if athlete_list %}Number of athletes: {{ athlete_list|length }}{% elif athlete_in_locker_room_list %}Athletes should be out of the locker room soon!{% else %}No athletes.{% endif %}\n"
        ),
        id="if_tag",
    ),
    pytest.param(
        (
            "{% if show_the_thing %}\n"
            "  <div>Please do not collapse this into a single line</div>\n"
            "{% endif %}\n"
        ),
        (
            "{% if show_the_thing %}\n"
            "    <div>Please do not collapse this into a single line</div>\n"
            "{% endif %}\n"
        ),
        id="issue_1597_preserve_multiline_short_if",
    ),
    pytest.param(
        (
            "{% if show_the_thing %}<div>Please keep inline source inline</div>{% endif %}\n"
        ),
        (
            "{% if show_the_thing %}<div>Please keep inline source inline</div>{% endif %}\n"
        ),
        id="issue_1597_keep_inline_short_if",
    ),
    pytest.param(
        (
            "{{ terms_form.move_in_date }}\n"
            "{% if terms_form.move_in_date.errors %}\n"
            '<span class="form-text text-danger">{{ terms_form.move_in_date.errors.0 }}</span>\n'
            "{% endif %}\n"
        ),
        (
            "{{ terms_form.move_in_date }}\n"
            "{% if terms_form.move_in_date.errors %}\n"
            '    <span class="form-text text-danger">{{ terms_form.move_in_date.errors.0 }}</span>\n'
            "{% endif %}\n"
        ),
        id="issue_1597_preserve_variable_before_if",
    ),
    pytest.param(
        (
            "{% csrf_token %}\n"
            "\n"
            "{% if messages %}\n"
            "  {% for message in messages %}\n"
            '  <div class="row mb-3">\n'
            '    <div class="col">\n'
            '      <div class="alert alert-danger">{{ message }}</div>\n'
            "    </div>\n"
            "  </div>\n"
            "  {% endfor %}\n"
            "{% endif %}\n"
        ),
        (
            "{% csrf_token %}\n"
            "{% if messages %}\n"
            "    {% for message in messages %}\n"
            '        <div class="row mb-3">\n'
            '            <div class="col">\n'
            '                <div class="alert alert-danger">{{ message }}</div>\n'
            "            </div>\n"
            "        </div>\n"
            "    {% endfor %}\n"
            "{% endif %}\n"
        ),
        id="issue_1597_preserve_nested_template_lines",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output


def test_single_line_if_blocks_format_in_one_pass() -> None:
    source = (
        '<form id="contact-form"\n'
        '      class="fade-rise glass rounded-3xl p-8"\n'
        "      hx-post=\"{% url 'contact_submit' %}\"\n"
        '      hx-target="#contact-form"\n'
        '      hx-swap="outerHTML"\n'
        '      hx-disabled-elt="find button[type=submit]">\n'
        "  {% csrf_token %}\n"
        "  {% if form.non_field_errors %}\n"
        '    <div class="mb-4 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-800"\n'
        '         role="alert">{{ form.non_field_errors }}</div>\n'
        "  {% endif %}\n"
        '  <div class="grid gap-4 sm:grid-cols-2">\n'
        "    <div>\n"
        '      <input name="first_name"\n'
        "             value=\"{{ form.first_name.value|default_if_none:'' }}\"\n"
        '             placeholder="First Name"\n'
        '             autocomplete="given-name"\n'
        '             class="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-swift-500 focus:ring-swift-500">\n'
        '      {% if form.first_name.errors %}<p class="mt-1 text-xs text-red-600">{{ form.first_name.errors.0 }}</p>{% endif %}\n'
        "    </div>\n"
        "    <div>\n"
        '      <input name="last_name"\n'
        "             value=\"{{ form.last_name.value|default_if_none:'' }}\"\n"
        '             placeholder="Last Name"\n'
        '             autocomplete="family-name"\n'
        '             class="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-swift-500 focus:ring-swift-500">\n'
        '      {% if form.last_name.errors %}<p class="mt-1 text-xs text-red-600">{{ form.last_name.errors.0 }}</p>{% endif %}\n'
        "    </div>\n"
        '    <div class="sm:col-span-2">\n'
        '      <input name="email"\n'
        '             type="email"\n'
        "             value=\"{{ form.email.value|default_if_none:'' }}\"\n"
        '             placeholder="Business Email"\n'
        '             autocomplete="email"\n'
        '             class="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-swift-500 focus:ring-swift-500">\n'
        '      {% if form.email.errors %}<p class="mt-1 text-xs text-red-600">{{ form.email.errors.0 }}</p>{% endif %}\n'
        "    </div>\n"
        '    <div class="sm:col-span-2">\n'
        '      <input name="job_title"\n'
        "             value=\"{{ form.job_title.value|default_if_none:'' }}\"\n"
        '             placeholder="Job Title"\n'
        '             autocomplete="organization-title"\n'
        '             class="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-gray-900 shado0 focus:border-swift-500 focus:ring-swift-500">\n'
        '      {% if form.job_title.errors %}<p class="mt-1 text-xs text-red-600">{{ form.job_title.errors.0 }}</p>{% endif %}\n'
        "    </div>\n"
        "  </div>\n"
        "</form>\n"
    )
    config = config_builder({
        "profile": "django",
        "indent": 2,
        "max_line_length": 120,
    })
    output = formatter(config, source)
    second_pass = formatter(config, output)

    printer(second_pass, source, output)
    assert output == second_pass
