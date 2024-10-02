"""Test for indent.

--indent 4

uv run pytest tests/test_config/test_indent.py
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
        ("<section><p><div><span></span></div></p></section>"),
        (
            "<section>\n"
            "  <p>\n"
            "    <div>\n"
            "      <span></span>\n"
            "    </div>\n"
            "  </p>\n"
            "</section>\n"
        ),
        ({"indent": 2}),
        id="two",
    ),
    pytest.param(
        ("<section><p><div><span></span></div></p></section>"),
        (
            "<section>\n"
            " <p>\n"
            "  <div>\n"
            "   <span></span>\n"
            "  </div>\n"
            " </p>\n"
            "</section>\n"
        ),
        ({"indent": 1}),
        id="one",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
