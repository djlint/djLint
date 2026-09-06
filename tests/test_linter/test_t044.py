"""Test linter code T044.

uv run pytest tests/test_linter/test_t044.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(("{{ if x }}"), (True), id="an if written as an output tag"),
    pytest.param(
        ("{{ url 'home' }}"), (True), id="a url tag given a route name"
    ),
    pytest.param(("{{ for i in items }}"), (True), id="a for loop"),
    pytest.param(("{{ set total = 1 }}"), (True), id="a set given a value"),
    pytest.param(
        ('{{ include "a.html" }}'), (True), id="an include given a template"
    ),
    pytest.param(("{{ endif }}"), (True), id="a bare closing keyword"),
    pytest.param(("{{ else }}"), (True), id="a bare branch keyword"),
    pytest.param(
        ("{{- endfor -}}"),
        (True),
        id="a closing keyword with whitespace control",
    ),
    pytest.param(
        ("<a href=\"{{ url 'home' }}\">x</a>"),
        (True),
        id="inside an attribute value",
    ),
    pytest.param(
        ("{{ if not user.is_active }}"),
        (True),
        id="a negated if is still a statement",
    ),
    pytest.param(
        ("{{ if in_stock }}"),
        (True),
        id="an argument that merely starts with an expression word",
    ),
    pytest.param(("{{ url }}"), (False), id="a bare keyword is a variable"),
    pytest.param(
        ('{{ url|default:"/" }}'), (False), id="a bare keyword with a filter"
    ),
    pytest.param(
        ("{{ set.name }}"), (False), id="an attribute of a variable named set"
    ),
    pytest.param(("{{ block.super }}"), (False), id="block.super"),
    pytest.param(
        ("{{ endpoint }}"), (False), id="a name that merely starts with end"
    ),
    pytest.param(
        ("{{ ending }}"), (False), id="another name starting with end"
    ),
    pytest.param(
        ("{{ item.if }}"), (False), id="a keyword as an attribute name"
    ),
    pytest.param(("{% if x %}{% endif %}"), (False), id="a real block tag"),
    pytest.param(
        ("{{ include_me }}"),
        (False),
        id="a name that merely starts with a keyword",
    ),
    pytest.param(("{{ form }}"), (False), id="form is not for"),
    pytest.param(('{{ url ~ "/x" }}'), (False), id="a jinja concatenation"),
    pytest.param(
        ('{{ url if url else "#" }}'),
        (False),
        id="a jinja conditional expression",
    ),
    pytest.param(("{{ url is defined }}"), (False), id="a jinja test"),
    pytest.param(
        ("{{ url not in seen }}"), (False), id="a jinja membership test"
    ),
    pytest.param(("{{{ if x }}}"), (False), id="a handlebars triple stash"),
    pytest.param(("{# {{ if x }} #}"), (False), id="inside a template comment"),
    pytest.param(
        ("{% verbatim %}{{ if x }}{% endverbatim %}"),
        (False),
        id="inside a verbatim block",
    ),
    pytest.param(
        ("{% verbatim myblock %}{{ if x }}{% endverbatim myblock %}"),
        (False),
        id="inside a named verbatim block",
    ),
    pytest.param(
        (
            "{% verbatim vueapp %}\n"
            '<div id="app">\n'
            "  <a :href=\"{{ url ? url : '#' }}\">go</a>\n"
            "</div>\n"
            "{% endverbatim vueapp %}"
        ),
        (False),
        id="a vue template inside a named verbatim block",
    ),
    pytest.param(
        ("{% verbatim hbs %}\n<div>{{ else }}</div>\n{% endverbatim hbs %}"),
        (False),
        id="a handlebars branch inside a named verbatim block",
    ),
    pytest.param(
        ("{%- verbatim tpl -%}{{ endif }}{%- endverbatim tpl -%}"),
        (False),
        id="a named verbatim block with whitespace control",
    ),
    pytest.param(
        ("{% verbatim a %}{{ if x }}{% endverbatim a %}{{ if y }}"),
        (True),
        id="a statement after a named verbatim block is still reported",
    ),
    pytest.param(
        ('{% trans "Write {{ if x }} instead" %}'),
        (False),
        id="quoted inside a block tag",
    ),
    pytest.param(
        ('{% trans "Write {{ if x }} instead" %}{{ if y }}'),
        (True),
        id="a statement after a quoted argument is still reported",
    ),
    pytest.param(("{{ url , name }}"), (False), id="a comma after a name"),
    pytest.param(
        ('{{ from "x" import y }}'),
        (True),
        id="an import written as an output tag",
    ),
    pytest.param(
        ("{{ from - 1 }}"),
        (False),
        id="an expression starting with a variable named from",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_t044(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T044" in codes) is reported


expression_data = [
    pytest.param(
        ("{{ url ? url : '#' }}"), ("jinja"), (False), id="a twig ternary"
    ),
    pytest.param(
        ("{{ url ?? '/' }}"), ("jinja"), (False), id="a twig null coalesce"
    ),
    pytest.param(("{{ url ?: '/' }}"), ("jinja"), (False), id="a twig elvis"),
    pytest.param(
        ("<img src=\"{{ url ?? '/static/x.png' }}\">"),
        ("jinja"),
        (False),
        id="a twig null coalesce in an attribute",
    ),
    pytest.param(
        ("{{ url\n   ? url\n   : '#' }}"),
        ("jinja"),
        (False),
        id="a twig ternary across lines",
    ),
    pytest.param(
        ("{{ include ('sidebar.html') }}"),
        ("jinja"),
        (False),
        id="a space before a call's arguments",
    ),
    pytest.param(
        ("{{ block ('title') }}"),
        ("jinja"),
        (False),
        id="a space before the block function's arguments",
    ),
    pytest.param(
        ("{{ url ('home') }}"),
        ("jinja"),
        (False),
        id="a space before the url function's arguments",
    ),
    pytest.param(
        ("{{ now ('%Y') }}"),
        ("jinja"),
        (False),
        id="a space before the now function's arguments",
    ),
    pytest.param(
        ("{{ filter [0] }}"),
        ("jinja"),
        (False),
        id="a space before a subscript",
    ),
    pytest.param(
        ("{{ url , name }}"), ("jinja"), (False), id="a space before a comma"
    ),
    pytest.param(
        ("{{ block .super }}"),
        ("jinja"),
        (False),
        id="a space before an attribute",
    ),
    pytest.param(
        ("{{ set : 1 }}"), ("jinja"), (False), id="a space before a colon"
    ),
    pytest.param(
        ("{{+ if x }}"),
        ("jinja"),
        (True),
        id="an if with plus whitespace control",
    ),
    pytest.param(
        ("{{+ endif }}"),
        ("jinja"),
        (True),
        id="a closing keyword with plus whitespace control",
    ),
    pytest.param(
        ("{{+ endif }}"),
        ("nunjucks"),
        (True),
        id="nunjucks reads plus whitespace control too",
    ),
    pytest.param(
        ("{{ if -1 > count }}"),
        ("jinja"),
        (True),
        id="an if whose argument starts with a minus",
    ),
    pytest.param(
        ("{{ if !user }}"),
        ("nunjucks"),
        (True),
        id="an if whose argument starts with a bang",
    ),
    pytest.param(
        ("{{ if +x }}"),
        ("jinja"),
        (True),
        id="an if whose argument starts with a plus",
    ),
]


@pytest.mark.parametrize(("source", "profile", "reported"), expression_data)
def test_t044_expressions(source: str, profile: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T044" in codes) is reported


@pytest.mark.parametrize(
    ("profile", "reported"),
    [
        pytest.param("django", True, id="django"),
        pytest.param("jinja", True, id="jinja"),
        pytest.param("nunjucks", True, id="nunjucks"),
        pytest.param("golang", False, id="golang writes if as an output tag"),
        pytest.param("handlebars", False, id="handlebars has its own if"),
        pytest.param("angular", False, id="angular"),
        pytest.param("html", False, id="html runs no template rules"),
    ],
)
def test_t044_profiles(profile: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, "{{ if x }}", filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T044" in codes) is reported
