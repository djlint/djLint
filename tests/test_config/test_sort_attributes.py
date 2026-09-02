"""Test sort_attributes.

uv run pytest tests/test_config/test_sort_attributes.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        '<div data-z="1" class="c" id="i" aria-label="a"></div>\n',
        '<div id="i" class="c" aria-label="a" data-z="1"></div>\n',
        id="id comes first, then class, then the rest by name",
    ),
    pytest.param(
        '<a href="{% url \'p\' %}" class="c" id="i"></a>\n',
        '<a id="i" class="c" href="{% url \'p\' %}"></a>\n',
        id="a template tag inside a value travels with its attribute",
    ),
    pytest.param(
        '<div {% if x %}a="1"{% endif %} b="2"></div>\n',
        '<div {% if x %}a="1"{% endif %} b="2"></div>\n',
        id="a template tag beside the attributes holds the order",
    ),
    pytest.param(
        '<input a="1" a="2" b="3">\n',
        '<input a="1" a="2" b="3">\n',
        id="a name written twice keeps the one a browser reads",
    ),
    pytest.param(
        "<input required disabled name=n checked>\n",
        '<input checked disabled name="n" required>\n',
        id="an attribute written without a value sorts on its name",
    ),
    pytest.param(
        '<div CLASS="c" ID="i"></div>\n',
        '<div id="i" class="c"></div>\n',
        id="names are sorted after they are lowercased",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str) -> None:
    config = config_builder({"sort_attributes": True, "profile": "django"})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output


def test_default_keeps_the_order_as_written() -> None:
    source = '<div data-z="1" class="c" id="i"></div>\n'
    output = formatter(config_builder({}), source)

    assert output == source
