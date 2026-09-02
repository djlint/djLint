"""Test case.

uv run pytest tests/test_html/test_case.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from djlint.settings import Config
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


test_data_attributes = [
    pytest.param(
        ('<div CLASS="a" ID="b"></div>\n'),
        ('<div class="a" id="b"></div>\n'),
        id="known_attribute_names",
    ),
    pytest.param(
        ('<path D="M0" [ngModel]="x" Charset="y" />\n'),
        ('<path D="M0" [ngModel]="x" Charset="y" />\n'),
        id="a name H010 does not know keeps the case it carries",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data_attributes)
def test_attribute_case(
    source: str, expected: str, basic_config: Config
) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


test_data_two = [
    pytest.param(
        ("<dIV></Div>\n<bR>\n<Br />\n<MeTa class='asdf' />\n"),
        ('<dIV></Div>\n<bR>\n<Br />\n<MeTa class="asdf" />\n'),
        id="preserve_case",
    ),
    pytest.param(
        ('<div CLASS="a" ID="b" viewBox="0 0"></div>\n'),
        ('<div CLASS="a" ID="b" viewBox="0 0"></div>\n'),
        id="preserve_attribute_case",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data_two)
def test_base_two(source: str, expected: str) -> None:
    config = Config("dummy/source.html", ignore_case=True)
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
