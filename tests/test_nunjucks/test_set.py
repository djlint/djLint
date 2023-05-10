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
            '        name: "id",\n'
            '        type: "integer",\n'
            "        primary: true,\n"
            "        id: 1\n"
            "    },\n"
            "    {\n"
            '        name: "name",\n'
            '        type: "string"\n'
            "    }\n"
            "] %}\n"
        ),
        ({"max_line_length": 10}),
        id="indent multiilne",
    ),
    pytest.param(
        (
            '{% set schema=[{"name": "id",\n'
            '"type": "integer",\n'
            '"primary": true\n'
            "},] %}"
        ),
        ('{% set schema = [{name: "id", type: "integer", primary: true}] %}\n'),
        ({}),
        id="indent invalid json",
    ),
    pytest.param(
        (
            '{% set schema=[{name: "id",\n'
            "'type': \"1\",\n"
            '"primary+1": true\n'
            "}] %}"
        ),
        ('{% set schema = [{name: "id", type: "1", "primary+1": true}] %}\n'),
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
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args, nunjucks_config):
    args["profile"] = "nunjucks"
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
