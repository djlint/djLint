"""Test the attribute values the formatter rewrites.

uv run pytest tests/test_html/test_attribute_values.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

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
