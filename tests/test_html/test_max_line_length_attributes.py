"""Test that attributes are spread when they are what overruns the line.

uv run pytest tests/test_html/test_max_line_length_attributes.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        '<a href="/x"\n   id="y">Link</a>\n',
        '<a href="/x"\n   id="y">Link</a>\n',
        20,
        id="two_attributes_stay_spread_when_joining_would_overrun",
    ),
    pytest.param(
        '<a href="/x" id="y">Link</a>\n',
        '<a href="/x"\n   id="y">Link</a>\n',
        20,
        id="two_attributes_are_spread_when_the_line_overruns",
    ),
    pytest.param(
        '<a href="/x" id="y">Link</a>\n',
        '<a href="/x" id="y">Link</a>\n',
        120,
        id="a_line_within_the_limit_is_left_alone",
    ),
    pytest.param(
        '<p>Test <span class="value">1</span></p>\n',
        '<p>Test <span class="value">1</span></p>\n',
        1,
        id="one_attribute_cannot_shorten_the_line_and_is_left",
    ),
    pytest.param(
        '<a href="/x" id="y">A very long run of text that no attribute spreading can shorten</a>\n',
        '<a href="/x" id="y">A very long run of text that no attribute spreading can shorten</a>\n',
        20,
        id="a_line_long_from_its_text_is_left_alone",
    ),
]


@pytest.mark.parametrize(("source", "expected", "limit"), test_data)
def test_max_line_length_attributes(
    source: str, expected: str, limit: int
) -> None:
    config = config_builder({
        "profile": "jinja",
        "indent": 2,
        "max_line_length": limit,
    })

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
