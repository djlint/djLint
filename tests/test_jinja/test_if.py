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
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
