"""Test case.

poetry run pytest tests/test_html/test_case.py
"""
import pytest

from src.djlint.reformat import formatter
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
            '<HTML CLASS="no-js mY-ClAsS">\n'
            "    <HEAD>\n"
            '        <META CHARSET="utf-8">\n'
            "        <TITLE>My tITlE</TITLE>\n"
            '        <META NAME="description" content="My CoNtEnT">\n'
            "    </HEAD>\n"
            "    <body>\n"
            "        <P>\n"
            "            Hello world!\n"
            "            <BR>\n"
            "            This is HTML5 Boilerplate.\n"
            "        </P>\n"
            "        <SCRIPT>\n"
            "      window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;\n"
            "      ga('create', 'UA-XXXXX-Y', 'auto'); ga('send', 'pageview')\n"
            "        </SCRIPT>\n"
            '        <SCRIPT src="https://www.google-analytics.com/analytics.js" ASYNC DEFER></SCRIPT>\n'
            "    </body>\n"
            "</HTML>\n"
        ),
        id="case",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
