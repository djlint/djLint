"""Tests forced line break when a tag has breaks in attributes tag.

uv run pytest tests/test_config/test_line_break_after_multiline_tag.py
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
            '<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">string</div>\n'
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
        ),
        ({}),
        id="no_line_break_after_multiline_tag",
    ),
    pytest.param(
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    string\n"
            "</div>\n"
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
        ),
        ({}),
        id="no_line_break_after_multiline_tag_when_already_split",
    ),
    pytest.param(
        (
            '<div attribute="value" attributea="value" attributeb="value" attributec="value" attributed="value" attributef="value">string</div>\n'
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    string\n"
            "</div>\n"
        ),
        ({"line_break_after_multiline_tag": True}),
        id="line_break_after_multiline_tag",
    ),
    pytest.param(
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">string</div>\n'
        ),
        (
            '<div attribute="value"\n'
            '     attributea="value"\n'
            '     attributeb="value"\n'
            '     attributec="value"\n'
            '     attributed="value"\n'
            '     attributef="value">\n'
            "    string\n"
            "</div>\n"
        ),
        ({"line_break_after_multiline_tag": True}),
        id="line_break_after_multiline_tag_when_already_condensed",
    ),
    pytest.param(
        (
            '<div class="ds-flex ds-items-center ds-justify-center"\n'
            '     style="grid-column: 3/4">\n'
            "    {{ here_is_a_long_variable }}\n"
            "</div>\n"
            '<a class="ds-flex ds-items-center ds-justify-center"\n'
            '   style="grid-column: 3/4">\n'
            "    {{ here_is_a_long_variable }}\n"
            "</a>\n"
            '<span class="ds-flex ds-items-center ds-justify-center"\n'
            '      style="grid-column: 3/4">\n'
            "    {{ here_is_a_long_variable }}\n"
            "</span>\n"
        ),
        (
            '<div class="ds-flex ds-items-center ds-justify-center"\n'
            '     style="grid-column: 3/4">\n'
            "    {{ here_is_a_long_variable }}\n"
            "</div>\n"
            '<a class="ds-flex ds-items-center ds-justify-center"\n'
            '   style="grid-column: 3/4">\n'
            "    {{ here_is_a_long_variable }}\n"
            "</a>\n"
            '<span class="ds-flex ds-items-center ds-justify-center"\n'
            '      style="grid-column: 3/4">\n'
            "    {{ here_is_a_long_variable }}\n"
            "</span>\n"
        ),
        ({"line_break_after_multiline_tag": True}),
        id="more complex tags. #680",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
