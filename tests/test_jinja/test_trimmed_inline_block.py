"""Test elements following a whitespace-trimmed inline jinja block.

uv run pytest tests/test_jinja/test_trimmed_inline_block.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "<li>\n"
        "  {% if value %}\n"
        "    <b>Line {{ first }}\n"
        "      {%- if last != first %} to {{ last }}\n"
        "      {%- endif %}:</b>\n"
        "    <pre>Content</pre>\n"
        "  {% endif %}\n"
        "</li>\n",
        "<li>\n"
        "  {% if value %}\n"
        "    <b>Line {{ first }}\n"
        "      {%- if last != first %} to {{ last }}\n"
        "      {%- endif %}:</b>\n"
        "    <pre>Content</pre>\n"
        "  {% endif %}\n"
        "</li>\n",
        id="element_after_a_closed_block_and_tag_keeps_its_level",
    ),
    pytest.param(
        "<div>\n  {% if r %}</strong>{% endif %}\n  <p>after</p>\n</div>\n",
        "<div>\n  {% if r %}</strong>{% endif %}\n  <p>after</p>\n</div>\n",
        id="a_close_whose_open_took_no_level_still_takes_none_back",
    ),
    pytest.param(
        "<div>\n  <b>x</b>\n  <p>y</p>\n</div>\n",
        "<div>\n  <b>x</b>\n  <p>y</p>\n</div>\n",
        id="a_plain_nested_close_is_unaffected",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_trimmed_inline_block(source: str, expected: str) -> None:
    config = config_builder({
        "profile": "jinja",
        "indent": 2,
        "quote_style": "single",
    })

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
