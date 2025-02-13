"""Test handlebars each tag.

uv run pytest tests/test_handlebars/test_each.py
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
        (
            "<html lang='en'>    <head>        <meta charset='UTF-8' />        <meta name='viewport' content='width=device-width, initial-scale=1' />        <title></title>        <link href='css/style.css' rel='stylesheet' />    </head>    <body>        {{#unless}}        <div>            <p></p>        </div>    {{/unless}}</body></html>"
        ),
        (
            "<html lang='en'>\n"
            "    <head>\n"
            "        <meta charset='UTF-8' />\n"
            "        <meta name='viewport' content='width=device-width, initial-scale=1' />\n"
            "        <title></title>\n"
            "        <link href='css/style.css' rel='stylesheet' />\n"
            "    </head>\n"
            "    <body>\n"
            "        {{#unless}}\n"
            "            <div>\n"
            "                <p></p>\n"
            "            </div>\n"
            "        {{/unless}}\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="unless_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, handlebars_config: Config) -> None:
    output = formatter(handlebars_config, source)

    printer(expected, source, output)
    assert expected == output
