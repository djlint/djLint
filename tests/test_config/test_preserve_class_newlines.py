"""Test for preserve_class_newlines.

--preserve-class-newlines

uv run pytest tests/test_config/test_preserve_class_newlines.py
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
            "<a\n"
            '  href="foo"\n'
            '  class="\n'
            "    inline-flex items-center p-4\n"
            "    bg-white hover:bg-gray-200\n"
            "    text-sm font-medium text-gray-500 hover:text-gray-700\n"
            '  ">\n'
            "</a>\n"
        ),
        (
            '<a href="foo"\n'
            '   class="inline-flex items-center p-4\n'
            "          bg-white hover:bg-gray-200\n"
            '          text-sm font-medium text-gray-500 hover:text-gray-700"> </a>\n'
        ),
        ({"preserve_class_newlines": True}),
        id="preserves multiline class groups",
    ),
    pytest.param(
        (
            '<button type="button"\n'
            '        class="\n'
            "          inline-flex items-center\n"
            "          rounded-md px-3 py-2\n"
            '        "\n'
            '        data-state="ready">Save</button>\n'
        ),
        (
            '<button type="button"\n'
            '        class="inline-flex items-center\n'
            '               rounded-md px-3 py-2"\n'
            '        data-state="ready">Save</button>\n'
        ),
        ({"preserve_class_newlines": True}),
        id="preserves class newlines among other attributes",
    ),
    pytest.param(
        ('<my-tag class="\nfoo\nbar\n"></my-tag>'),
        ('<my-tag class="foo\n               bar"></my-tag>\n'),
        ({"preserve_class_newlines": True}),
        id="restores custom tag class newlines",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
