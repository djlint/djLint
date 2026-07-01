"""Test jinja if tag.

uv run pytest tests/test_jinja/test_if.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        "Dog{% if another_condition != 1 %}s{% endif %}",
        "Dog{% if another_condition != 1 %}s{% endif %}\n",
        id="issue_182_inline_if_suffix",
    ),
    pytest.param(
        "0 {% if plural %}dogs{% else %}dog{% endif %}",
        "0 {% if plural %}dogs{% else %}dog{% endif %}\n",
        id="issue_182_inline_if_else",
    ),
    pytest.param(
        "<p>Dog{% if condition %}s{% endif %}</p>",
        "<p>Dog{% if condition %}s{% endif %}</p>\n",
        id="issue_182_inline_if_in_tag_text",
    ),
    pytest.param(
        "Dog{% if condition %}\ns{% endif %}",
        "Dog{% if condition %}\ns{% endif %}\n",
        id="issue_182_inline_if_prefix_multiline",
    ),
    pytest.param(
        "__DJLINT_WS_LINE_0__\nDog{% if condition %}s{% endif %}",
        "__DJLINT_WS_LINE_0__\nDog{% if condition %}s{% endif %}\n",
        id="inline_if_preserves_marker_like_text",
    ),
    pytest.param(
        (
            "{% block content %}\n"
            "    <p>\n"
            "        {{ a }} foo\n"
            "        {%- if b %}- {{ b }} bar{% endif %}\n"
            "        {{ c }} baz\n"
            "    </p>\n"
            "    {% if a %}<span>x</span>{% endif %}\n"
            "{% endblock %}\n"
        ),
        (
            "{% block content %}\n"
            "    <p>\n"
            "        {{ a }} foo\n"
            "        {%- if b %}- {{ b }} bar{% endif %}\n"
            "        {{ c }} baz\n"
            "    </p>\n"
            "    {% if a %}<span>x</span>{% endif %}\n"
            "{% endblock %}\n"
        ),
        id="issue_2071_inline_trim_if",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
