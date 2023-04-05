"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_linter/test_linter.py::test_random

Test setup

(html, (list of codes that should file, plus optional line number))


"""
# pylint: disable=C0116,C0103,C0302


import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("{#-test -#}"),
        (),
        (["T001"]),
        id="T001",
    ),
    pytest.param(
        ("{#- test -#}"),
        (),
        (["T001"]),
        id="T001_2",
    ),
    pytest.param(
        ("<div>\n" "     {%\n" '         ("something", "1"),\n' "     %}\n" " </div>"),
        (),
        (["T001"]),
        id="T001_3",
    ),
    pytest.param(
        ("{{- foo }}{{+ bar }}{{ biz -}}{{ baz +}}"),
        (),
        (["T001"]),
        id="T001_4",
    ),
    pytest.param(
        ('<link src="/static/there">'),
        ([("J004", 1)]),
        (),
        id="J004",
    ),
    pytest.param(
        (
            '<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n<form action="/Collections"></form></a>'
        ),
        ([("J018", 1), ("J018", 2)]),
        (),
        id="J018",
    ),
    pytest.param(
        ('<a href="javascript:abc()">\n<form action="javascript:abc()"></form></a>'),
        (),
        ([("J018", 1), ("J018", 2)]),
        id="J018_no",
    ),
    pytest.param(
        ('<a href="onclick:abc()">\n<form action="onclick:abc()"></form></a>'),
        (),
        ([("J018", 1), ("J018", 2)]),
        id="J018_on_events",
    ),
    pytest.param(
        ('<div class="em-ajaxLogs" data-src="/table/task/{{ t.id }}/log"></div>'),
        ([("J018", 1)]),
        (),
        id="J018_data_src",
    ),
    pytest.param(
        ('<a href="mailto:joe"></a><a href="tel:joe"></a>'),
        (),
        (["J018"]),
        id="J018_mailto",
    ),
    pytest.param(
        ('<a href="data:,Hello%2C%20World%21"></a>'),
        (),
        (["J018"]),
        id="J018_data",
    ),
    pytest.param(
        ('<div data-row-selection-action="highlight"></div>'),
        (),
        (["J018"]),
        id="J018_attributes",
    ),
    pytest.param(
        (
            "{% macro rendersubmit(buttons=[], class=\"\", index='', url='', that=\"\" , test='') -%}"
        ),
        (),
        (["T027"]),
        id="T027",
    ),
    pytest.param(
        ("<a href=\"{% blah 'asdf' -%}\">"),
        (),
        (["T028"]),
        id="T028",
    ),
    pytest.param(
        ("<a href=\"{%- if 'asdf' %}\">"),
        (["T028"]),
        (),
        id="T028_2",
    ),
    pytest.param(
        ("<a href=\"{%- if 'asdf' %}\">"),
        (["T028"]),
        (),
        id="T028_3",
    ),
    pytest.param(
        ("<a href=\"{{- blah 'asdf' }}\">"),
        (),
        (["T028"]),
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
        (),
        (["T032"]),
        id="T032",
    ),
    pytest.param(
        ("{% not ok }%"),
        (["T034"]),
        (),
        id="T034",
    ),
    pytest.param(
        ("{% not ok \n%}"),
        (),
        (["T034"]),
        id="T034",
    ),
    pytest.param(
        (
            "{% raw %}\n"
            ";      e.g. for a ISO8601 formatted timestring, use: %{%Y-%m-%dT%H:%M:%S%z}t\n"
            "{% endraw %}"
        ),
        (),
        (["T034"]),
        id="raw",
    ),
]


@pytest.mark.parametrize(("source", "expected", "excluded"), test_data)
def test_jinja_linter(source, expected, excluded, jinja_config) -> None:
    filename = "file"
    filepath = filename
    lint = linter(jinja_config, source, filename, filepath)[filename]

    lint_printer(source, expected, excluded, lint)

    def check_rule(rule, lint):
        if isinstance(rule, tuple):
            return (
                any(
                    x["code"] == rule[0] and int(x["line"].split(":")[0]) == rule[1]
                    for x in lint
                )
                is True
            )
        else:
            return any(x["code"] == rule for x in lint) is True

    for rule in expected:
        assert check_rule(rule, lint) is True

    for rule in excluded:
        assert check_rule(rule, lint) is False
