"""Test for format js.

--format-js
--indent-js

uv run pytest tests/test_config/test_format_js.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        ('<div><script>console.log("hi");</script></div>'),
        (
            "<div>\n"
            "    <script>\n"
            '        console.log("hi");\n'
            "    </script>\n"
            "</div>\n"
        ),
        ({"format_js": True}),
        id="enabled",
    ),
    pytest.param(
        ('<div><script>() => {console.log("hi")}</script></div>'),
        (
            "<div>\n"
            "    <script>\n"
            "     () => {\n"
            '      console.log("hi")\n'
            "     }\n"
            "    </script>\n"
            "</div>\n"
        ),
        ({"format_js": True, "indent_js": 1}),
        id="enabled_with_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            "    <script>\n"
            "        __jsnlog_configure = function(JL) {\n"
            "             JL.setOptions({\n"
            '                  "defaultAjaxUrl": "/analytics/trace"\n'
            "             })\n"
            "        };\n"
            "        try {\n"
            "             __jsnlog_configure(JL);\n"
            "        } catch (e) {};\n"
            "    </script>\n"
            "</div>\n"
            "<style>.body {width: 12px}\n"
            "</style>\n"
            "<script src=\"{% static '/js/shared.min.js' %}\"></script>\n"
            "<script src=\"{% static '/js/alive.min.js' %}\"></script>\n"
            "<script src=\"{% static '/js/search.min.js' %}\" defer async></script>\n"
            "<script src=\"{% static '/js/utility.min.js' %}\" defer async></script>"
        ),
        (
            "<div>\n"
            "    <script>\n"
            "        __jsnlog_configure = function(JL) {\n"
            "            JL.setOptions({\n"
            '                "defaultAjaxUrl": "/analytics/trace"\n'
            "            })\n"
            "        };\n"
            "        try {\n"
            "            __jsnlog_configure(JL);\n"
            "        } catch (e) {};\n"
            "    </script>\n"
            "</div>\n"
            "<style>.body {width: 12px}</style>\n"
            "<script src=\"{% static '/js/shared.min.js' %}\"></script>\n"
            "<script src=\"{% static '/js/alive.min.js' %}\"></script>\n"
            "<script src=\"{% static '/js/search.min.js' %}\" defer async></script>\n"
            "<script src=\"{% static '/js/utility.min.js' %}\" defer async></script>\n"
        ),
        ({"format_js": True}),
        id="enabled_block_one",
    ),
    pytest.param(
        (
            "<html>\n"
            "    <head>\n"
            "        <style>\n"
            "            body {}\n"
            "\n"
            "            div {}\n"
            "        </style>\n"
            "    </head>\n"
            "    <script>\n"
            "        let a;\n"
            "\n"
            "        let b;\n"
            "    </script>\n"
            "</html>"
        ),
        (
            "<html>\n"
            "    <head>\n"
            "        <style>\n"
            "            body {}\n"
            "\n"
            "            div {}\n"
            "        </style>\n"
            "    </head>\n"
            "    <script>\n"
            "        let a;\n"
            "\n"
            "        let b;\n"
            "    </script>\n"
            "</html>\n"
        ),
        ({"format_js": True}),
        id="blank lines",
    ),
    pytest.param(
        (
            "<script>\n"
            "    /* beautify preserve:start */\n"
            "function(){}\n"
            "    function(){}\n"
            "        function(){}\n"
            "\n"
            "    /* beautify preserve:end */\n"
            "</script>\n"
            "<script>\n"
            "    /* beautify ignore:start */\n"
            "function(){}\n"
            "    function(){}\n"
            "        function(){}\n"
            "\n"
            "    /* beautify ignore:end */\n"
            "</script>\n"
            "<style>\n"
            "    /* beautify ignore:start */\n"
            "                            .class {display: none;}\n"
            "    /* beautify ignore:end */\n"
            "</style>"
        ),
        (
            "<script>\n"
            "    /* beautify preserve:start */\n"
            "function(){}\n"
            "    function(){}\n"
            "        function(){}\n"
            "\n"
            "    /* beautify preserve:end */\n"
            "</script>\n"
            "<script>\n"
            "    /* beautify ignore:start */\n"
            "function(){}\n"
            "    function(){}\n"
            "        function(){}\n"
            "\n"
            "    /* beautify ignore:end */\n"
            "</script>\n"
            "<style>\n"
            "    /* beautify ignore:start */\n"
            "                            .class {display: none;}\n"
            "    /* beautify ignore:end */\n"
            "</style>\n"
        ),
        ({"format_js": True}),
        id="ignore",
    ),
    pytest.param(
        (
            '<script type="text/javascript">\n'
            "    let s = `\n"
            "        <p>Text.</p>`;\n"
            "</script>\n"
            "<div>"
            '<script type="text/javascript">\n'
            "    let s = `\n"
            "        <p>Text.\n"
            "      </p>`;\n"
            "</script></div>"
        ),
        (
            '<script type="text/javascript">\n'
            "   let s = `\n"
            "        <p>Text.</p>`;\n"
            "</script>\n"
            "<div>\n"
            '    <script type="text/javascript">\n'
            "       let s = `\n"
            "        <p>Text.\n"
            "      </p>`;\n"
            "    </script>\n"
            "</div>\n"
        ),
        ({"format_js": True, "indent_js": 3}),
        id="literals",
    ),
    pytest.param(
        (
            "<!-- djlint:off -->\n"
            '  <script id="search-index" type="application/json">{{ search_index }}</script><div></div>\n'
            "  <!-- djlint:on -->"
        ),
        (
            "<!-- djlint:off -->\n"
            '  <script id="search-index" type="application/json">{{ search_index }}</script><div></div>\n'
            "<!-- djlint:on -->\n"
        ),
        ({"format_js": True}),
        id="ignored blocks",
    ),
    pytest.param(
        (
            "<script>\n"
            "{# djlint:off #}\n"
            "function test() {\n"
            "    var x = 1;\n"
            "        var y = 2;\n"
            "}\n"
            "{# djlint:on #}\n"
            "function other() {\n"
            "    var a = 1;\n"
            "    var b = 2;\n"
            "}\n"
            "</script>"
        ),
        (
            "<script>\n"
            "    {# djlint:off #}\n"
            "function test() {\n"
            "    var x = 1;\n"
            "        var y = 2;\n"
            "}\n"
            "{# djlint:on #}\n"
            "    function other() {\n"
            "        var a = 1;\n"
            "        var b = 2;\n"
            "    }\n"
            "</script>\n"
        ),
        ({"format_js": True, "profile": "django"}),
        id="djlint:off inside script",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
