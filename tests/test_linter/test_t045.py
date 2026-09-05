"""Test linter code T045.

uv run pytest tests/test_linter/test_t045.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<!-- {% include "debug.html" %} -->'),
        ("django"),
        (True),
        id="an include commented out with an html comment",
    ),
    pytest.param(
        ("<!-- {% if debug %}<p>x</p>{% endif %} -->"),
        ("django"),
        (True),
        id="a block commented out with an html comment",
    ),
    pytest.param(
        ("<!--\n{% load static %}\n-->"),
        ("django"),
        (True),
        id="a comment written over several lines",
    ),
    pytest.param(
        ("<!-- a --><!-- {% if x %}{% endif %} -->"),
        ("django"),
        (True),
        id="a comment touching the one before it",
    ),
    pytest.param(
        ("<!-- {{#if x}}y{{/if}} -->"),
        ("handlebars"),
        (True),
        id="a handlebars section",
    ),
    pytest.param(
        ("<!-- {{~#if x}}y{{~/if}} -->"),
        ("handlebars"),
        (True),
        id="a handlebars section with whitespace control",
    ),
    pytest.param(
        ("<!-- {{> partial}} -->"),
        ("handlebars"),
        (True),
        id="a handlebars partial",
    ),
    pytest.param(
        ("<!-- {{if .X}}y{{end}} -->"), ("golang"), (True), id="a go block"
    ),
    pytest.param(
        ('<!-- {{- template "footer" . -}} -->'),
        ("golang"),
        (True),
        id="a go template call with whitespace control",
    ),
    pytest.param(
        ("<!-- built {{ version }} -->"),
        ("django"),
        (False),
        id="a value printed into a comment",
    ),
    pytest.param(
        ("<!-- {{ block.super }} -->"),
        ("django"),
        (False),
        id="a value whose name is also a go keyword",
    ),
    pytest.param(
        ("<!-- {# a template comment #} -->"),
        ("django"),
        (False),
        id="a template comment inside the html comment",
    ),
    pytest.param(
        ("<!-- {# {% if x %}{% endif %} #} -->"),
        ("django"),
        (False),
        id="a tag inside a template comment inside the html comment",
    ),
    pytest.param(
        ("<!-- {% comment %}{% if x %}{% endif %}{% endcomment %} -->"),
        ("django"),
        (False),
        id="a tag inside a comment block inside the html comment",
    ),
    pytest.param(
        ("<!-- djlint:off -->{% if x %}{% endif %}<!-- djlint:on -->"),
        ("django"),
        (False),
        id="the djlint pragmas hold no tag",
    ),
    pytest.param(
        ("{# <!-- {% if x %}{% endif %} --> #}"),
        ("django"),
        (False),
        id="the html comment is inside a template comment",
    ),
    pytest.param(
        ("{% comment %}<!-- {% if x %}{% endif %} -->{% endcomment %}"),
        ("django"),
        (False),
        id="the html comment is inside a comment block",
    ),
    pytest.param(
        ("{% verbatim %}<!-- {% if x %}{% endif %} -->{% endverbatim %}"),
        ("django"),
        (False),
        id="the html comment is inside a verbatim block",
    ),
    pytest.param(
        ("{# djlint:off T045 #}<!-- {% if x %}{% endif %} -->"),
        ("django"),
        (False),
        id="the rule is switched off",
    ),
    pytest.param(
        (
            '<!--[if lt IE 9]><script src="{% static "shiv.js" %}"></script><![endif]-->'
        ),
        ("django"),
        (False),
        id="a conditional comment is markup for the browser it names",
    ),
    pytest.param(
        ('<!--[if !mso]><!--><p>{% trans "x" %}</p><!--<![endif]-->'),
        ("django"),
        (False),
        id="the markup a revealed conditional comment shows to every other browser",
    ),
    pytest.param(
        ('<!--><p>{% trans "x" %}</p>'),
        ("django"),
        (False),
        id="an empty comment closed by its first angle bracket",
    ),
    pytest.param(
        ("<!-- {{! handlebars comment }} -->"),
        ("handlebars"),
        (False),
        id="a handlebars comment inside the html comment",
    ),
    pytest.param(
        ("<!-- {{!-- {{#if x}}{{/if}} --}} -->"),
        ("handlebars"),
        (False),
        id="a section inside a handlebars comment inside the html comment",
    ),
    pytest.param(
        ("<!-- {{/* go comment */}} -->"),
        ("golang"),
        (False),
        id="a go comment inside the html comment",
    ),
    pytest.param(
        ("<!-- plain comment -->"), ("django"), (False), id="a plain comment"
    ),
]


@pytest.mark.parametrize(("source", "profile", "reported"), test_data)
def test_t045(source: str, profile: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T045" in codes) is reported
