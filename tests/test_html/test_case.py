"""Test case.

poetry run pytest tests/test_html/test_case.py
"""
import pytest

from src.djlint.reformat import formatter
from src.djlint.settings import Config
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
            '<html CLASS="no-js mY-ClAsS">\n'
            "    <head>\n"
            '        <meta CHARSET="utf-8">\n'
            "        <title>My tITlE</title>\n"
            '        <meta NAME="description" content="My CoNtEnT">\n'
            "    </head>\n"
            "    <body>\n"
            "        <p>\n"
            "            Hello world!\n"
            "            <br>\n"
            "            This is HTML5 Boilerplate.\n"
            "        </p>\n"
            "        <script>\n"
            "      window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;\n"
            "      ga('create', 'UA-XXXXX-Y', 'auto'); ga('send', 'pageview')\n"
            "        </script>\n"
            '        <script src="https://www.google-analytics.com/analytics.js" ASYNC DEFER> </script>\n'
            "    </body>\n"
            "</html>\n"
        ),
        id="case",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


test_data_two = [
    pytest.param(
        ("<dIV></Div>\n" "<bR>\n" "<Br />\n" "<MeTa class='asdf' />\n"),
        ("<dIV></Div>\n" "<bR>\n" "<Br />\n" "<MeTa class='asdf' />\n"),
        id="preserve_case",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data_two)
def test_base_two(source, expected):
    config = Config("dummy/source.html", ignore_case=True)
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
