"""Test jinja calls written over several lines.

uv run pytest tests/test_jinja/test_multiline_call.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "<div>\n  {{ function(\n    argument='value',\n  ) }}\n</div>\n",
        "<div>\n  {{ function(\n    argument='value',\n  ) }}\n</div>\n",
        id="closing_bracket_keeps_the_indent_of_its_tag",
    ),
    pytest.param(
        "<div>\n"
        "  {{ function([\n"
        "    nested(\n"
        "      argument='value',\n"
        "    ),\n"
        "  ]) }}\n"
        "</div>\n",
        "<div>\n"
        "  {{ function([\n"
        "    nested(\n"
        "      argument='value',\n"
        "    ),\n"
        "  ]) }}\n"
        "</div>\n",
        id="nested_arguments_keep_their_depth",
    ),
    pytest.param(
        "{{ function(\n  argument='value',\n) }}\n",
        "{{ function(\n  argument='value',\n) }}\n",
        id="closing_bracket_at_column_zero",
    ),
    pytest.param(
        "<div>\n  {{ function(\n    a) }}\n</div>\n",
        "<div>\n  {{ function(\n    a) }}\n</div>\n",
        id="closing_bracket_on_the_argument_line",
    ),
    pytest.param(
        "<div>{{ function(a, b) }}</div>\n",
        "<div>{{ function(a, b) }}</div>\n",
        id="a_call_on_one_line_is_left_alone",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_multiline_call(source: str, expected: str) -> None:
    config = config_builder({
        "profile": "jinja",
        "indent": 2,
        "quote_style": "single",
    })

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
