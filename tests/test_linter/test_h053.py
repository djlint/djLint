"""Test linter code H053.

uv run pytest tests/test_linter/test_h053.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<div id="a"></div><span id="a"></span>'),
        (True),
        id="the same id on two elements",
    ),
    pytest.param(
        ('<div id="a"></div><div>{% if x %}<b id="a"></b>{% endif %}</div>'),
        (True),
        id="one unconditional, one conditional",
    ),
    pytest.param(
        ("<div id='a'></div><div id=\"a\"></div>"),
        (True),
        id="the quote style differs but the value is the same",
    ),
    pytest.param(
        ("<div id=a></div><div id=a></div>"),
        (True),
        id="written without quotes",
    ),
    pytest.param(
        ('{% for i in xs %}<b id="row"></b>{% endfor %}<i id="row"></i>'),
        (True),
        id="inside a for loop and outside it",
    ),
    pytest.param(
        ('<div id="a"></div>{% block b %}<div id="a"></div>{% endblock %}'),
        (True),
        id="a block is not a branch",
    ),
    pytest.param(
        (
            '{% if x %}<div id="a"></div>{% endif %}'
            '{% if y %}<div id="a"></div>{% endif %}'
        ),
        (True),
        id="two separate conditions can both be true",
    ),
    pytest.param(
        (
            '{% if x %}<div id="a"></div>'
            '{% if y %}<div id="a"></div>{% endif %}{% endif %}'
        ),
        (True),
        id="a nested condition inside the same branch",
    ),
    pytest.param(
        ('<div id="a"></div><div id="b"></div>'),
        (False),
        id="two different ids",
    ),
    pytest.param(
        ('{% if x %}<div id="a"></div>{% else %}<div id="a"></div>{% endif %}'),
        (False),
        id="the if and else branches are exclusive",
    ),
    pytest.param(
        (
            '{% if x %}<div id="a"></div>{% elif y %}<div id="a"></div>{% endif %}'
        ),
        (False),
        id="the if and elif branches are exclusive",
    ),
    pytest.param(
        (
            '{% for i in xs %}<div id="a"></div>'
            '{% empty %}<div id="a"></div>{% endfor %}'
        ),
        (False),
        id="the loop body and its empty clause are exclusive",
    ),
    pytest.param(
        (
            '{% if x %}{% mytag %}x{% endmytag %}<div id="a"></div>'
            '{% else %}<div id="a"></div>{% endif %}'
        ),
        (False),
        id="the closer of an unknown block does not close the if",
    ),
    pytest.param(
        ('% if x:\n<div id="a"></div>\n% else:\n<div id="a"></div>\n% endif\n'),
        (False),
        id="the branches of a mako if are exclusive",
    ),
    pytest.param(
        ('% if x:\n<div id="a"></div>\n% endif\n<div id="a"></div>\n'),
        (True),
        id="one inside a mako if, one outside",
    ),
    pytest.param(
        ('<div id="a"></div><div id="A"></div>'),
        (False),
        id="ids are case sensitive",
    ),
    pytest.param(
        ('<div id="{{ n }}"></div><div id="{{ n }}"></div>'),
        (False),
        id="a value written by a template tag",
    ),
    pytest.param(
        ('<div id="row-{{ i }}"></div><div id="row-{{ i }}"></div>'),
        (False),
        id="a value partly written by a template tag",
    ),
    pytest.param(
        ('<div data-id="a"></div><div id="a"></div>'),
        (False),
        id="a name that merely ends in id",
    ),
    pytest.param(
        ('<div id="a"></div>{% comment %}<div id="a"></div>{% endcomment %}'),
        (False),
        id="inside a template comment",
    ),
    pytest.param(
        ('<p title=\'<b id="a">\'></p><div id="a"></div>'),
        (False),
        id="text inside an attribute value is not a tag",
    ),
    pytest.param(
        (
            '<div id="a"></div><!-- djlint:off -->'
            '<div id="a"></div><!-- djlint:on -->'
        ),
        (False),
        id="inside a djlint:off region",
    ),
    pytest.param(
        ('<script>var s = \'<div id="a">\';</script><div id="a"></div>'),
        (False),
        id="text inside a script is not a tag",
    ),
    pytest.param(
        ('<div id=""></div><div id=""></div>'),
        (False),
        id="an empty value names nothing",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h053(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H053" in codes) is reported


def test_h053_reports_the_later_id() -> None:
    filename = "test.html"
    config = Config(filename, profile="django")
    source = (
        '{% if x %}<a id="a"></a>{% else %}<b id="a"></b>{% endif %}\n'
        '<i id="a"></i>\n'
    )

    findings = [
        error
        for error in linter(config, source, filename, filename)[filename]
        if error["code"] == "H053"
    ]

    assert findings == [
        {
            "code": "H053",
            "line": "2:3",
            "match": 'id="a"',
            "message": "Id is used more than once in the file.",
        }
    ]


@pytest.mark.parametrize(
    ("profile", "source"),
    [
        pytest.param(
            "handlebars",
            '{{#if x}}<div id="a"></div>{{else}}<div id="a"></div>{{/if}}',
            id="handlebars",
        ),
        pytest.param(
            "golang",
            '{{if .X}}<div id="a"></div>{{else}}<div id="a"></div>{{end}}',
            id="golang",
        ),
        pytest.param(
            "jinja",
            '{% if x %}<div id="a"></div>{% else %}<div id="a"></div>{% endif %}',
            id="jinja",
        ),
    ],
)
def test_h053_branches_in_other_profiles(profile: str, source: str) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]

    assert "H053" not in [error["code"] for error in findings]
