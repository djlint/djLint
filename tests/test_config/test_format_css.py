"""Test for format css.

--format-css
--indent-css

poetry run pytest tests/test_config/test_format_css.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("<div><style>body{color:red}</style></div>"),
        (
            "<div>\n"
            "    <style>\n"
            "        body {\n"
            "            color: red\n"
            "        }\n"
            "    </style>\n"
            "</div>\n"
        ),
        ({"format_css": True}),
        id="enabled",
    ),
    pytest.param(
        ("<div><style>body{color:red}</style></div>"),
        (
            "<div>\n"
            "    <style>\n"
            "     body {\n"
            "      color: red\n"
            "     }\n"
            "    </style>\n"
            "</div>\n"
        ),
        ({"format_css": True, "indent_css": 1}),
        id="enabled_with_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            "    <script>\n"
            "          __jsnlog_configure = function(JL) {\n"
            "               JL.setOptions({\n"
            '                    "defaultAjaxUrl": "/analytics/trace"\n'
            "             })\n"
            "        };\n"
            "        try {\n"
            "              __jsnlog_configure(JL);\n"
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
            "          __jsnlog_configure = function(JL) {\n"
            "               JL.setOptions({\n"
            '                    "defaultAjaxUrl": "/analytics/trace"\n'
            "             })\n"
            "        };\n"
            "        try {\n"
            "              __jsnlog_configure(JL);\n"
            "        } catch (e) {};\n"
            "    </script>\n"
            "</div>\n"
            "<style>\n"
            "    .body {\n"
            "        width: 12px\n"
            "    }\n"
            "</style>\n"
            "<script src=\"{% static '/js/shared.min.js' %}\"></script>\n"
            "<script src=\"{% static '/js/alive.min.js' %}\"></script>\n"
            "<script src=\"{% static '/js/search.min.js' %}\" defer async></script>\n"
            "<script src=\"{% static '/js/utility.min.js' %}\" defer async></script>\n"
        ),
        ({"format_css": True}),
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
        ({"format_css": True}),
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
        ({"format_css": True}),
        id="ignore",
    ),
    pytest.param(
        (
            "<!-- djlint:off -->\n"
            "  <style> body{color:{{ search_index }};}</style><div></div>\n"
            "  <!-- djlint:on -->"
        ),
        (
            "<!-- djlint:off -->\n"
            "  <style> body{color:{{ search_index }};}</style><div></div>\n"
            "<!-- djlint:on -->\n"
        ),
        ({"format_js": True}),
        id="ignored blocks",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
