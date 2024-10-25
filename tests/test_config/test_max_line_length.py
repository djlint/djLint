"""Test for max line length.

--max-line-length 4

uv run pytest tests/test_config/test_max_line_length.py
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
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            "<div required\n"
            "     long\n"
            "     attributenamesarereallycool\n"
            '     class="asdf"\n'
            '     data-attr="asdf"\n'
            '     id="asdf">\n'
            "</div>\n"
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        ({"max_line_length": 1}),
        id="short lines",
    ),
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            "<div required\n"
            "     long\n"
            "     attributenamesarereallycool\n"
            '     class="asdf"\n'
            '     data-attr="asdf"\n'
            '     id="asdf"></div>\n'
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        ({"max_line_length": 1000}),
        id="longer lines",
    ),
    pytest.param(
        ("<div></div>\n"),
        ("<div></div>\n"),
        ({"max_line_length": 12}),
        id="twelve",
    ),
    pytest.param(
        ("<div></div>\n"),
        ("<div>\n</div>\n"),
        ({"max_line_length": 11}),
        id="eleven",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
