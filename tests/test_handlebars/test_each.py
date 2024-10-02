"""Test handlebars each tag.

uv run pytest tests/test_handlebars/test_each.py
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
            "{{#each people}}{{print_person}} <p>and more long stuff</p>{{/each}}"
        ),
        (
            "{{#each people }}\n"
            "    {{print_person}}\n"
            "    <p>and more long stuff</p>\n"
            "{{/each}}\n"
        ),
        id="each_tag",
    ),
    pytest.param(
        (
            '{{#each (cprFindConfigObj "inventoryCategories") as |category c | }}'
        ),
        (
            '{{#each (cprFindConfigObj "inventoryCategories") as |category c | }}\n'
        ),
        id="each_tag_with_pipe",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, handlebars_config: Config) -> None:
    output = formatter(handlebars_config, source)

    printer(expected, source, output)
    assert expected == output
