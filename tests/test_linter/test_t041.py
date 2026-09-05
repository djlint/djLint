"""Test linter code T041.

uv run pytest tests/test_linter/test_t041.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        (
            '{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}'
        ),
        (False),
        id="a parent chosen inside a branch, as jinja documents",
    ),
    pytest.param(
        ('{% if x %}{% extends "a.html" %}{% endif %}'),
        (False),
        id="an extends guarded by an if",
    ),
    pytest.param(
        ('{% load static %}{% extends "base.html" %}'),
        (True),
        id="a load before it",
    ),
    pytest.param(
        ('{{ x }}{% extends "base.html" %}'), (True), id="a variable before it"
    ),
    pytest.param(
        ('<!DOCTYPE html>{% extends "base.html" %}'),
        (True),
        id="a doctype before it",
    ),
    pytest.param(
        ('hello {% extends "base.html" %}'), (True), id="text before it"
    ),
    pytest.param(
        ('{% if a %}{% endif %}{% extends "base.html" %}'),
        (True),
        id="a closed block before it",
    ),
    pytest.param(
        ('{% load static %}\n{% extends "base.html" %}'),
        (True),
        id="a load on the line above",
    ),
    pytest.param(
        ('<script>x</script>{% extends "base.html" %}'),
        (True),
        id="a script before it",
    ),
    pytest.param(
        ('{% extends "base.html" %}{% block a %}x{% endblock %}'),
        (False),
        id="extends first",
    ),
    pytest.param(
        ('{# a comment #}{% extends "base.html" %}'),
        (False),
        id="a template comment before it",
    ),
    pytest.param(
        ('\n\n  {% extends "base.html" %}'),
        (False),
        id="leading whitespace only",
    ),
    pytest.param(
        ('\ufeff{% extends "base.html" %}'),
        (False),
        id="a byte order mark is whitespace",
    ),
    pytest.param(
        ('{%- extends "base.html" -%}'), (False), id="whitespace control form"
    ),
    pytest.param(
        ('{%+ extends "base.html" %}'),
        (False),
        id="plus whitespace control form",
    ),
    pytest.param(
        ("{% block a %}x{% endblock %}"), (False), id="no extends at all"
    ),
    pytest.param(
        ('{% comment %}{% load x %}{% endcomment %}{% extends "base.html" %}'),
        (False),
        id="a load inside a comment block",
    ),
    pytest.param(
        ('{% comment %}hello{% endcomment %}{% extends "base.html" %}'),
        (False),
        id="text inside a comment block",
    ),
    pytest.param(
        (
            "{% verbatim %}{% load x %}{% endverbatim %}"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a load inside a verbatim block",
    ),
    pytest.param(
        (
            "{# djlint:off #}{% load x %}{# djlint:on #}"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a load inside a djlint:off region",
    ),
    pytest.param(
        ('{% load x %}{# djlint:off T041 #}{% extends "base.html" %}'),
        (False),
        id="the extends itself is inside a djlint:off region",
    ),
    pytest.param(
        (
            '{% comment %}{% extends "a.html" %}{% endcomment %}'
            '{% extends "b.html" %}'
        ),
        (False),
        id="an extends inside a comment block is not the first",
    ),
    pytest.param(
        ('{% extends "a.html" %}{% extends "b.html" %}'),
        (False),
        id="only the first extends matters",
    ),
    pytest.param(
        ('<!-- x -->{% extends "base.html" %}'),
        (False),
        id="an html comment is not linted",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_t041(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T041" in codes) is reported


profile_data = [
    pytest.param(
        ('{% raw %}{% load x %}{% endraw %}{% extends "base.html" %}'),
        ("jinja"),
        (False),
        id="a load inside a raw block",
    ),
    pytest.param(
        ('{% load x %}{% extends "base.html" %}'),
        ("jinja"),
        (True),
        id="jinja is checked",
    ),
    pytest.param(
        ('{% load x %}{% extends "base.html" %}'),
        ("nunjucks"),
        (True),
        id="nunjucks is checked",
    ),
    pytest.param(
        ('{% load x %}{% extends "base.html" %}'),
        ("handlebars"),
        (False),
        id="handlebars is excluded",
    ),
    pytest.param(
        ('{% load x %}{% extends "base.html" %}'),
        ("golang"),
        (False),
        id="golang is excluded",
    ),
    pytest.param(
        ('{% load x %}{% extends "base.html" %}'),
        ("liquid"),
        (False),
        id="liquid is excluded",
    ),
    pytest.param(
        ('{% load x %}{% extends "base.html" %}'),
        ("angular"),
        (False),
        id="angular is excluded",
    ),
]


@pytest.mark.parametrize(("source", "profile", "reported"), profile_data)
def test_t041_profiles(source: str, profile: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T041" in codes) is reported


def test_t041_reports_the_extends_tag() -> None:
    filename = "test.html"
    config = Config(filename, profile="django")
    source = '{% load static %}\n{% extends "base.html" %}\n'

    findings = linter(config, source, filename, filename)[filename]

    assert [error for error in findings if error["code"] == "T041"] == [
        {
            "code": "T041",
            "line": "2:0",
            "match": '{% extends "base.htm',
            "message": "Extends tag should be the first tag in the template.",
        }
    ]
