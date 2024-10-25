"""Test django spaceless tag.

uv run pytest tests/test_django/test_tag_spaces.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        ("{% a %}\n{%b       %}{%+c%}{%-d+%}\n{#a}{{g {%a%}}}{%l{{q}}+%}"),
        (
            "{% a %}\n"
            "{% b %}{%+ c %}{%- d +%}\n"
            "{#a}{{ g {% a % }}}{% l{{ q }} +%}\n"
        ),
        ({}),
        id="messy stuff",
    ),
    pytest.param(
        ("{% a %}\n{%b%}{%c%}{%-d+%}\n{#a}{{g {%a%}}}{%l{{q}}+%}"),
        ("{% a %}\n{%b%}{%c%}{%-d+%}\n{#a}{{g {%a%}}}{%l{{q}}+%}\n"),
        ({"profile": "handlebars"}),
        id="messy stuff",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
