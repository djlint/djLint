"""Test tags whose name a template expression writes.

uv run pytest tests/test_jinja/test_template_tag_name.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "<{{ tag }}\n"
        "  {%- if attrs %}{% include 'attrs.html' %}{% endif -%}\n"
        ">Text</{{ tag }}>\n",
        "<{{ tag }} {%- if attrs %}{% include 'attrs.html' %}{% endif -%}"
        ">Text</{{ tag }}>\n",
        id="a_guarded_block_stays_in_the_attribute_area",
    ),
    pytest.param(
        "<{{ tag }} class='a'>Text</{{ tag }}>\n",
        '<{{ tag }} class="a">Text</{{ tag }}>\n',
        id="its_attributes_are_normalised_like_any_other_tag",
    ),
    pytest.param(
        "<div>\n  <{{ tag }}>Text</{{ tag }}>\n</div>\n",
        "<div>\n  <{{ tag }}>Text</{{ tag }}>\n</div>\n",
        id="the_element_indents_like_any_other",
    ),
    pytest.param(
        "<{{ tag }}{% if attrs %}{% include 'a.html' %}{% endif %}>\n"
        "  {{- label -}}\n"
        "</{{ tag }}>\n",
        "<{{ tag }}{% if attrs %}{% include 'a.html' %}{% endif %}>\n"
        "  {{- label -}}\n"
        "</{{ tag }}>\n",
        id="its_contents_are_indented_inside_it",
    ),
    pytest.param(
        "<{{ a }}>\n  <{{ b }}>\n    x\n  </{{ b }}>\n</{{ a }}>\n",
        "<{{ a }}>\n  <{{ b }}>\n    x\n  </{{ b }}>\n</{{ a }}>\n",
        id="and_they_nest",
    ),
    pytest.param(
        "<{{ tag }} />\n<p>x</p>\n",
        "<{{ tag }} />\n<p>x</p>\n",
        id="a_self_closed_one_opens_nothing",
    ),
    pytest.param(
        "<${tag}>\n  x\n</${tag}>\n",
        "<${tag}>\n  x\n</${tag}>\n",
        id="a_mako_expression_names_a_tag_too",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_template_tag_name(source: str, expected: str) -> None:
    config = config_builder({
        "profile": "jinja",
        "indent": 2,
        "quote_style": "single",
    })

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output
