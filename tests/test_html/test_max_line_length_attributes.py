"""Test that attributes are spread when they are what overruns the line.

uv run pytest tests/test_html/test_max_line_length_attributes.py
"""

from __future__ import annotations

import pytest

from djlint._reformat import formatter
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
    pytest.param(
        '<div>\n<div>\n<a href="/x" id="y">\nLink\n</a>\n</div>\n</div>\n',
        '<div>\n  <div>\n    <a href="/x" id="y">\n      Link\n    </a>\n  </div>\n</div>\n',
        30,
        id="content_stays_off_a_line_its_indentation_would_overrun",
    ),
    pytest.param(
        '<p>\nSome <span class="m" id="h">\nx\n</span> tail\n</p>\n',
        '<p>\n  Some <span class="m" id="h">\n  x\n  </span> tail\n</p>\n',
        40,
        id="content_stays_off_a_line_the_text_around_it_would_overrun",
    ),
    pytest.param(
        '<div>\n<div>\n{% block t %}\n<h2 class="m" id="h">\n{{ _(\'L\') }}\n</h2>\n'
        "{% endblock %}\n</div>\n</div>\n",
        '<div>\n  <div>\n    {% block t %}\n      <h2 class="m" id="h">{{ _("L") }}</h2>\n'
        "    {% endblock %}\n  </div>\n</div>\n",
        68,
        id="a_template_block_stays_open_where_its_indentation_would_overrun",
    ),
    pytest.param(
        '<div>\n<span style="a: 1; b: 2;">x</span>\n</div>\n',
        '<div>\n  <span style="a: 1; b: 2;">x</span>\n</div>\n',
        35,
        id="a_single_style_attribute_is_not_spread_for_the_line",
    ),
]


@pytest.mark.parametrize(("source", "expected", "limit"), test_data)
def test_max_line_length_attributes(source: str, expected: str, limit: int) -> None:
    config = config_builder({"profile": "jinja", "indent": 2, "max_line_length": limit})

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
