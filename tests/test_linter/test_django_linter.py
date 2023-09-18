"""Djlint linter rule tests for django.

poetry run pytest tests/test_linter/test_django_linter.py

"""

import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("{{test }}\n{% test%}<a>"),
        (
            [
                {
                    "code": "T001",
                    "line": "1:0",
                    "match": "{{test }}",
                    "message": "Variables should be wrapped in a whitespace.",
                },
                {
                    "code": "T001",
                    "line": "2:0",
                    "match": "{% test%}",
                    "message": "Variables should be wrapped in a whitespace.",
                },
                {
                    "code": "H025",
                    "line": "2:9",
                    "match": "<a>",
                    "message": "Tag seems to be an orphan.",
                },
            ]
        ),
        id="T001",
    ),
    pytest.param(
        ("{% extends 'this' %}"),
        (
            [
                {
                    "code": "T002",
                    "line": "1:0",
                    "match": "{% extends 'this' %}",
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002",
    ),
    pytest.param(
        ("{% extends this %}"),
        ([]),
        id="T002_unquoted_var_names",
    ),
    pytest.param(
        ("{% with a='this' %}"),
        (
            [
                {
                    "code": "T002",
                    "line": "1:0",
                    "match": "{% with a='this' %}",
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002_with",
    ),
    pytest.param(
        ("{% trans 'this' %}"),
        (
            [
                {
                    "code": "T002",
                    "line": "1:0",
                    "match": "{% trans 'this' %}",
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002_trans",
    ),
    pytest.param(
        ("{% translate 'this' %}"),
        (
            [
                {
                    "code": "T002",
                    "line": "1:0",
                    "match": "{% translate 'this' ",
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002_translate",
    ),
    pytest.param(
        ("{% include 'this' %}"),
        (
            [
                {
                    "code": "T002",
                    "line": "1:0",
                    "match": "{% include 'this' %}",
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002_include",
    ),
    pytest.param(
        ("{% now 'Y-m-d G:i:s' %}"),
        (
            [
                {
                    "code": "T002",
                    "line": "1:0",
                    "match": "{% now 'Y-m-d G:i:s'",
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002_now",
    ),
    pytest.param(
        (
            '{% extends "layout.h" %}\n'
            '<div class="card" data-list=\'{"name": "blah"}\'>\n'
            '{% include "template.html" %}\n'
            "<div {% fpr %} data-{{ name }}='{{ value }}'{% endfor %}/>"
        ),
        (
            [
                {
                    "code": "H025",
                    "line": "2:0",
                    "match": '<div class="card" da',
                    "message": "Tag seems to be an orphan.",
                }
            ]
        ),
        id="T002_test_greedy_regex",
    ),
    pytest.param(
        ("{% if form.action_url %}\n" "   ='stuff'\n" " {% endif %}"),
        ([]),
        id="T002_test_greedy_regex_2",
    ),
    pytest.param(
        (
            '{% include "template.html" %}\n'
            " {% include \"template.html\" with type='mono' %}"
        ),
        (
            [
                {
                    "code": "T002",
                    "line": "2:1",
                    "match": '{% include "template',
                    "message": "Double quotes should be used in tags.",
                }
            ]
        ),
        id="T002_test_line_num",
    ),
    pytest.param(
        ("{% endblock %}"),
        (
            [
                {
                    "code": "T003",
                    "line": "1:0",
                    "match": "{% endblock %}",
                    "message": "Endblock should have name. Ex: {% endblock body %}.",
                }
            ]
        ),
        id="T003",
    ),
    pytest.param(
        ('<link src="/static/there">'),
        (
            [
                {
                    "code": "D004",
                    "line": "1:0",
                    "match": '<link src="/static/',
                    "message": "(Django) Static urls should follow {% static path/to/file %} pattern.",
                }
            ]
        ),
        id="DJ004",
    ),
    pytest.param(
        (
            '<a href="/Collections?handler=RemoveAgreement&id=@a.Id">\n'
            '<form action="/Collections"></form></a>'
        ),
        (
            [
                {
                    "code": "D018",
                    "line": "1:0",
                    "match": '<a href="/Collection',
                    "message": "(Django) Internal links should use the {% url ... %} pattern.",
                },
                {
                    "code": "D018",
                    "line": "2:0",
                    "match": '<form action="/Colle',
                    "message": "(Django) Internal links should use the {% url ... %} pattern.",
                },
            ]
        ),
        id="DJ018",
    ),
    pytest.param(
        ('<a href="javascript:abc()">\n' '<form action="javascript:abc()"></form></a>'),
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
        id="DJ018_no_match",
    ),
    pytest.param(
        (
            '<a href="#">\n<form action="#"><a href="#tab">\n'
            '<form action="#go"></form></a></form></a>'
        ),
        ([]),
        id="DJ018_has_urls",
    ),
    pytest.param(
        ('<div class="em-ajaxLogs" data-src="/table/task/{{ t.id }}/log"></div>'),
        (
            [
                {
                    "code": "D018",
                    "line": "1:0",
                    "match": '<div class="em-ajaxL',
                    "message": "(Django) Internal links should use the {% url ... %} pattern.",
                }
            ]
        ),
        id="DJ018_data_src",
    ),
    pytest.param(
        ('<a href="mailto:joe"></a><a href="tel:joe"></a>'),
        ([]),
        id="DJ018_mailto",
    ),
    pytest.param(
        ('<a href="data:,Hello%2C%20World%21"></a>'),
        ([]),
        id="DJ018_data",
    ),
    pytest.param(
        ('<div data-row-selection-action="highlight"></div>'),
        ([]),
        id="DJ018_attribute_names",
    ),
    pytest.param(
        ('<form action="{% url \'something\' %}" data-action="xxx"></form>'),
        ([]),
        id="DJ018_data_action",
    ),
    pytest.param(
        ('<form action="{% url \'something\' action="xxx" %}"></form>'),
        ([]),
        id="DJ018_action_attr_url",
    ),
    pytest.param(
        ("{% blah 'asdf %}"),
        (
            [
                {
                    "code": "T027",
                    "line": "1:0",
                    "match": "{% blah 'asdf %}",
                    "message": "Unclosed string found in template syntax.",
                }
            ]
        ),
        id="T027",
    ),
    pytest.param(
        ("{% blah 'asdf' %}{{ blah \"asdf\" }}"),
        ([]),
        id="T027_no",
    ),
    pytest.param(
        ("{% blah 'asdf' 'blah %}"),
        (
            [
                {
                    "code": "T027",
                    "line": "1:0",
                    "match": "{% blah 'asdf' 'blah",
                    "message": "Unclosed string found in template syntax.",
                }
            ]
        ),
        id="T027_long_name",
    ),
    pytest.param(
        ('{% trans "Check box if you\'re interested in this location." %}'),
        ([]),
        id="T027_trans",
    ),
    pytest.param(
        ('{% trans "Check box if you\'re interested in this location." %}'),
        ([]),
        id="T027_golang comment",
    ),
    pytest.param(
        ("{{/* can't */}}"),
        ([]),
        id="T027_mixed_quotes",
    ),
    pytest.param(
        ("<a href=\"{{ blah 'asdf' -}}\">"),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<a href=\"{{ blah 'as",
                    "message": "Tag seems to be an orphan.",
                }
            ]
        ),
        id="T028_no",
    ),
    pytest.param(
        ("<a {{ blah 'asdf' }}>"),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<a {{ blah 'asdf' }}",
                    "message": "Tag seems to be an orphan.",
                }
            ]
        ),
        id="T028_no_2",
    ),
    pytest.param(
        ("<a {% blah 'asdf' %}>"),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<a {% blah 'asdf' %}",
                    "message": "Tag seems to be an orphan.",
                }
            ]
        ),
        id="T028_no_3",
    ),
    pytest.param(
        ("{% blah 'asdf' %}"),
        ([]),
        id="T028_no_5",
    ),
    pytest.param(
        ("{% for 'asdf' %}"),
        ([]),
        id="T028_no_6",
    ),
    pytest.param(
        ('<input class="{% if %}{% endif %}" />'),
        ([]),
        id="T028_no_7",
    ),
    pytest.param(
        ("{% static ''  \"  \"  'foo/bar.min.css' %}"),
        (
            [
                {
                    "code": "T032",
                    "line": "1:0",
                    "match": "{% static ''",
                    "message": "Extra whitespace found in template tags.",
                }
            ]
        ),
        id="T032",
    ),
    pytest.param(
        ("{% static  ''  %}"),
        (
            [
                {
                    "code": "T032",
                    "line": "1:0",
                    "match": "{% static",
                    "message": "Extra whitespace found in template tags.",
                }
            ]
        ),
        id="T032_2",
    ),
    pytest.param(
        ("{% static '' \"     \" 'foo/bar.min.css' %}"),
        ([]),
        id="T032_no",
    ),
    pytest.param(
        ("{{ static ''  \"  \"  'foo/bar.min.css' }}"),
        (
            [
                {
                    "code": "T032",
                    "line": "1:0",
                    "match": "{{ static ''",
                    "message": "Extra whitespace found in template tags.",
                }
            ]
        ),
        id="T032_3",
    ),
    pytest.param(
        ("{{ static  ''  }}"),
        (
            [
                {
                    "code": "T032",
                    "line": "1:0",
                    "match": "{{ static",
                    "message": "Extra whitespace found in template tags.",
                }
            ]
        ),
        id="T032_4",
    ),
    pytest.param(
        ("{{ static '' \"     \" 'foo/bar.min.css' }}"),
        ([]),
        id="T032_no_2",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    filename = "test.html"
    output = linter(django_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = list(filter(lambda x: x not in expected, output[filename])) + list(
        filter(lambda x: x not in output[filename], expected)
    )

    assert len(mismatch) == 0
