"""Test linter code H053.

uv run pytest tests/test_linter/test_h053.py
"""

from __future__ import annotations

import time

import pytest

from djlint.lint import linter
from djlint.rules import H053
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
    pytest.param(
        (
            '{% if x %}<div id="p"></div>{%\nelse\n%}'
            '<div id="p"></div>{% endif %}'
        ),
        (False),
        id="a newline between the delimiters and the tag name",
    ),
    pytest.param(
        (
            '{%\tif x\t%}<div id="p"></div>{%\telse\t%}'
            '<div id="p"></div>{%\tendif\t%}'
        ),
        (False),
        id="a tab between the delimiters and the tag name",
    ),
    pytest.param(
        (
            '{%\n  if x\n%}<div id="p"></div>{%\n  else\n%}'
            '<div id="p"></div>{%\n  endif\n%}'
        ),
        (False),
        id="a tag broken over lines",
    ),
    pytest.param(
        (
            '{% ifequal a b %}<div id="x"></div>{% else %}'
            '<div id="x"></div>{% endifequal %}'
        ),
        (False),
        id="the branches of an ifequal are exclusive",
    ),
    pytest.param(
        (
            '{% ifnotequal a b %}<div id="x"></div>{% else %}'
            '<div id="x"></div>{% endifnotequal %}'
        ),
        (False),
        id="the branches of an ifnotequal are exclusive",
    ),
    pytest.param(
        (
            '<template id="ta"><li id="row"></li></template>'
            '<template id="tb"><li id="row"></li></template>'
        ),
        (False),
        id="each template holds a document fragment of its own",
    ),
    pytest.param(
        (
            '<ul id="list"></ul><template id="row-tpl">'
            '<li id="row"><span id="label"></span></li></template>'
            '<li id="row"></li>'
        ),
        (False),
        id="a template fragment and the document around it",
    ),
    pytest.param(
        ('<template><li id="row"></li><li id="row"></li></template>'),
        (True),
        id="twice inside one template fragment",
    ),
    pytest.param(
        ('<template id="t"></template><div id="t"></div>'),
        (True),
        id="a template carries its own id in the document",
    ),
    pytest.param(
        (
            '{% ifequal a b %}<div id="x"></div>{% endifequal %}'
            '<div id="x"></div>'
        ),
        (True),
        id="the body of an ifequal and the document after it",
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
        pytest.param(
            "handlebars",
            '{{#if a}}<div id="x"></div>{{else if b}}<div id="x"></div>{{/if}}',
            id="a handlebars chained condition",
        ),
        pytest.param(
            "handlebars",
            '{{#if a}}<div id="p"></div>{{else unless b}}'
            '<div id="p"></div>{{/if}}',
            id="a handlebars chained unless",
        ),
        pytest.param(
            "handlebars",
            '{{#if a}}<div id="p"></div>{{ else if b }}'
            '<div id="p"></div>{{/if}}',
            id="a spaced handlebars chained condition",
        ),
        pytest.param(
            "handlebars",
            '{{#myHelper x}}<div id="p"></div>{{else}}'
            '<div id="p"></div>{{/myHelper}}',
            id="the inverse section of a custom block helper",
        ),
        pytest.param(
            "handlebars",
            '{{#link-to "a"}}<div id="p"></div>{{else}}'
            '<div id="p"></div>{{/link-to}}',
            id="the inverse section of a named block helper",
        ),
        pytest.param(
            "handlebars",
            '{{#user}}<div id="p"></div>{{^}}<div id="p"></div>{{/user}}',
            id="the inverse section of a mustache section",
        ),
        pytest.param(
            "golang",
            '{{\tif .A\t}}<div id="p"></div>{{\telse\t}}'
            '<div id="p"></div>{{\tend\t}}',
            id="a tab between the golang delimiters and the tag name",
        ),
        pytest.param(
            "all",
            '{{#if a}}<div id="x"></div>{{else if b}}<div id="x"></div>{{/if}}',
            id="a handlebars chained condition with no profile",
        ),
        pytest.param(
            "all",
            '{{if .A}}<div id="x"></div>{{else}}<div id="x"></div>{{end}}',
            id="a golang condition with no profile",
        ),
        pytest.param(
            "all",
            '{% if x %}<div id="x"></div>{% elsif y %}'
            '<div id="x"></div>{% endif %}',
            id="a liquid elsif with no profile",
        ),
        pytest.param(
            "all",
            '{% case x %}{% when "a" %}<div id="x"></div>'
            '{% when "b" %}<div id="x"></div>{% endcase %}',
            id="a liquid case with no profile",
        ),
    ],
)
def test_h053_branches_in_other_profiles(profile: str, source: str) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]

    assert "H053" not in [error["code"] for error in findings]


def test_h053_a_block_helper_body_is_not_a_branch() -> None:
    """The inverse section of a helper branches, its body alone does not."""
    filename = "test.html"
    config = Config(filename, profile="handlebars")
    source = '{{#myHelper}}<div id="p"></div>{{/myHelper}}<div id="p"></div>'

    findings = linter(config, source, filename, filename)[filename]

    assert "H053" in [error["code"] for error in findings]


@pytest.mark.parametrize(
    "source",
    [
        pytest.param("{" * 20000, id="a run of braces"),
        pytest.param("{{" * 10000, id="a run of output delimiters"),
        pytest.param("{%" * 10000, id="a run of statement delimiters"),
        pytest.param(
            "<script>" + "{" * 20000 + "</script>",
            id="a run of braces in a script",
        ),
    ],
)
def test_h053_reads_a_run_of_delimiters_in_one_pass(source: str) -> None:
    """A pattern scanning for a closing delimiter reads the file per brace.

    The rule is timed on its own: the tag tokenizer djLint shares is
    quadratic over a brace run written inside a tag, which no change here
    can help, so the run is timed where no tag holds it. 20000 braces
    spent 15 seconds in this scan before it was made linear.
    """
    filename = "test.html"
    config = Config(filename, profile="django")
    rule = {"name": "H053", "message": "Id is used more than once in the file."}

    started = time.perf_counter()
    findings = H053.run(rule, config, source, filename, [])
    elapsed = time.perf_counter() - started

    assert not findings
    assert elapsed < 2
