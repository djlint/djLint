"""Test linter code T043.

uv run pytest tests/test_linter/test_t043.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
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
