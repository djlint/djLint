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
        ("{{test }}\n{% test%}<a>"),
        ([("T001", 1), ("T001", 2)]),
        (),
        id="T001",
    ),
    pytest.param(
        ("{% extends 'this' %}"),
        (
            [
                ("T002", 1),
            ]
        ),
        (),
        id="T002",
    ),
    pytest.param(
        ("{% extends this %}"),
        (),
        (["T002"]),
        id="T002_unquoted_var_names",
    ),
    pytest.param(
        ("{% with a='this' %}"),
        (["T002"]),
        (),
        id="T002_with",
    ),
    pytest.param(
        ("{% trans 'this' %}"),
        (["T002"]),
        (),
        id="T002_trans",
    ),
    pytest.param(
        ("{% translate 'this' %}"),
        (["T002"]),
        (),
        id="T002_translate",
    ),
    pytest.param(
        ("{% include 'this' %}"),
        (["T002"]),
        (),
        id="T002_include",
    ),
    pytest.param(
        ("{% now 'Y-m-d G:i:s' %}"),
        (["T002"]),
        (),
        id="T002_now",
    ),
    pytest.param(
        (
            '{% extends "layout.h" %}\n'
            '<div class="card" data-list=\'{"name": "blah"}\'>\n'
            '{% include "template.html" %}\n'
            "<div {% fpr %} data-{{ name }}='{{ value }}'{% endfor %}/>"
        ),
        (),
        (["T002"]),
        id="T002_test_greedy_regex",
    ),
    pytest.param(
        ("{% if form.action_url %}\n" "   ='stuff'\n" " {% endif %}"),
        (),
        (["T002"]),
        id="T002_test_greedy_regex_2",
    ),
    pytest.param(
        (
            '{% include "template.html" %}\n'
            " {% include \"template.html\" with type='mono' %}"
        ),
        ([("T002", 2)]),
        (),
        id="T002_test_line_num",
    ),
    pytest.param(
        ("{% endblock %}"),
        ([("T003", 1)]),
        (),
        id="T003",
    ),
    pytest.param(
        ('<link src="/static/there">'),
        ([("D004", 1)]),
        (),
        id="DJ004",
    ),
    pytest.param(
        (
            '<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n'
            '<form action="/Collections"></form></a>'
        ),
        ([("D018", 1), ("D018", 2)]),
        (),
        id="DJ018",
    ),
    pytest.param(
        ('<a href="javascript:abc()">\n' '<form action="javascript:abc()"></form></a>'),
        (),
        ([("D018", 1), ("D018", 2)]),
        id="DJ018_no_match",
    ),
    pytest.param(
        (
            '<a href="#">\n<form action="#"><a href="#tab">\n'
            '<form action="#go"></form></a></form></a>'
        ),
        (),
        ([("D018", 1), ("D018", 2)]),
        id="DJ018_has_urls",
    ),
    pytest.param(
        ('<div class="em-ajaxLogs" data-src="/table/task/{{ t.id }}/log"></div>'),
        ([("D018", 1)]),
        (),
        id="DJ018_data_src",
    ),
    pytest.param(
        ('<a href="mailto:joe"></a><a href="tel:joe"></a>'),
        (),
        (["D018"]),
        id="DJ018_mailto",
    ),
    pytest.param(
        ('<a href="data:,Hello%2C%20World%21"></a>'),
        (),
        (["D018"]),
        id="DJ018_data",
    ),
    pytest.param(
        ('<div data-row-selection-action="highlight"></div>'),
        (),
        (["D018"]),
        id="DJ018_attribute_names",
    ),
    pytest.param(
        ('<form action="{% url \'something\' %}" data-action="xxx"></form>'),
        (),
        (["D018"]),
        id="DJ018_data_action",
    ),
    pytest.param(
        ("{% blah 'asdf %}"),
        (["T027"]),
        (),
        id="T027",
    ),
    pytest.param(
        ("{% blah 'asdf' %}{{ blah \"asdf\" }}"),
        (),
        (["T027"]),
        id="T027_no",
    ),
    pytest.param(
        ("{% blah 'asdf' 'blah %}"),
        (["T027"]),
        (),
        id="T027_long_name",
    ),
    pytest.param(
        ('{% trans "Check box if you\'re interested in this location." %}'),
        (),
        (["T027"]),
        id="T027_trans",
    ),
    pytest.param(
        (
            "{% macro rendersubmit(buttons=[], class=\"\", index='', url='', that=\"\" , test='') -%}"
        ),
        (),
        (["T027"]),
        id="T027_mixed_quotes",
    ),
    pytest.param(
        ("<a href=\"{{ blah 'asdf' -}}\">"),
        (),
        (["T028"]),
        id="T028_no",
    ),
    pytest.param(
        ("<a {{ blah 'asdf' }}>"),
        (),
        (["T028"]),
        id="T028_no_2",
    ),
    pytest.param(
        ("<a {% blah 'asdf' %}>"),
        (),
        (["T028"]),
        id="T028_no_3",
    ),
    pytest.param(
        ("{% blah 'asdf' %}"),
        (),
        (["T028"]),
        id="T028_no_5",
    ),
    pytest.param(
        ("{% for 'asdf' %}"),
        (),
        (["T028"]),
        id="T028_no_6",
    ),
    pytest.param(
        ('<input class="{% if %}{% endif %}" />'),
        (),
        (["T028"]),
        id="T028_no_7",
    ),
    pytest.param(
        ("{% static ''  \"  \"  'foo/bar.min.css' %}"),
        (["T032"]),
        (),
        id="T032",
    ),
    pytest.param(
        ("{% static  ''  %}"),
        (["T032"]),
        (),
        id="T032_2",
    ),
    pytest.param(
        ("{% static '' \"     \" 'foo/bar.min.css' %}"),
        (),
        (["T032"]),
        id="T032_no",
    ),
    pytest.param(
        ("{{ static ''  \"  \"  'foo/bar.min.css' }}"),
        (["T032"]),
        (),
        id="T032_3",
    ),
    pytest.param(
        ("{{ static  ''  }}"),
        (["T032"]),
        (),
        id="T032_4",
    ),
    pytest.param(
        ("{{ static '' \"     \" 'foo/bar.min.css' }}"),
        (),
        (["T032"]),
        id="T032_no_2",
    ),
]


@pytest.mark.parametrize(("source", "expected", "excluded"), test_data)
def test_django_linter(source, expected, excluded, django_config) -> None:
    filename = "file"
    filepath = filename
    lint = linter(django_config, source, filename, filepath)[filename]

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
