"""Test case.

poetry run pytest tests/test_html/test_case.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            '<HTML CLASS="no-js mY-ClAsS">\n'
            "  <HEAD>\n"
            '    <META CHARSET="utf-8">\n'
            "    <TITLE>My tITlE</TITLE>\n"
            '    <META NAME="description" content="My CoNtEnT">\n'
            "  </HEAD>\n"
            "  <body>\n"
            "    <P>Hello world!<BR> This is HTML5 Boilerplate.</P>\n"
            "    <SCRIPT>\n"
            "      window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;\n"
            "      ga('create', 'UA-XXXXX-Y', 'auto'); ga('send', 'pageview')\n"
            "    </SCRIPT>\n"
            '    <SCRIPT src="https://www.google-analytics.com/analytics.js" ASYNC DEFER> </SCRIPT>\n'
            "  </body>\n"
            "</HTML>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            '<html class="no-js mY-ClAsS">\n'
            "    <head>\n"
            '        <meta charset="utf-8" />\n'
            "        <title>My tITlE</title>\n"
            '        <meta name="description" content="My CoNtEnT" />\n'
            "    </head>\n"
            "    <body>\n"
            "        <p>\n"
            "            Hello world!<br />\n"
            "            This is HTML5 Boilerplate.\n"
            "        </p>\n"
            "        <script>\n"
            "            window.ga = function() {\n"
            "                ga.q.push(arguments)\n"
            "            };\n"
            "            ga.q = [];\n"
            "            ga.l = +new Date;\n"
            "            ga('create', 'UA-XXXXX-Y', 'auto');\n"
            "            ga('send', 'pageview')\n"
            "        </script>\n"
            "        <script\n"
            '            src="https://www.google-analytics.com/analytics.js"\n'
            "            async\n"
            "            defer></script>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="case",
    )
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
