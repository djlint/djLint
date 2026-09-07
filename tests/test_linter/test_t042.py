"""Test linter code T042.

uv run pytest tests/test_linter/test_t042.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

MESSAGE = "Content outside a block is not rendered in a template that extends another."

test_data = [
    pytest.param(
        ('{% extends "b.html" %}<div>lost</div>{% block a %}x{% endblock %}'),
        (True),
        id="html before the first block",
    ),
    pytest.param(
        ('{% extends "b.html" %}{% block a %}x{% endblock %}<p>lost</p>'),
        (True),
        id="html after the last block",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% if y %}<p>lost</p>{% endif %}'
            "{% block a %}x{% endblock %}"
        ),
        (True),
        id="html inside an if that is outside every block",
    ),
    pytest.param(
        ('{% extends "b.html" %}lost text{% block a %}x{% endblock %}'),
        (True),
        id="bare text",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% blocktrans %}not a block{% endblocktrans %}'
            "{% block a %}x{% endblock %}"
        ),
        (True),
        id="a blocktrans is not a block",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% comment %}{% block a %}{% endcomment %}'
            "<p>lost</p>{% block b %}x{% endblock %}"
        ),
        (True),
        id="a block tag inside a comment opens nothing",
    ),
    pytest.param(
        ('<pre>{% extends "base.html" %}</pre>\n<p>lost</p>\n'),
        (True),
        id="an extends tag inside a pre still runs",
    ),
    pytest.param(
        (
            "<script>\nvar t = \"{% extends 'base.html' %}\";\n</script>\n"
            "<p>lost</p>\n"
        ),
        (True),
        id="an extends tag inside a script still runs",
    ),
    pytest.param(
        ('<!-- {% extends "b.html" %} -->\n<div>free</div>'),
        (True),
        id="an extends tag inside an html comment still runs",
    ),
    pytest.param(
        ('{% extends "b.html" %}<!-- note -->{% block a %}x{% endblock %}'),
        (False),
        id="an html comment reaches no reader either way",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% load static %}\n\n'
            "<!-- Home page -->\n\n{% block content %}\n<h1>Hi</h1>\n"
            "{% endblock %}\n"
        ),
        (False),
        id="a section divider comment between the extends and the block",
    ),
    pytest.param(
        ('{% extends "b.html" %}<!-- <p>x</p> -->{% block a %}x{% endblock %}'),
        (False),
        id="markup inside an html comment",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% block a %}<!-- {% endblock %} -->'
            "<p>lost</p>"
        ),
        (True),
        id="a tag inside an html comment is still read",
    ),
    pytest.param(
        ('{% extends "b.html" %}<!-- oops<p>lost</p>'),
        (True),
        id="an html comment that is never closed opens none",
    ),
    pytest.param(
        ('{% extends "b.html" %}<p>a --> b</p>{% block a %}x{% endblock %}'),
        (True),
        id="an arrow in text closes no html comment",
    ),
    pytest.param(
        ('{% extends "b.html" %}{% block a %}<div>kept</div>{% endblock %}'),
        (False),
        id="html inside a block",
    ),
    pytest.param(
        ('{% extends "b.html" %}{% load static %}{% block a %}x{% endblock %}'),
        (False),
        id="a template tag outside a block runs",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% set y = 1 %}'
            "{% block a %}{{ y }}{% endblock %}"
        ),
        (False),
        id="a top level set",
    ),
    pytest.param(
        ('{% extends "b.html" %}\n\n\n{% block a %}x{% endblock %}'),
        (False),
        id="whitespace only",
    ),
    pytest.param(
        ('{% extends "b.html" %}{# note #}{% block a %}x{% endblock %}'),
        (False),
        id="a template comment",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% comment %}<p>not rendered anyway</p>'
            "{% endcomment %}{% block a %}x{% endblock %}"
        ),
        (False),
        id="a comment block",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% block a %}{% block inner %}<p>nested</p>'
            "{% endblock %}{% endblock %}"
        ),
        (False),
        id="nested blocks",
    ),
    pytest.param(("<div>free</div>"), (False), id="no extends"),
    pytest.param(
        ("<div>free</div>{% block a %}x{% endblock %}"),
        (False),
        id="no extends with blocks",
    ),
    pytest.param(
        ('<p>before</p>{% extends "b.html" %}{% block a %}x{% endblock %}'),
        (False),
        id="content before the extends tag is not this rule's",
    ),
    pytest.param(
        ('{% extends "b.html" %}{{ y }}{% block a %}x{% endblock %}'),
        (False),
        id="a variable is a template tag",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{%- block a -%}<div>kept</div>'
            "{%- endblock -%}"
        ),
        (False),
        id="whitespace control markers on the block tags",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% block a %}'
            "{% blocktrans %}kept{% endblocktrans %}{% endblock %}"
        ),
        (False),
        id="a blocktrans inside a block",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% raw %}<p>x</p>{% endraw %}'
            "{% block a %}x{% endblock %}"
        ),
        (False),
        id="a raw block",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% verbatim %}<p>x</p>{% endverbatim %}'
            "{% block a %}x{% endblock %}"
        ),
        (False),
        id="a verbatim block",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{# djlint:off T042 #}<p>x</p>{# djlint:on #}'
            "{% block a %}x{% endblock %}"
        ),
        (False),
        id="the rule is switched off",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{# djlint:off #}<p>x</p>{# djlint:on #}'
            "{% block a %}x{% endblock %}"
        ),
        (False),
        id="every rule is switched off",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% macro m() %}<p>x</p>{% endmacro %}'
            "{% block a %}{{ m() }}{% endblock %}"
        ),
        (False),
        id="a macro body is output only where it is called",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% set nav %}<p>x</p>{% endset %}'
            "{% block a %}{{ nav }}{% endblock %}"
        ),
        (False),
        id="a block form set captures its body",
    ),
    pytest.param(
        ('{# {% extends "b.html" %} #}<div>free</div>'),
        (False),
        id="an extends tag inside a comment does not run",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% block content %}\n'
            "  {% set body | indent(width=2) %}<p>x</p>{% endset %}\n"
            "  <p>y</p>\n{% endblock %}\n"
        ),
        (False),
        id="a block form set whose filter takes a keyword argument",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% block content %}\n'
            '{% set cfg | tojson(indent=2) %}{"a": 1}{% endset %}\n'
            '<div data-cfg="{{ cfg }}">kept</div>\n{% endblock %}\n'
        ),
        (False),
        id="a keyword argument in a set does not close the block around it",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% set x = "a=b" %}'
            "{% block a %}{{ x }}{% endblock %}<p>lost</p>"
        ),
        (True),
        id="an assigning set with an equals sign in a string",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% partialdef card %}\n'
            '<div class="card">hi</div>\n{% endpartialdef %}\n'
            "{% block content %}x{% endblock %}\n"
        ),
        (False),
        id="a partialdef captures its body",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% partialdef card inline %}\n'
            '<div class="card">hi</div>\n{% endpartialdef %}\n'
            "{% block content %}x{% endblock %}\n"
        ),
        (False),
        id="an inline partialdef captures its body",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% load sekizai_tags %}\n'
            '{% addtoblock "css" %}<link rel="stylesheet" href="/a.css">'
            "{% endaddtoblock %}\n{% block content %}x{% endblock %}\n"
        ),
        (False),
        id="an addtoblock captures its body",
    ),
    pytest.param(
        (
            '{% extends "base.html" %}\n{% load sekizai_tags %}\n'
            '{% addtoblock "js" %}<script src="/a.js"></script>'
            "{% endaddtoblock %}\n{% block content %}x{% endblock %}\n"
        ),
        (False),
        id="an addtoblock holding a script captures its body",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}<!-- djlint:off --><p>x</p>'
            "<!-- djlint:on -->{% block a %}x{% endblock %}"
        ),
        (False),
        id="an html comment switches every rule off",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}\n<!-- djlint:off -->\n<p>x</p>\n'
            "<!-- djlint:on -->\n{% block a %}x{% endblock %}\n"
        ),
        (False),
        id="an html comment switches every rule off over lines",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}<!-- djlint:off T042 -->'
            "{% load static %}<p>x</p>{% load i18n %}<!-- djlint:on -->"
            "{% block a %}x{% endblock %}"
        ),
        (False),
        id="an html comment switches the rule off around a tag",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{{ {"a": {"b": 1}} }}{% block a %}x{% endblock %}'
        ),
        (False),
        id="an output tag holding nested braces",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% include "x.html" with s="%}" %}'
            "{% block a %}x{% endblock %}"
        ),
        (False),
        id="a tag holding its own closing delimiter in a string",
    ),
    pytest.param(
        (
            '{% extends "b.html" %}{% if a == \' %}<div>kept</div>'
            "{% block a %}x{% endblock %}"
        ),
        (True),
        id="a tag with an unclosed quote does not swallow the tags after it",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_t042(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T042" in codes) is reported


def test_t042_reports_each_run_once() -> None:
    source = (
        '{% extends "b.html" %}\n'
        "<p>a</p>\n"
        "{% if x %}\n"
        "<p>b</p>\n"
        "{% endif %}\n"
        "{% block a %}x{% endblock %}\n"
    )
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]

    assert [x for x in findings if x["code"] == "T042"] == [
        {
            "code": "T042",
            "line": "2:0",
            "match": "<p>a</p>",
            "message": MESSAGE,
        },
        {
            "code": "T042",
            "line": "4:0",
            "match": "<p>b</p>",
            "message": MESSAGE,
        },
    ]


def test_t042_reports_a_run_at_its_start() -> None:
    source = (
        '{% extends "b.html" %}\n'
        "<div>\n"
        "<p>lost</p>\n"
        "</div>\n"
        "{% block a %}x{% endblock %}\n"
    )
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]

    assert [x for x in findings if x["code"] == "T042"] == [
        {
            "code": "T042",
            "line": "2:0",
            "match": "<div>\n<p>lost</p>\n</",
            "message": MESSAGE,
        }
    ]


def test_t042_an_arrow_in_text_does_not_split_a_run() -> None:
    source = '{% extends "b.html" %}<p>a --> b</p>{% block a %}x{% endblock %}'
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]

    assert [x for x in findings if x["code"] == "T042"] == [
        {
            "code": "T042",
            "line": "1:22",
            "match": "<p>a --> b</p>",
            "message": MESSAGE,
        }
    ]


def test_t042_an_html_comment_pragma_covers_only_its_own_region() -> None:
    source = (
        '{% extends "b.html" %}\n'
        "<p>a</p>\n"
        "<!-- djlint:off T042 -->\n"
        "<p>b</p>\n"
        "<!-- djlint:on -->\n"
        "{% block x %}{% endblock %}\n"
    )
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]

    assert [x for x in findings if x["code"] == "T042"] == [
        {"code": "T042", "line": "2:0", "match": "<p>a</p>", "message": MESSAGE}
    ]


@pytest.mark.parametrize(
    ("profile", "reported"),
    [
        pytest.param("django", True, id="django"),
        pytest.param("jinja", True, id="jinja"),
        pytest.param("nunjucks", True, id="nunjucks"),
        pytest.param("handlebars", False, id="handlebars"),
        pytest.param("golang", False, id="golang"),
        pytest.param("liquid", False, id="liquid"),
        pytest.param("angular", False, id="angular"),
        pytest.param("html", False, id="html"),
    ],
)
def test_t042_profiles(profile: str, reported: bool) -> None:
    source = '{% extends "b.html" %}<p>lost</p>{% block a %}x{% endblock %}'
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T042" in codes) is reported
