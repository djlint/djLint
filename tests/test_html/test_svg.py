"""Test svg.

uv run pytest tests/test_html/test_svg.py
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
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <head>\n"
            "    <title>SVG</title>\n"
            "  </head>\n"
            "  <body>\n"
            '    <svg width="100" height="100">\n'
            '      <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />\n'
            "    </svg>\n"
            "  </body>\n"
            "</html>\n"
            '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            "<defs /> <style >\n"
            "    polygon { fill: black }\n"
            "    div {\n"
            "  color: white;\n"
            "      font:18px serif;\n"
            "      height: 100%;\n"
            "      overflow: auto;\n"
            "    }\n"
            "  </style>\n"
            " <g>\n"
            '  <g><polygon points="5,5 195,10 185,185 10,195" />\n'
            "      <text>    Text</text></g>\n"
            "  </g>\n"
            "  <!-- Common use case: embed HTML text into SVG -->\n"
            '  <foreignObject x="20" y="20" width="160" height="160">\n'
            "    <!--\n"
            "      In the context of SVG embedded into HTML, the XHTML namespace could be avoided, but it is mandatory in the context of an SVG document\n"
            "    -->\n"
            '    <div xmlns="http://www.w3.org/1999/xhtml">\n'
            "    <p>\n"
            "  123\n"
            "      </p>\n"
            "      <span>\n"
            "        123\n"
            "        </span>\n"
            "    </div>\n"
            "  </foreignObject>\n"
            "</svg>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <head>\n"
            "        <title>SVG</title>\n"
            "    </head>\n"
            "    <body>\n"
            '        <svg width="100" height="100">\n'
            '            <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />\n'
            "        </svg>\n"
            "    </body>\n"
            "</html>\n"
            '<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n'
            "    <defs /> <style>\n"
            "    polygon { fill: black }\n"
            "    div {\n"
            "  color: white;\n"
            "      font:18px serif;\n"
            "      height: 100%;\n"
            "      overflow: auto;\n"
            "    }\n"
            "    </style>\n"
            "    <g>\n"
            "    <g>\n"
            '    <polygon points="5,5 195,10 185,185 10,195" />\n'
            "    <text>    Text</text>\n"
            "    </g>\n"
            "    </g>\n"
            "    <!-- Common use case: embed HTML text into SVG -->\n"
            '    <foreignObject x="20" y="20" width="160" height="160">\n'
            "    <!--\n"
            "      In the context of SVG embedded into HTML, the XHTML namespace could be avoided, but it is mandatory in the context of an SVG document\n"
            "    -->\n"
            '    <div xmlns="http://www.w3.org/1999/xhtml">\n'
            "        <p>123</p>\n"
            "        <span>123</span>\n"
            "    </div>\n"
            "    </foreignObject>\n"
            "</svg>\n"
        ),
        id="svg",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
