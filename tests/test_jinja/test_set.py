"""Test jinja set tags.

uv run pytest tests/test_jinja/test_set.py
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
        '{% set dir = "example" %}\n{% set foo = dir %}',
        '{% set dir = "example" %}\n{% set foo = dir %}\n',
        id="shadow_builtin",
    ),
    pytest.param(
        '{% set x = print("Hello") %}',
        '{% set x = print("Hello") %}\n',
        id="do_not_execute_expression",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
