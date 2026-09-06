"""Test linter code H054.

uv run pytest tests/test_linter/test_h054.py
"""

from __future__ import annotations

import time

import pytest

from djlint.lint import linter
from djlint.rules import H054
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<a href="/x"><button>Go</button></a>'),
        (True),
        id="a button inside a link",
    ),
    pytest.param(
        ('<button><a href="/x">Go</a></button>'),
        (True),
        id="a link inside a button",
    ),
    pytest.param(
        ('<a href="/x"><input type="text"></a>'),
        (True),
        id="an input inside a link",
    ),
    pytest.param(
        ("<button><select><option>a</option></select></button>"),
        (True),
        id="a select inside a button",
    ),
    pytest.param(
        ('<a href="{{ url }}"><button type="button">x</button></a>'),
        (True),
        id="an href written by a template tag counts",
    ),
    pytest.param(
        ('<a href="/x"><span><button>deep</button></span></a>'),
        (True),
        id="the control need not be a direct child",
    ),
    pytest.param(
        ("<a href><button>x</button></a>"),
        (True),
        id="a valueless href still makes a link",
    ),
    pytest.param(
        ('<a href="/x"><textarea></textarea></a>'),
        (True),
        id="a textarea inside a link",
    ),
    pytest.param(
        ('<button type="button"><input type="file"></button>'),
        (True),
        id="a file input inside a button",
    ),
    pytest.param(
        ('<a href="/x"><a>plain</a><button>x</button></a>'),
        (True),
        id="closing a plain link does not end the one around it",
    ),
    pytest.param(
        ('<A HREF="/x"><BUTTON>x</BUTTON></A>'),
        (True),
        id="read whatever the case",
    ),
    pytest.param(
        ('<a href="/x">text</a><button>x</button>'), (False), id="siblings"
    ),
    pytest.param(
        ("<a><button>x</button></a>"),
        (False),
        id="a link with no href is not interactive",
    ),
    pytest.param(
        ("<button><span>x</span></button>"),
        (False),
        id="plain content inside a button",
    ),
    pytest.param(
        ('<a href="/x"><input type="hidden" name="t"></a>'),
        (False),
        id="a hidden input is not a control",
    ),
    pytest.param(
        ('<label><input type="checkbox"> x</label>'),
        (False),
        id="a label is not a container the rule watches",
    ),
    pytest.param(
        ('<a href="/x">1</a><a href="/y">2</a>'), (False), id="sibling links"
    ),
    pytest.param(
        ("<button>x</button><button>y</button>"), (False), id="sibling buttons"
    ),
    pytest.param(
        ('<p title="<a href=/x><button>t</button></a>">x</p>'),
        (False),
        id="markup inside an attribute value is text",
    ),
    pytest.param(
        ('<a data-href="/x"><button>x</button></a>'),
        (False),
        id="a name that merely ends in href",
    ),
    pytest.param(
        ('<a href="/x"><input type="{{ t }}"></a>'),
        (False),
        id="a type written by a template tag is unknowable",
    ),
    pytest.param(
        ("<ul><li><button>x</buton></li><li><button>y</button></li></ul>"),
        (False),
        id="a button left open ends with the element around it",
    ),
    pytest.param(
        ('{% comment %}<a href="/x"><button>x</button></a>{% endcomment %}'),
        (False),
        id="a commented out block",
    ),
    pytest.param(
        ('<a href="/x">{# djlint:off #}<button>x</button>{# djlint:on #}</a>'),
        (False),
        id="an ignored region",
    ),
    pytest.param(
        (
            "{%- comment -%}"
            '<a href="/x"><button>x</button></a>'
            "{%- endcomment -%}"
        ),
        (False),
        id="a comment block written with whitespace control",
    ),
    pytest.param(
        ('<a class="btn" {# href #}><button type="button">Go</button></a>'),
        (False),
        id="an href inside a comment is not one",
    ),
    pytest.param(
        (
            '<a class="card" {% if not href %}aria-disabled="true"{% endif %}>'
            '<button type="button">Go</button></a>'
        ),
        (False),
        id="an href a condition names is not one",
    ),
    pytest.param(
        ("<a data-url={{ href }}><button>x</button></a>"),
        (False),
        id="an href written as another attribute's value is not one",
    ),
    pytest.param(
        ("<a data-attr=href><button>x</button></a>"),
        (False),
        id="an unquoted value of href is not an href",
    ),
    pytest.param(
        ('<a {% if x %}href="/y"{% endif %}><button>x</button></a>'),
        (True),
        id="an href an if writes between its tags is one",
    ),
    pytest.param(
        ('<a href="/x"><input {# type="hidden" was removed #} name="q"></a>'),
        (True),
        id="a type inside a comment is not the type",
    ),
    pytest.param(
        ('<a href="/x"><input name="q" {# type="hidden" #}></a>'),
        (True),
        id="a type commented out after the attributes is not the type",
    ),
    pytest.param(
        ('<a href="/x">go<template><button>x</button></template></a>'),
        (False),
        id="a template's content is not rendered where it is written",
    ),
    pytest.param(
        ('<template><a href="/x"><button>x</button></a></template>'),
        (True),
        id="nesting written inside a template is still nesting",
    ),
    pytest.param(
        (
            '<a href="/x">\n<pre>\n</a>\n</pre>\n<button type="button">y</button>'
        ),
        (False),
        id="a closing tag in a pre body closes the element it names",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h054(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H054" in codes) is reported


def test_h054_reports_the_inner_tag() -> None:
    filename = "test.html"
    config = Config(filename, profile="django")
    source = '<a href="/x">\n  <button>Go</button>\n</a>'

    findings = linter(config, source, filename, filename)[filename]
    reported = [
        (error["line"], error["match"])
        for error in findings
        if error["code"] == "H054"
    ]

    assert reported == [("2:2", "<button>")]


profile_test_data = [
    pytest.param(
        ("liquid"),
        (
            "{%- comment -%}"
            '<a href="/x"><button>x</button></a>'
            "{%- endcomment -%}"
        ),
        (False),
        id="a liquid comment block with whitespace control",
    ),
    pytest.param(
        ("liquid"),
        (
            "{%- comment -%}\n"
            "  Old CTA, replaced:\n"
            '  <a href="{{ product.url }}">'
            "<button>Add to cart</button></a>\n"
            "{%- endcomment -%}\n"
            '<a href="{{ product.url }}" class="button">Add to cart</a>'
        ),
        (False),
        id="a shopify snippet with the old markup commented out",
    ),
    pytest.param(
        ("jinja"),
        ('<a class="btn" {# href="{{ url }}" #}><button>Go</button></a>'),
        (False),
        id="an href commented out inline",
    ),
    pytest.param(
        ("jinja"),
        (
            '<a class="card" {% if not href %}aria-disabled="true"{% endif %}>'
            '<button type="button">Go</button></a>'
        ),
        (False),
        id="a macro parameter called href",
    ),
    pytest.param(
        ("golang"),
        (
            '<a class="btn" {{/* href comes later */}}>'
            '<button type="button">Go</button></a>'
        ),
        (False),
        id="an href inside a golang comment",
    ),
    pytest.param(
        ("handlebars"),
        (
            '<a class="btn" {{!-- href --}}>'
            '<button type="button">Go</button></a>'
        ),
        (False),
        id="an href inside a handlebars comment",
    ),
    pytest.param(
        ("golang"),
        ('<a href="/x"><input {{/* type="hidden" */}} name="q"></a>'),
        (True),
        id="a type inside a golang comment is not the type",
    ),
    pytest.param(
        ("handlebars"),
        ('<a href="/x"><input {{!-- type="hidden" --}} name="q">'),
        (True),
        id="a type inside a handlebars comment is not the type",
    ),
]


@pytest.mark.parametrize(("profile", "source", "reported"), profile_test_data)
def test_h054_in_other_profiles(
    profile: str, source: str, reported: bool
) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H054" in codes) is reported


def test_h054_reads_unmatched_closing_tags_in_one_pass() -> None:
    """Closing tags that match nothing cost the same at any depth.

    Walking the open elements for each of them turned a file of them
    into quadratic work: this took four seconds before the name of the
    tag was looked up instead.
    """
    filename = "test.html"
    config = Config(filename, profile="django")
    source = "<li>" * 15000 + "</ul>" * 15000
    rule = {
        "name": "H054",
        "message": "Interactive element should not be nested inside another.",
    }

    start = time.perf_counter()
    findings = H054.run(rule, config, source, filename, [])

    assert findings == ()
    assert time.perf_counter() - start < 2
