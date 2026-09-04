"""Test template tags written over several lines inside an attribute.

uv run pytest tests/test_jinja/test_multiline_attribute_tag.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "<div data-x='{{ f({\n  x: y,\n}) }}'></div>\n",
        "<div data-x='{{ f({\n  x: y,\n}) }}'></div>\n",
        id="a_dictionary_keeps_its_indentation",
    ),
    pytest.param(
        "<div data-x='{{ f({\n    x: y,\n}) }}'></div>\n",
        "<div data-x='{{ f({\n    x: y,\n}) }}'></div>\n",
        id="a_deeper_indent_is_kept_as_written",
    ),
    pytest.param(
        "<div data-x='q\n  w\n e'></div>\n",
        "<div data-x='q\n  w\n e'></div>\n",
        id="a_value_holding_no_tag_is_unaffected",
    ),
    pytest.param(
        "<div>{{  a  }}</div>\n",
        "<div>{{ a }}</div>\n",
        id="padding_inside_a_tag_is_still_collapsed",
    ),
    pytest.param(
        "<div>{{ f(a,   b) }}</div>\n",
        "<div>{{ f(a, b) }}</div>\n",
        id="padding_between_arguments_is_still_collapsed",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_multiline_attribute_tag(source: str, expected: str) -> None:
    config = config_builder({
        "profile": "jinja",
        "indent": 2,
        "quote_style": "single",
    })

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
