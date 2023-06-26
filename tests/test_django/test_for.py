"""Test django for tag.

poetry run pytest tests/test_django/test_for.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

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
        ("{% for i in items %}\n" "    <div>{% formfield i %}</div>\n" "{% endfor %}"),
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
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
