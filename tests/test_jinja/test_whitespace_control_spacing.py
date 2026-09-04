"""Test whitespace beside a block whose neighbour strips it.

uv run pytest tests/test_jinja/test_whitespace_control_spacing.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "{%- if kwargs -%}\n"
        "  {%- if args -%}, {% endif %}\n"
        "  {%- for k in kwargs -%}{{ k }}{%- endfor -%}\n"
        "{%- endif -%}\n",
        "{%- if kwargs -%}\n"
        "  {%- if args -%}, {% endif %}\n"
        "  {%- for k in kwargs -%}{{ k }}{%- endfor -%}\n"
        "{%- endif -%}\n",
        id="the_next_tag_strips_the_line_break_so_the_space_is_kept",
    ),
    pytest.param(
        "{% if a %}x{% endif -%}\n{% if b %} y{% endif %}\n",
        "{% if a %}x{% endif -%}\n{% if b %} y{% endif %}\n",
        id="the_tag_above_strips_the_line_break_so_the_space_is_kept",
    ),
    pytest.param(
        "{% for i in xs %}{{ i }}{%- if not loop.last -%}, {% endif %}{% endfor %}\n",
        "{% for i in xs %}{{ i }}{%- if not loop.last -%}, {% endif %}{% endfor %}\n",
        id="a_real_neighbour_keeps_the_space_as_before",
    ),
    pytest.param(
        "{%- if value -%}, {% endif %}\n",
        "{%- if value -%},{% endif %}\n",
        id="a_plain_line_break_still_supplies_the_space",
    ),
    pytest.param(
        "<p>x</p>\n{% if v %}, {% endif %}\n<p>y</p>\n",
        "<p>x</p>\n{% if v %},{% endif %}\n<p>y</p>\n",
        id="and_so_does_one_between_two_elements",
    ),
    pytest.param(
        "{%- if v -%} ,{% endif %}\n",
        "{%- if v -%},{% endif %}\n",
        id="jinja_strips_this_one_itself_so_djlint_agrees",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_whitespace_control_spacing(source: str, expected: str) -> None:
    config = config_builder({"profile": "jinja", "indent": 2})

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
