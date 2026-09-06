"""Test linter code T043.

uv run pytest tests/test_linter/test_t043.py
"""

from __future__ import annotations

import time

import pytest

from djlint.lint import linter
from djlint.rules.T043 import run
from djlint.settings import Config

test_data = [
    pytest.param(
        ("{% block a %}1{% endblock %}{% block a %}2{% endblock %}"),
        (True),
        id="the same name twice",
    ),
    pytest.param(
        (
            "{% block a %}{% block b %}{% endblock %}{% endblock %}"
            "{% block b %}{% endblock %}"
        ),
        (True),
        id="a nested block's name reused after it",
    ),
    pytest.param(
        (
            "{% if x %}{% block a %}1{% endblock %}"
            "{% else %}{% block a %}2{% endblock %}{% endif %}"
        ),
        (True),
        id="exclusive branches are no defence",
    ),
    pytest.param(
        ("{%- block a -%}1{%- endblock -%}{% block a %}2{% endblock %}"),
        (True),
        id="whitespace control markers",
    ),
    pytest.param(
        ("{% block a.b %}{% endblock %}{% block a.b %}{% endblock %}"),
        (True),
        id="a dotted name",
    ),
    pytest.param(
        ("{% block a %}{% endblock %}{%block a%}{% endblock %}"),
        (True),
        id="written without padding",
    ),
    pytest.param(
        ("{% block a %}{% endblock %}{% block a scoped %}{% endblock %}"),
        (True),
        id="a jinja modifier after the name",
    ),
    pytest.param(
        ("{% block a %}1{% endblock %}{% block b %}2{% endblock %}"),
        (False),
        id="two different names",
    ),
    pytest.param(
        ("{% block a %}1{% endblock a %}"),
        (False),
        id="a named endblock is not a second occurrence",
    ),
    pytest.param(
        (
            "{% block a %}1{% endblock %}"
            "{% comment %}{% block a %}2{% endblock %}{% endcomment %}"
        ),
        (False),
        id="a block inside a comment does not count",
    ),
    pytest.param(
        ("{% block a %}{% endblock %}{# {% block a %}{% endblock %} #}"),
        (False),
        id="nor one inside a template comment",
    ),
    pytest.param(
        (
            "{% block a %}{% endblock %}"
            "{% verbatim %}{% block a %}{% endblock %}{% endverbatim %}"
        ),
        (False),
        id="nor one inside verbatim",
    ),
    pytest.param(
        (
            "{% block a %}{% endblock %}"
            "{# djlint:off #}{% block a %}{% endblock %}{# djlint:on #}"
        ),
        (False),
        id="nor one inside a djlint:off region",
    ),
    pytest.param(
        ("{% block Content %}{% endblock %}{% block content %}{% endblock %}"),
        (False),
        id="names that differ in case",
    ),
    pytest.param(
        (
            "{% blocktrans %}x{% endblocktrans %}{% blocktrans %}y{% endblocktrans %}"
        ),
        (False),
        id="blocktrans is not a block",
    ),
    pytest.param(
        ("{% block a %}{% endblock %}{% block a-b %}{% endblock %}"),
        (False),
        id="a name that merely starts the same",
    ),
    pytest.param(
        (
            "{% block a %}{% endblock %}"
            "{% raw %}{% block a %}{% endblock %}{% endraw %}"
        ),
        (False),
        id="nor one inside raw",
    ),
    pytest.param(
        (
            "{% block a %}{% endblock %}"
            "{% verbatim myblock %}{% block a %}{% endblock %}"
            "{% endverbatim myblock %}"
        ),
        (False),
        id="nor one inside a named verbatim",
    ),
    pytest.param(
        (
            "<script>window.C = {% block js_conf %}{}{% endblock %};</script>\n"
            "<script>window.D = {% block js_conf %}{}{% endblock %};</script>"
        ),
        (True),
        id="a script body is text to the engine",
    ),
    pytest.param(
        ("{% block a %}1{% endblock %}<pre>{% block a %}2{% endblock %}</pre>"),
        (True),
        id="so is a pre body",
    ),
    pytest.param(
        ("{% block a %}1{% endblock %}\n<!-- {% block a %}2{% endblock %} -->"),
        (True),
        id="an html comment hides the block from the browser only",
    ),
    pytest.param(
        (
            "{% block a %}1{% endblock %}"
            "{% filter upper %}{% block a %}2{% endblock %}{% endfilter %}"
        ),
        (True),
        id="a filter body is parsed like any other",
    ),
    pytest.param(
        (
            '{% embed "card.twig" %}{% block body %}one{% endblock %}'
            "{% endembed %}\n"
            '{% embed "card.twig" %}{% block body %}two{% endblock %}'
            "{% endembed %}"
        ),
        (False),
        id="two embeds of one partial fill the same block",
    ),
    pytest.param(
        (
            '{% embed "card.twig" %}'
            "{% block body %}one{% endblock %}"
            "{% block body %}two{% endblock %}"
            "{% endembed %}"
        ),
        (True),
        id="but a name repeated inside one embed still collides",
    ),
    pytest.param(
        (
            '{% embed "https://youtu.be/x" %}\n'
            "{% block a %}1{% endblock %}\n"
            "{% block a %}2{% endblock %}"
        ),
        (True),
        id="an embed with no closing tag scopes nothing",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_t043(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T043" in codes) is reported


def test_each_later_occurrence_is_reported_at_its_tag() -> None:
    filename = "test.html"
    config = Config(filename, profile="django")
    source = (
        "{% block a %}\n"
        "{% endblock %}\n"
        "{% block a %}\n"
        "{% endblock %}\n"
        "{% block a %}{% endblock %}\n"
    )

    findings = [
        (error["line"], error["match"])
        for error in linter(config, source, filename, filename)[filename]
        if error["code"] == "T043"
    ]

    assert findings == [("3:0", "{% block a %}"), ("5:0", "{% block a %}")]


@pytest.mark.parametrize(
    "profile",
    [
        pytest.param("django", id="django"),
        pytest.param("jinja", id="jinja"),
        pytest.param("nunjucks", id="nunjucks"),
    ],
)
@pytest.mark.parametrize(
    "source",
    [
        pytest.param(
            '{% embed "card.twig" %}{% block body %}one{% endblock %}'
            "{% endembed %}\n"
            '{% embed "card.twig" %}{% block body %}two{% endblock %}'
            "{% endembed %}",
            id="two embeds of the same partial",
        ),
        pytest.param(
            "{% block content %}{% endblock %}\n"
            '{% embed "card.twig" %}\n'
            "  {% block content %}hi{% endblock %}\n"
            "{% endembed %}",
            id="an embed beside a block of the same name",
        ),
    ],
)
def test_an_embed_fills_another_template(profile: str, source: str) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert "T043" not in codes


def test_a_block_tag_with_no_closing_marker_is_scanned_once() -> None:
    """A file of unterminated tags used to be walked once per tag."""
    filename = "test.html"
    config = Config(filename, profile="django")
    rule = next(
        entry["rule"]
        for entry in config.linter_rules
        if entry["rule"]["name"] == "T043"
    )
    source = "{% block a " * 4000

    start = time.perf_counter()
    errors = run(
        rule=rule, config=config, html=source, filepath=filename, line_ends=[]
    )

    assert errors == ()
    assert time.perf_counter() - start < 2


@pytest.mark.parametrize(
    ("profile", "reported"),
    [
        pytest.param("django", True, id="django"),
        pytest.param("jinja", True, id="jinja"),
        pytest.param("nunjucks", True, id="nunjucks"),
        pytest.param("handlebars", False, id="handlebars is excluded"),
        pytest.param("golang", False, id="golang is excluded"),
        pytest.param("liquid", False, id="liquid is excluded"),
        pytest.param("angular", False, id="angular is excluded"),
        pytest.param("html", False, id="html drops every T rule"),
    ],
)
def test_profiles(profile: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)
    source = "{% block a %}1{% endblock %}{% block a %}2{% endblock %}"

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("T043" in codes) is reported
