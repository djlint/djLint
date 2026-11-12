"""Test sort_load_tags.

uv run pytest tests/test_config/test_sort_load_tags.py
"""

from __future__ import annotations

import pytest

from djlint.formatter.load_tags import sort_load_tags
from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "{% load static i18n custom_tags %}\n",
        "{% load custom_tags i18n static %}\n",
        id="issue 2718",
    ),
    pytest.param(
        "{% load static i18n static %}\n",
        "{% load i18n static %}\n",
        id="a library loaded twice is loaded once",
    ),
    pytest.param(
        "{% load trans blocktrans from i18n %}\n",
        "{% load blocktrans trans from i18n %}\n",
        id="the names loaded from a library are sorted, the library stays",
    ),
    pytest.param(
        "{% load b a from c d %}\n",
        "{% load b a from c d %}\n",
        id="a from django cannot read is left as written",
    ),
    pytest.param(
        "{%load  i18n   static%}\n",
        "{% load i18n static %}\n",
        id="a tag already in order is only spaced",
    ),
    pytest.param(
        "{% load static\n  i18n %}\n", "{% load i18n static %}\n", id="a tag written across lines"
    ),
    pytest.param(
        "{%- load b a -%}\n", "{%- load a b -%}\n", id="whitespace control is left as written"
    ),
    pytest.param(
        "{% block a %}{% load b a %}{% endblock %}\n",
        "{% block a %}\n    {% load a b %}\n{% endblock %}\n",
        id="a load inside a block",
    ),
    pytest.param(
        "{% comment %}{% load b a %}{% endcomment %}\n",
        "{% comment %}{% load b a %}{% endcomment %}\n",
        id="a load in a comment is text",
    ),
    pytest.param(
        "{% verbatim %}\n{% load b a %}\n{% endverbatim %}\n",
        "{% verbatim %}\n    {% load b a %}\n{% endverbatim %}\n",
        id="a load shown as text",
    ),
    pytest.param("<pre>{% load b a %}</pre>\n", "<pre>{% load b a %}</pre>\n", id="a load in pre"),
    pytest.param(
        "{# djlint:off #}\n{% load b a %}\n{# djlint:on #}\n",
        "{# djlint:off #}\n{% load b a %}\n{# djlint:on #}\n",
        id="djlint off",
    ),
    pytest.param(
        "{% loaded b a %}\n", "{% loaded b a %}\n", id="a tag whose name starts with load"
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str) -> None:
    config = config_builder({"sort_load_tags": True, "profile": "django"})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output


def test_default_keeps_the_order_as_written() -> None:
    source = "{% load static i18n %}\n"
    output = formatter(config_builder({"profile": "django"}), source)

    assert output == source


def test_an_unclosed_tag_does_not_swallow_the_next_one() -> None:
    config = config_builder({"sort_load_tags": True, "profile": "django"})
    source = "{% load b a\n{% load d c %}\n"

    assert sort_load_tags(source, config) == "{% load b a\n{% load c d %}\n"
