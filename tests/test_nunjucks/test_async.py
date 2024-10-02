"""Test nunjucks ascyn tags.

uv run pytest tests/test_nunjucks/test_async.py
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
            "<ul>{% asyncEach athlete in athlete_list %}<li>{{ athlete.name }}</li>{% empty %}<li>Sorry, no athletes in this list.</li>{% endeach %}</ul>"
        ),
        (
            "<ul>\n"
            "    {% asyncEach athlete in athlete_list %}\n"
            "        <li>{{ athlete.name }}</li>\n"
            "    {% empty %}\n"
            "        <li>Sorry, no athletes in this list.</li>\n"
            "    {% endeach %}\n"
            "</ul>\n"
        ),
        id="eachAsync",
    ),
    pytest.param(
        (
            "<ul>{% asyncAll athlete in athlete_list %}<li>{{ athlete.name }}</li>{% empty %}<li>Sorry, no athletes in this list.</li>{% endall %}</ul>"
        ),
        (
            "<ul>\n"
            "    {% asyncAll athlete in athlete_list %}\n"
            "        <li>{{ athlete.name }}</li>\n"
            "    {% empty %}\n"
            "        <li>Sorry, no athletes in this list.</li>\n"
            "    {% endall %}\n"
            "</ul>\n"
        ),
        id="eachAll",
    ),
    pytest.param(
        (
            "{% asyncEach i in items %}\n"
            "    <div>{% formfield i %}</div>\n"
            "{% endeach %}"
        ),
        (
            "{% asyncEach i in items %}\n"
            "    <div>{% formfield i %}</div>\n"
            "{% endeach %}\n"
        ),
        id="each test nested formfield",
    ),
    pytest.param(
        (
            "{% asyncAll i in items %}\n"
            "    <div>{% formfield i %}</div>\n"
            "{% endall %}"
        ),
        (
            "{% asyncAll i in items %}\n"
            "    <div>{% formfield i %}</div>\n"
            "{% endall %}\n"
        ),
        id="all test nested formfield",
    ),
    pytest.param(
        (
            '<div class="form-inputs plans-form">\n'
            '    <div class="trans-wrapper pos-comparator-flex">\n'
            "        {% asyncEach field in POSOptimizer %}\n"
            "            <div>\n"
            "                <label>{{ field.label }}</label>\n"
            "                {% formfield field show_label=False %}\n"
            "            </div>\n"
            "        {% endeach %}\n"
            "        {% asyncAll field in POSOptimizer %}\n"
            "            <div>\n"
            "                <label>{{ field.label }}</label>\n"
            "                {% formfield field show_label=False %}\n"
            "            </div>\n"
            "        {% endall %}\n"
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
            "        {% asyncEach field in POSOptimizer %}\n"
            "            <div>\n"
            "                <label>{{ field.label }}</label>\n"
            "                {% formfield field show_label=False %}\n"
            "            </div>\n"
            "        {% endeach %}\n"
            "        {% asyncAll field in POSOptimizer %}\n"
            "            <div>\n"
            "                <label>{{ field.label }}</label>\n"
            "                {% formfield field show_label=False %}\n"
            "            </div>\n"
            "        {% endall %}\n"
            "        <div>\n"
            "            <label>&nbsp</label>\n"
            '            <button type="submit">{% trans "Calcola" %}</button>\n'
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="each test nested formfield inside for",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
