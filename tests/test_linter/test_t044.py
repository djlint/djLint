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
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_t044(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

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
