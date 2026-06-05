"""Test django if tag.

uv run pytest tests/test_django/test_if.py
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
            "{% if athlete_list %}Number of athletes: {{ athlete_list|length }}{% elif athlete_in_locker_room_list %}Athletes should be out of the locker room soon!{% else %}No athletes.{% endif %}"
        ),
        (
            "{% if athlete_list %}\n"
            "    Number of athletes: {{ athlete_list|length }}\n"
            "{% elif athlete_in_locker_room_list %}\n"
            "    Athletes should be out of the locker room soon!\n"
            "{% else %}\n"
            "    No athletes.\n"
            "{% endif %}\n"
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
