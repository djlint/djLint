"""Test linter code T041.

uv run pytest tests/test_linter/test_t041.py
"""

from __future__ import annotations

import time

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        (
            '{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}'
        ),
        (True),
        id="django rejects a parent chosen inside a branch",
    ),
    pytest.param(
        ('{% if x %}{% extends "a.html" %}{% endif %}'),
        (True),
        id="django rejects an extends guarded by an if",
    ),
    pytest.param(
        ('{% if a %}\n  {% extends "base.html" %}\n{% endif %}\n'),
        (True),
        id="django rejects an extends guarded by an if over three lines",
    ),
    pytest.param(
        ('{% elif a %}{% extends "base.html" %}'),
        (True),
        id="django rejects an extends guarded by an elif",
    ),
    pytest.param(
        ('{% if a %}{% if b %}{% extends "base.html" %}{% endif %}{% endif %}'),
        (True),
        id="django rejects an extends guarded by nested ifs",
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
        (True),
        id="an html comment before it",
    ),
    pytest.param(
        ('<!-- Copyright 2026 Acme Corp. -->\n{% extends "base.html" %}'),
        (True),
        id="a licence html comment before it",
    ),
    pytest.param(
        (
            '<!--\n  SPDX-License-Identifier: MIT\n-->\n{% extends "base.html" %}'
        ),
        (True),
        id="an html comment over three lines before it",
    ),
    pytest.param(
        ('<!-- <!DOCTYPE html> -->{% extends "base.html" %}'),
        (True),
        id="a doctype inside an html comment before it",
    ),
    pytest.param(
        ('<!--[if IE]><p>x</p><![endif]-->{% extends "base.html" %}'),
        (True),
        id="a conditional comment before it",
    ),
    pytest.param(
        (
            "{% comment %}\nA note about this template.\n{% endcomment %}\n"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a comment block over three lines before it",
    ),
    pytest.param(
        (
            "{% comment %}\n  templates/app/page.html\n"
            "  Renders the profile page.\n{% endcomment %}\n"
            '{% extends "base.html" %}\n{% block content %}{% endblock %}\n'
        ),
        (False),
        id="a comment block header before it",
    ),
    pytest.param(
        (
            "{% comment %}\n<p>old markup</p>\n{% endcomment %}\n"
            '{% extends "base.html" %}'
        ),
        (False),
        id="markup commented out over lines before it",
    ),
    pytest.param(
        (
            '{% comment "translators: note" %}\nhi\n{% endcomment %}\n'
            '{% extends "base.html" %}'
        ),
        (False),
        id="a comment block with a note before it",
    ),
    pytest.param(
        ('{%comment%}\nnote\n{%endcomment%}\n{% extends "base.html" %}'),
        (False),
        id="a comment block written without spaces before it",
    ),
    pytest.param(
        ('{% comment %}note\n{% endcomment %}{% extends "base.html" %}'),
        (False),
        id="a comment block closed on the next line before it",
    ),
    pytest.param(
        (
            "{% comment %}\n"
            '{% extends "old.html" %}\n'
            "{% endcomment %}\n"
            '{% extends "base.html" %}'
        ),
        (False),
        id="an extends inside a comment block over lines is not the first",
    ),
    pytest.param(
        (
            "{% verbatim myblock %}{% load x %}{% endverbatim myblock %}"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a load inside a named verbatim block",
    ),
    pytest.param(
        (
            "{% verbatim myblock %}\n{{ vue }}\n{% endverbatim myblock %}\n"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a named verbatim block over lines before it",
    ),
    pytest.param(
        (
            "{% comment %}djlint:off{% endcomment %}{% load x %}"
            "{% comment %}djlint:on{% endcomment %}"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a load inside a comment block djlint:off region",
    ),
    pytest.param(
        (
            "{% comment %}djlint:off{% endcomment %}\n{% load x %}\n"
            "{% comment %}djlint:on{% endcomment %}\n"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a comment block djlint:off region over lines",
    ),
    pytest.param(
        (
            "<!-- djlint:off -->\n{% load x %}\n<!-- djlint:on -->\n"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a load inside an html comment djlint:off region",
    ),
    pytest.param(
        (
            "<!-- djlint:off T041 -->{% load x %}<!-- djlint:on -->"
            '{% extends "base.html" %}'
        ),
        (False),
        id="a load inside an html djlint:off region naming the rule",
    ),
    pytest.param(
        (
            "{# djlint:off H025 #}{% load x %}{# djlint:on #}"
            '{% extends "base.html" %}'
        ),
        (True),
        id="a load inside a djlint:off region naming another rule",
    ),
    pytest.param(
        ('{% blocktrans %}Hi{% endblocktrans %}{% extends "base.html" %}'),
        (True),
        id="a blocktrans block before it",
    ),
    pytest.param(
        (
            "{% blocktrans %}\nHello\n{% endblocktrans %}\n"
            '{% extends "base.html" %}'
        ),
        (True),
        id="a blocktrans block over lines before it",
    ),
    pytest.param(
        ('{% filter upper %}hi{% endfilter %}{% extends "base.html" %}'),
        (True),
        id="a filter block before it",
    ),
    pytest.param(
        ('<?php echo 1; ?>{% extends "base.html" %}'),
        (True),
        id="a php block before it",
    ),
    pytest.param(
        ('\ufeff---\ntitle: x\n---\n{% extends "base.html" %}'),
        (False),
        id="front matter behind a byte order mark",
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
        (
            '{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}'
        ),
        ("jinja"),
        (False),
        id="a parent chosen inside a branch, as jinja documents",
    ),
    pytest.param(
        ('{% if x %}{% extends "a.html" %}{% endif %}'),
        ("jinja"),
        (False),
        id="an extends guarded by an if",
    ),
    pytest.param(
        ('{% if x %}{% extends "a.html" %}{% endif %}'),
        ("nunjucks"),
        (False),
        id="nunjucks takes an extends guarded by an if",
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


def test_t041_reads_an_unclosed_prefix_once() -> None:
    """A prefix of openings that never close costs one pass, not one each.

    Sixteen thousand unclosed `{#` inside an html comment took thirteen
    seconds when each of them was scanned to the end of the file.
    """
    filename = "test.html"
    config = Config(filename, profile="django")
    source = "<!--" + ("{#" * 16000) + "-->" + '{% extends "base.html" %}'

    started = time.perf_counter()
    findings = linter(config, source, filename, filename)[filename]
    elapsed = time.perf_counter() - started

    assert "T041" in [error["code"] for error in findings]
    assert elapsed < 5


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
