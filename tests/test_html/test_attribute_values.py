"""Test the attribute values the formatter rewrites.

uv run pytest tests/test_html/test_attribute_values.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint._reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint._settings import Config

test_data = [
    pytest.param(
        '<form method="POST" action="/"></form>\n',
        '<form method="post" action="/">\n</form>\n',
        id="form method is lowercased",
    ),
    pytest.param(
        (
            '<script type="text/javascript"></script>\n'
            '<style type="text/css"></style>\n'
            '<link type="text/css" rel="stylesheet" href="a.css">\n'
        ),
        ('<script></script>\n<style></style>\n<link rel="stylesheet" href="a.css">\n'),
        id="default types are dropped",
    ),
    pytest.param(
        (
            "<script type=text/javascript></script>\n"
            '<style type = "text/css"></style>\n'
            "<link TYPE=TEXT/CSS rel=stylesheet href=a.css>\n"
        ),
        ('<script></script>\n<style></style>\n<link rel="stylesheet" href="a.css">\n'),
        id="default types are dropped unquoted or spaced",
    ),
    pytest.param(
        "<form method=POST></form>\n<form action=/a method = 'GET'></form>\n",
        '<form method="post">\n</form>\n<form action="/a" method=\'get\'>\n</form>\n',
        id="form method is lowercased unquoted or spaced",
    ),
    pytest.param(
        "<script type=text/javascript{{ v }}></script>\n<form method=POST{{ v }}></form>\n",
        '<script type="text/javascript{{ v }}"></script>\n<form method="POST{{ v }}">\n</form>\n',
        id="an unquoted value glued to a template tag is left alone",
    ),
    pytest.param(
        '<script type="module"></script>\n',
        '<script type="module"></script>\n',
        id="a type that means something is kept",
    ),
    pytest.param(
        '<script-x type="text/javascript"></script-x>\n',
        '<script-x type="text/javascript">\n</script-x>\n',
        id="a custom element named like script keeps its type",
    ),
    pytest.param(
        '<style-x type="text/css"></style-x>\n',
        '<style-x type="text/css">\n</style-x>\n',
        id="a custom element named like style keeps its type",
    ),
    pytest.param(
        '<link-x type="text/css" rel="stylesheet">\n',
        '<link-x type="text/css" rel="stylesheet">\n',
        id="a custom element named like link keeps its type",
    ),
    pytest.param(
        '<form-x method="POST"></form-x>\n',
        '<form-x method="POST">\n</form-x>\n',
        id="a custom element named like form keeps its method",
    ),
    pytest.param(
        (
            '<style type="text/javascript"></style>\n'
            "<script type=text/css></script>\n"
            '<link type="text/javascript" rel="stylesheet" href="a.js">\n'
            '<link type="text/css" rel="icon" href="a.css">\n'
            '<link type="text/css" rel="stylesheets" href="a.css">\n'
        ),
        (
            '<style type="text/javascript"></style>\n'
            '<script type="text/css"></script>\n'
            '<link type="text/javascript" rel="stylesheet" href="a.js">\n'
            '<link type="text/css" rel="icon" href="a.css">\n'
            '<link type="text/css" rel="stylesheets" href="a.css">\n'
        ),
        id="a type is dropped only where it is the element's default",
    ),
    pytest.param(
        (
            '<link rel="alternate stylesheet" type="text/css" href="a.css">\n'
            "<link type=text/css href=b.css rel=stylesheet>\n"
        ),
        ('<link rel="alternate stylesheet" href="a.css">\n<link href="b.css" rel="stylesheet">\n'),
        id="a stylesheet link drops text/css wherever its rel is written",
    ),
    pytest.param(
        (
            '<link {% if x %} rel="stylesheet"{% endif %} type="text/css">\n'
            '<link {{ attrs }} rel="stylesheet" type="text/css">\n'
            '<link rel="stylesheet" {% if x %}rel="icon"{% endif %} type="text/css">\n'
            '<link rel="stylesheet" type="text/css" href="{{ a }}">\n'
        ),
        (
            '<link {% if x %} rel="stylesheet"{% endif %} type="text/css">\n'
            '<link {{ attrs }} rel="stylesheet" type="text/css">\n'
            '<link rel="stylesheet" {% if x %}rel="icon"{% endif %}>\n'
            '<link rel="stylesheet" href="{{ a }}">\n'
        ),
        id="a template tag before the rel may write another one first",
    ),
    pytest.param(
        (
            "<link {# rel=stylesheet #} rel=preload type=text/css>\n"
            '<script {# type="text/javascript" #}></script>\n'
            '<script {# note #} type="text/javascript"></script>\n'
        ),
        (
            '<link {# rel=stylesheet #} rel="preload" type="text/css">\n'
            '<script {# type="text/javascript" #}></script>\n'
            "<script {# note #}></script>\n"
        ),
        id="template tags and comments are read whole",
    ),
    pytest.param(
        (
            "<link {# note\ncontinued #} rel=stylesheet type=text/css href=a.css>\n"
            '<script {% if a\n%}async{% endif %} type="text/javascript"></script>\n'
        ),
        (
            '<link {# note continued #} rel="stylesheet" href="a.css">\n'
            "<script {% if a %}async{% endif %}></script>\n"
        ),
        id="template tags and comments across lines are read whole",
    ),
    pytest.param(
        (
            "<script {{ 'data-note=\"' ~ '}} type=text/javascript x\"' }}></script>\n"
            "<script {% set n = '%} type=text/javascript' %}></script>\n"
        ),
        (
            "<script {{ 'data-note=\"' ~ '}} type=text/javascript x\"' }}></script>\n"
            "<script {% set n = '%} type=text/javascript' %}></script>\n"
        ),
        id="a closer inside a string of a template tag does not end the tag",
    ),
    pytest.param(
        (
            '<script type="text/javascript" type="module"></script>\n'
            '<script {% if a %}type="text/javascript"{% endif %} type="module"></script>\n'
            '<style type="text/css" type="text/x"></style>\n'
            '<link rel="stylesheet" type="text/css" type="text/x">\n'
        ),
        (
            '<script type="text/javascript" type="module"></script>\n'
            '<script {% if a %}type="text/javascript"{% endif %} type="module"></script>\n'
            '<style type="text/css" type="text/x"></style>\n'
            '<link rel="stylesheet" type="text/css" type="text/x">\n'
        ),
        id="a default type followed by another type is kept",
    ),
    pytest.param(
        (
            "<script type=text/javascript {{ attrs|safe }}></script>\n"
            '<style type="text/css" {% attrs %}></style>\n'
            '<link rel="stylesheet" type="text/css" {{ attrs }}>\n'
            '<script type="text/javascript" src="{{ url }}" {# note #}></script>\n'
        ),
        (
            '<script type="text/javascript" {{ attrs|safe }}></script>\n'
            '<style type="text/css" {% attrs %}></style>\n'
            '<link rel="stylesheet" type="text/css" {{ attrs }}>\n'
            '<script src="{{ url }}" {# note #}></script>\n'
        ),
        id="a default type followed by a template tag is kept",
    ),
    pytest.param(
        (
            '<script type="text/javascript" src={{url}}></script>\n'
            '<script type="text/javascript" src={{a}}{{b}}></script>\n'
            '<script type="text/javascript" class=a{{ b }}></script>\n'
            '<script type="text/javascript" src= {{ url }}></script>\n'
            '<script type="text/javascript" src={% if a %}x{% endif %}></script>\n'
        ),
        (
            '<script src="{{url}}"></script>\n'
            '<script src="{{a}}{{b}}"></script>\n'
            '<script class="a{{ b }}"></script>\n'
            '<script src="{{ url }}"></script>\n'
            '<script src="{% if a %}x{% endif %}"></script>\n'
        ),
        id="a template tag in a bare value after the type is part of that value",
    ),
    pytest.param(
        (
            '<script type="text/javascript" data-x="{{ "a > b" }}" {{ attrs|safe }}></script>\n'
            '<script type="text/javascript" data-x="{{ "a type=b" }}"></script>\n'
            '<script type="text/javascript" data-x=\'{{ "it\'s" }}\' {% attrs %}></script>\n'
            '<script type="text/javascript" data-type="x" data-x="type=x" @type="y"></script>\n'
        ),
        (
            '<script type="text/javascript" data-x="{{ "a > b" }}" {{ attrs|safe }}></script>\n'
            '<script data-x="{{ "a type=b" }}"></script>\n'
            '<script type="text/javascript" data-x=\'{{ "it\'s" }}\' {% attrs %}></script>\n'
            '<script data-type="x" data-x="type=x" @type="y"></script>\n'
        ),
        id="a quoted value after the type is read with its template tags whole",
    ),
    pytest.param(
        (
            '<script type="text/javascript" type=text/javascript defer></script>\n'
            "<style TYPE='text/css' type=\"text/css\"></style>\n"
            '<script type="text/javascript" type="text/javascript" type="module"></script>\n'
        ),
        (
            "<script defer></script>\n"
            "<style></style>\n"
            '<script type="text/javascript" type="module"></script>\n'
        ),
        id="a default type followed only by the same default is dropped with it",
    ),
    pytest.param(
        (
            '<link rel="{{ \'icon\' if x else \'stylesheet\' }}" type="text/css" href="a">\n'
            '<link rel=\'{% if x %} stylesheet {% else %} icon {% endif %}\' type="text/css" href="b">\n'
        ),
        (
            '<link rel="{{ \'icon\' if x else \'stylesheet\' }}" type="text/css" href="a">\n'
            "<link rel='{% if x %} stylesheet {% else %} icon {% endif %}'\n"
            '      type="text/css"\n'
            '      href="b">\n'
        ),
        id="a rel a template tag writes may not be a stylesheet",
    ),
    pytest.param(
        (
            '<form {% if a %}data-{% endif -%} method="POST"></form>\n'
            '<form @method="POST" x-on:method="POST"></form>\n'
            '<script @type="text/javascript" :type="text/javascript"></script>\n'
            '<form {% if a %}method="POST"{% endif %}></form>\n'
        ),
        (
            '<form {% if a %}data-{% endif -%} method="POST">\n</form>\n'
            '<form @method="POST" x-on:method="POST">\n</form>\n'
            '<script @type="text/javascript" :type="text/javascript"></script>\n'
            '<form {% if a %}method="post"{% endif %}>\n</form>\n'
        ),
        id="only an attribute of its own is rewritten",
    ),
    pytest.param(
        (
            "<script type=text/javascript {{- s }}></script>\n"
            '<script type="text/javascript" {%- if a %} async{% endif %}></script>\n'
            '<script {{ a -}} type="text/javascript"></script>\n'
            "<form method=POST {{- s }}></form>\n"
            '<form method="POST"{%- if a %} x{% endif %}></form>\n'
            '<script type="text/javascript" {#- c #}></script>\n'
            '<script {# c -#} type="text/javascript"></script>\n'
        ),
        (
            "<script type=text/javascript {{- s }}></script>\n"
            '<script type="text/javascript" {%- if a %} async{% endif %}></script>\n'
            '<script {{ a -}} type="text/javascript"></script>\n'
            "<form method=POST {{- s }}>\n</form>\n"
            '<form method="POST"{%- if a %} x{% endif %}>\n</form>\n'
            '<script type="text/javascript" {#- c #}></script>\n'
            '<script {# c -#} type="text/javascript"></script>\n'
        ),
        id="a value whose space a template tag trims is left alone",
    ),
    pytest.param(
        '<pre><form method="POST"><script type="text/javascript"></pre>\n',
        '<pre><form method="POST"><script type="text/javascript"></pre>\n',
        id="verbatim content is left alone",
    ),
    pytest.param(
        (
            '{% include "a.html" with s=\'<form method="POST">\' %}\n'
            '{% include "b.html" with t=\'<script type="text/javascript">\' %}\n'
        ),
        (
            '{% include "a.html" with s=\'<form method="POST">\' %}\n'
            '{% include "b.html" with t=\'<script type="text/javascript">\' %}\n'
        ),
        id="a tag written inside a template tag is left alone",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
