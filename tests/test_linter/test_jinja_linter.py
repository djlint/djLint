"""Djlint linter tests for jinja.

poetry run pytest tests/test_linter/test_jinja_linter.py

"""

import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<button onclick="util.request(`set`, {to_set : {tags: ' '}});">'),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": '<button onclick="uti',
                    "message": "Tag seems to be an orphan.",
                }
            ]
        ),
        id="T001 fix for #606",
    ),
    pytest.param(
        ("{#-test -#}"),
        ([]),
        id="T001",
    ),
    pytest.param(
        ("{#- test -#}"),
        ([]),
        id="T001_2",
    ),
    pytest.param(
        ("<div>\n" "     {%\n" '         ("something", "1"),\n' "     %}\n" " </div>"),
        ([]),
        id="T001_3",
    ),
    pytest.param(
        ("{{- foo }}{{+ bar }}{{ biz -}}{{ baz +}}"),
        ([]),
        id="T001_4",
    ),
    pytest.param(
        ('<link src="/static/there">'),
        (
            [
                {
                    "code": "J004",
                    "line": "1:0",
                    "match": '<link src="/static/',
                    "message": "(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.",
                }
            ]
        ),
        id="J004",
    ),
    pytest.param(
        (
            '<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n<form action="/Collections"></form></a>'
        ),
        (
            [
                {
                    "code": "J018",
                    "line": "1:0",
                    "match": '<a href="/Collection',
                    "message": "(Jinja) Internal links should use the {{ url_for() ... }} pattern.",
                },
                {
                    "code": "J018",
                    "line": "2:0",
                    "match": '<form action="/Colle',
                    "message": "(Jinja) Internal links should use the {{ url_for() ... }} pattern.",
                },
            ]
        ),
        id="J018",
    ),
    pytest.param(
        ('<a href="javascript:abc()">\n<form action="javascript:abc()"></form></a>'),
        (
            [
                {
                    "code": "H019",
                    "line": "1:0",
                    "match": '<a href="javascript:',
                    "message": "Replace 'javascript:abc()' with on_ event and real url.",
                },
                {
                    "code": "H019",
                    "line": "2:0",
                    "match": '<form action="javasc',
                    "message": "Replace 'javascript:abc()' with on_ event and real url.",
                },
            ]
        ),
        id="J018_no",
    ),
    pytest.param(
        ('<a href="onclick:abc()">\n<form action="onclick:abc()"></form></a>'),
        ([]),
        id="J018_on_events",
    ),
    pytest.param(
        ('<div class="em-ajaxLogs" data-src="/table/task/{{ t.id }}/log"></div>'),
        (
            [
                {
                    "code": "J018",
                    "line": "1:0",
                    "match": '<div class="em-ajaxL',
                    "message": "(Jinja) Internal links should use the {{ url_for() ... }} pattern.",
                }
            ]
        ),
        id="J018_data_src",
    ),
    pytest.param(
        ('<a href="mailto:joe"></a><a href="tel:joe"></a>'),
        ([]),
        id="J018_mailto",
    ),
    pytest.param(
        ('<a href="data:,Hello%2C%20World%21"></a>'),
        ([]),
        id="J018_data",
    ),
    pytest.param(
        ('<div data-row-selection-action="highlight"></div>'),
        ([]),
        id="J018_attributes",
    ),
    pytest.param(
        ('<form action="{{ url_for(\'something\', action="xxx") }}"></form>'),
        ([]),
        id="J018_action_attr_url",
    ),
    pytest.param(
        (
            "{% macro rendersubmit(buttons=[], class=\"\", index='', url='', that=\"\" , test='') -%}"
        ),
        ([]),
        id="T027",
    ),
    pytest.param(
        ("<a href=\"{% blah 'asdf' -%}\"></a>"),
        ([]),
        id="T028",
    ),
    pytest.param(
        ("<a href=\"{%- if 'asdf' %}\"></a>"),
        (
            [
                {
                    "code": "T028",
                    "line": "1:0",
                    "match": "<a href=\"{%- if 'asd",
                    "message": "Consider using spaceless tags inside attribute values. {%- if/for -%}",
                }
            ]
        ),
        id="T028_2",
    ),
    pytest.param(
        ("<a href=\"{%- if 'asdf' %}\"></a>"),
        (
            [
                {
                    "code": "T028",
                    "line": "1:0",
                    "match": "<a href=\"{%- if 'asd",
                    "message": "Consider using spaceless tags inside attribute values. {%- if/for -%}",
                }
            ]
        ),
        id="T028_3",
    ),
    pytest.param(
        ("<a href=\"{{- blah 'asdf' }}\"></a>"),
        ([]),
        id="T028_4",
    ),
    pytest.param(
        (
            "{# [INFO] Simple example #}\n"
            "  {% set stuff = [\n"
            "      'value', 'value'\n"
            "  ] %}\n"
            "n"
            "  {# [INFO] Real example #}\n"
            "  {% set online_scaners = [\n"
            "      ('https://example.com', 'blue', 'One'),\n"
            "      ('https://example.com', 'green', 'Two'),\n"
            "      ('https://example.com', 'plum', 'Three'),\n"
            "  ] %}"
        ),
        ([]),
        id="T032",
    ),
    pytest.param(
        ("{% not ok }%"),
        (
            [
                {
                    "code": "T034",
                    "line": "1:0",
                    "match": "{% not ok }%",
                    "message": "Did you intend to use {% ... %} instead of {% ... }%?",
                }
            ]
        ),
        id="T034",
    ),
    pytest.param(
        ("{% not ok \n%}"),
        ([]),
        id="T034",
    ),
    pytest.param(
        (
            "{% raw %}\n"
            ";      e.g. for a ISO8601 formatted timestring, use: %{%Y-%m-%dT%H:%M:%S%z}t\n"
            "{% endraw %}"
        ),
        ([]),
        id="raw",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, jinja_config):
    filename = "test.html"
    output = linter(jinja_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = list(filter(lambda x: x not in expected, output[filename])) + list(
        filter(lambda x: x not in output[filename], expected)
    )

    assert len(mismatch) == 0
