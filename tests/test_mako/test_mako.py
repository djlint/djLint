"""Test that the mako profile keeps Mako's line syntax working.

uv run pytest tests/test_mako/test_mako.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from djlint.src import has_pragma
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing import Any

test_data = [
    pytest.param(
        (
            "<main>\n"
            '    <section class="container"\n'
            "    % if getattr(course, 'language'):\n"
            "      lang=${course.language}\n"
            "    % endif\n"
            "    >\n"
            '      <div class="wrapper">${HTML(body)}</div>\n'
            "    </section>\n"
            "</main>\n"
        ),
        (
            "<main>\n"
            '    <section class="container"\n'
            "    % if getattr(course, 'language'):\n"
            "      lang=${course.language}\n"
            "    % endif\n"
            "    >\n"
            '        <div class="wrapper">${HTML(body)}</div>\n'
            "    </section>\n"
            "</main>\n"
        ),
        ({}),
        id="control lines in a tag keep the attributes they decide as written",
    ),
    pytest.param(
        (
            "<script \\\n"
            "% if defer:\n"
            "defer \\\n"
            "% endif\n"
            'type="text/javascript" charset="utf-8">\n'
            "    ${source | n}\n"
            "</script>\n"
        ),
        (
            "<script \\\n"
            "% if defer:\n"
            "defer \\\n"
            "% endif\n"
            'type="text/javascript" charset="utf-8">${source | n}</script>\n'
        ),
        ({}),
        id="a default type inside a tag with control lines is not dropped",
    ),
    pytest.param(
        ("<div\n% if a > b:\nclass='big'\n% endif\n>x</div>\n"),
        ("<div\n% if a > b:\nclass='big'\n% endif\n>x</div>\n"),
        ({}),
        id="a > in a condition does not end the tag",
    ),
    pytest.param(
        ("<p>\n% if user:\nHello\n% endif\n</p>\n"),
        ("<p>\n    % if user:\n    Hello\n    % endif\n</p>\n"),
        ({}),
        id="control lines keep a line each in a short element",
    ),
    pytest.param(
        ("<ul>\n% for item in items:\n<li>${item}</li>\n% endfor\n</ul>\n"),
        ("<ul>\n    % for item in items:\n    <li>${item}</li>\n    % endfor\n</ul>\n"),
        ({}),
        id="a loop",
    ),
    pytest.param(
        ("<div><span>a</span>\n## a comment <b>\n<span>b</span></div>\n"),
        ("<div>\n    <span>a</span>\n    ## a comment <b>\n    <span>b</span>\n</div>\n"),
        ({}),
        id="a comment keeps its line and its markup is not read",
    ),
    pytest.param(
        ("<%doc>\n  <b>keep</b>   this\n</%doc>\n<div><p>x</p></div>\n"),
        ("<%doc>\n  <b>keep</b>   this\n</%doc>\n<div>\n    <p>x</p>\n</div>\n"),
        ({}),
        id="a doc block is left as written",
    ),
    pytest.param(
        ("<pre>\n<%text>\n  ${not_evaluated}   <b>x</b>\n</%text>\n</pre>\n"),
        ("<pre>\n<%text>\n  ${not_evaluated}   <b>x</b>\n</%text>\n</pre>\n"),
        ({}),
        id="a text block is left as written",
    ),
    pytest.param(
        ("## djlint:off\n<div><p>x</p>\n   </div>\n## djlint:on\n<div><p>y</p></div>\n"),
        ("## djlint:off\n<div><p>x</p>\n   </div>\n## djlint:on\n<div>\n    <p>y</p>\n</div>\n"),
        ({}),
        id="a djlint:off region",
    ),
    pytest.param(
        ("<p>\n%% of the vote\n</p>\n"),
        ("<p>%% of the vote</p>\n"),
        ({}),
        id="an escaped percent sign is text",
    ),
    pytest.param(
        (
            "<script>\n"
            "var a = ${json};\n"
            "<%block name='extra'></%block>\n"
            "</script>\n"
            "<script>var b=1;</script>\n"
        ),
        (
            "<script>\n"
            "var a = ${json};\n"
            "<%block name='extra'></%block>\n"
            "</script>\n"
            "<script>\n"
            "    var b = 1;\n"
            "</script>\n"
        ),
        ({"format_js": True}),
        id="a script holding Mako syntax is not beautified",
    ),
    pytest.param(
        ("<script>\n% if a:\nvar a=1;\n% endif\n</script>\n"),
        ("<script>\n% if a:\nvar a=1;\n% endif\n</script>\n"),
        ({"format_js": True}),
        id="a script holding control lines is not beautified",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    config = config_builder({"profile": "mako", **args})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
    assert formatter(config, output) == output


@pytest.mark.parametrize(
    "first_line",
    [
        pytest.param("## djlint:on\n", id="a comment"),
        pytest.param("<%doc>djlint:on</%doc>\n", id="a doc block"),
        pytest.param("<!-- djlint:on -->\n", id="an html comment"),
    ],
)
def test_pragma(first_line: str) -> None:
    assert has_pragma(config_builder({"profile": "mako"}), first_line)
