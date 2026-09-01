"""Formatting a file twice must give the same result as formatting it once.

uv run pytest tests/test_idempotency.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

templates = [
    pytest.param(
        "{% if x %}\n    {#\n        line\n    #}\n{% endif %}\n",
        id="multiline template comment",
    ),
    pytest.param(
        "<div>\n    {% set p = {\n        a: 1\n    } %}\n</div>\n",
        id="multiline set block",
    ),
    pytest.param(
        '<svg viewBox="0 0 24 24">\n    <path d="\n    {% block p %}\n'
        '    {% endblock p %}\n    " />\n</svg>\n',
        id="template tag inside an attribute value",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "    <head></head>\n"
            "    <body>\n"
            "        <script>\n"
            "            function foo() {\n"
            "                return \\`\n"
            "                    <div>\n"
            "                        <p>Text</p>\n"
            "                    </div>\n"
            "                \\`;\n"
            "            }\n"
            "        </script>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="script with an escaped backtick",
    ),
    pytest.param(
        "<style>\n    .a {\n        color: red;\n    }\n\n</style>\n",
        id="style with a trailing blank line",
    ),
    pytest.param(
        '<a href = "http://example.test/'
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa">T</a>\n',
        id="long attribute with space around equals",
    ),
    pytest.param(
        "<pre>\n  keep   this\n</pre>\n<textarea>\n  and this\n</textarea>\n",
        id="verbatim blocks",
    ),
    pytest.param(
        "{% for x in y %}\n    <li>{{ x }}</li>\n{% endfor %}\n",
        id="template block with html",
    ),
    pytest.param(
        '<div class="a  b"\n     id="c">\n    text\n</div>\n',
        id="multiline attributes",
    ),
    pytest.param(
        "<!-- djlint:off -->\n   left   alone\n<!-- djlint:on -->\n<div>x</div>\n",
        id="djlint off block",
    ),
    pytest.param(
        "{{ with .U }}\n{{ if .A }}\n<p>a</p>\n{{ end }}\n{{ end }}\n",
        id="golang block tags",
    ),
    pytest.param(
        "{% set hero %}{% block h %}{% endblock %}{% endset %}\n",
        id="single line set block",
    ),
    pytest.param(
        "{{ function(\n    a=1,\n    b=2,\n) }}\n",
        id="call arguments on their own lines",
    ),
    pytest.param(
        "<p>\n    {% language 'de' %}text{% endlanguage %}\n    <span>x</span>\n</p>\n",
        id="single line template block among siblings",
    ),
    pytest.param(
        "<script>-</script>v\n", id="text right after a script element"
    ),
    pytest.param(
        '<div><p>a</p><script>var a = "{% x %}"</script><p>b</p></div>\n',
        id="template delimiters inside javascript",
    ),
    pytest.param(
        '<input id="ab"  type="cdef">\n', id="extra space between attributes"
    ),
    pytest.param(
        '<li><code>{%-</code></li>\n<h2 id="a" tabindex="-1" class="title is-2">x</h2>\n<li><code>-%}</code></li>\n',
        id="template delimiter written as prose",
    ),
    pytest.param(
        '<td>{% x }%?</td>\n<h2 id="a" tabindex="-1" class="title is-2">x</h2>\n<p><code>{% tag %}</code></p>\n',
        id="unclosed template tag before a heading",
    ),
]

option_sets = [
    pytest.param({}, id="defaults"),
    pytest.param({"preserve_leading_space": True}, id="preserve-leading-space"),
    pytest.param({"preserve_blank_lines": True}, id="preserve-blank-lines"),
    pytest.param(
        {"single_attribute_per_line": True}, id="single-attribute-per-line"
    ),
    pytest.param({"format_css": True, "format_js": True}, id="format-css-js"),
    pytest.param(
        {"blank_line_after_tag": "load", "blank_line_before_tag": "block"},
        id="blank-line-tags",
    ),
    pytest.param({"max_attribute_length": 20}, id="max-attribute-length"),
    pytest.param({"indent": 2}, id="indent-2"),
    pytest.param(
        {"profile": "golang", "preserve_leading_space": True},
        id="golang-preserve-leading-space",
    ),
]


@pytest.mark.parametrize("args", option_sets)
@pytest.mark.parametrize("source", templates)
def test_formatting_is_a_fixed_point(source: str, args: dict[str, Any]) -> None:
    config = config_builder(args)
    once = formatter(config, source)
    twice = formatter(config, once)

    printer(once, source, twice)
    assert once == twice
