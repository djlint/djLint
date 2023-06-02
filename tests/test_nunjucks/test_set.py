"""Test nunjucks set tags.

poetry run pytest tests/test_nunjucks/test_set.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("{%- set posts = collections.docs -%}"),
        ("{%- set posts = collections.docs -%}\n"),
        ({}),
        id="set",
    ),
    pytest.param(
        ("{%-set posts = collections.docs-%}\n{%asdf%}"),
        ("{%- set posts = collections.docs -%}\n" "{% asdf %}\n"),
        ({}),
        id="set_with_sibling",
    ),
    pytest.param(
        ('<title>{% set_title "My Title" %}</title>'),
        ('<title>{% set_title "My Title" %}</title>\n'),
        ({}),
        id="don't break underscore stuff",
    ),
    pytest.param(
        (
            "{% set classes =  {\n"
            "'sPaging': 'd-flex justify-content-center ',\n"
            "'sPageButton': 'btn btn-outline-primary ms-1 me-1',\n"
            "'sPageButtonActive': 'active',\n"
            "}%}\n"
        ),
        (
            "{% set classes = {\n"
            '    "sPaging": "d-flex justify-content-center ",\n'
            '    "sPageButton": "btn btn-outline-primary ms-1 me-1",\n'
            '    "sPageButtonActive": "active"\n'
            "} %}\n"
        ),
        ({}),
        id="quote json keys",
    ),
    pytest.param(
        (
            "{% set schema=[\n"
            "{\n"
            '"name":"id",\n'
            '"type":      "integer",\n'
            '"primary": true,\n'
            "id:1\n"
            "},\n"
            "{\n"
            '"name": "name",\n'
            '"type": "string"\n'
            "}\n"
            "] %}"
        ),
        (
            "{% set schema = [\n"
            "    {\n"
            '        "name": "id",\n'
            '        "type": "integer",\n'
            '        "primary": true,\n'
            '        "id": 1\n'
            "    },\n"
            "    {\n"
            '        "name": "name",\n'
            '        "type": "string"\n'
            "    }\n"
            "] %}\n"
        ),
        ({"max_line_length": 10}),
        id="indent multiilne",
    ),
    pytest.param(
        (
            "<div>{% set schema=[\n"
            "{\n"
            '"name":"id",\n'
            '"type":      "integer",\n'
            '"primary": true,\n'
            "id:1\n"
            "},\n"
            "{\n"
            '"name": "name",\n'
            '"type": "string"\n'
            "}\n"
            "] %}</div>"
        ),
        (
            "<div>\n"
            "    {% set schema = [\n"
            "        {\n"
            '            "name": "id",\n'
            '            "type": "integer",\n'
            '            "primary": true,\n'
            '            "id": 1\n'
            "        },\n"
            "        {\n"
            '            "name": "name",\n'
            '            "type": "string"\n'
            "        }\n"
            "    ] %}\n"
            "</div>\n"
        ),
        ({"max_line_length": 10}),
        id="nestedindent multiilne",
    ),
    pytest.param(
        (
            '{% set schema=[{"name": "id",\n'
            '"type": "integer",\n'
            '"primary": true\n'
            "},] %}"
        ),
        ('{% set schema = [{"name": "id", "type": "integer", "primary": true}] %}\n'),
        ({}),
        id="indent invalid json",
    ),
    pytest.param(
        (
            '{% set schema=[{"name": "id",\n'
            '"type": "integer",\n'
            '"primary": true\n'
            "},] %}"
        ),
        (
            '{% set schema=[{"name": "id",\n'
            '"type": "integer",\n'
            '"primary": true\n'
            "},] %}\n"
        ),
        ({"no_set_formatting": True}),
        id="disabled",
    ),
    pytest.param(
        (
            '{% set schema=[{name: "id",\n'
            "'type': \"1\",\n"
            '"primary+1": true\n'
            "}] %}"
        ),
        ('{% set schema = [{"name": "id", "type": "1", "primary+1": true}] %}\n'),
        ({}),
        id="indent valid json",
    ),
    pytest.param(
        (
            '{% set table_keys = [ ( "date_started", "Start date"), ( "name", "Name" )] %}'
        ),
        ("{% set table_keys = [('date_started', 'Start date'), ('name', 'Name')] %}\n"),
        ({}),
        id="indent py style list",
    ),
    pytest.param(
        (
            '{% set cta %}{% include "partials/cta.njk" %}<div></div>{% endset %}\n'
            "{%-set posts = collections.docs-%}\n"
            "{%asdf%}"
        ),
        (
            "{% set cta %}\n"
            '    {% include "partials/cta.njk" %}\n'
            "    <div></div>\n"
            "{% endset %}\n"
            "{%- set posts = collections.docs -%}\n"
            "{% asdf %}\n"
        ),
        ({}),
        id="set block",
    ),
    pytest.param(
        (
            "<ul>\n"
            "  {# djlint:off #}\n"
            "  <li>{%set a=[{'x':1}]%}</li>\n"
            "  {# djlint:on #}\n"
            "</ul>"
        ),
        (
            "<ul>\n"
            "    {# djlint:off #}\n"
            "  <li>{%set a=[{'x':1}]%}</li>\n"
            "    {# djlint:on #}\n"
            "</ul>\n"
        ),
        ({"max_line_length": 1}),
        id="ignored code should not be touched",
    ),
    pytest.param(
        ('{%- set posts = "¿Spécial çhärs 👻?" -%}'),
        ('{%- set posts = "¿Spécial çhärs 👻?" -%}\n'),
        ({}),
        id="set",
    ),
    pytest.param(
        ("<li>{{ foo(1,2) }}</li>"),
        ("<li>{{ foo(1, 2) }}</li>\n"),
        ({}),
        id="don't add parenth to lists",
    ),
    pytest.param(
        ('{{- foo("bar") -}}'),
        ('{{- foo("bar") -}}\n'),
        ({}),
        id="don't break spaceless tags #667",
    ),
    pytest.param(
        (
            "{% for tag in collections.all | getAllTags | filterTagList | sort %}\n"
            "    {% set tagUrl %}\n"
            "        /tags/{{ tag | slugify }}/{% endset %}\n"
            '        <a href="{{ tagUrl }}" class="post-tag">{{ tag }} ({{ collections[tag].length }})</a>\n'
            "    {% endfor %}\n"
        ),
        (
            "{% for tag in collections.all | getAllTags | filterTagList | sort %}\n"
            "    {% set tagUrl %}\n"
            "        /tags/{{ tag | slugify }}/\n"
            "    {% endset %}\n"
            '    <a href="{{ tagUrl }}" class="post-tag">{{ tag }} ({{ collections[tag].length }})</a>\n'
            "{% endfor %}\n"
        ),
        ({}),
        id="check dedent on nested block",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args, nunjucks_config):
    args["profile"] = "nunjucks"
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
