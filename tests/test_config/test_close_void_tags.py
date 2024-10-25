"""Test for custom html.

uv run pytest tests/test_config/test_close_void_tags.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(("<img><meta>"), ("<img>\n<meta>\n"), ({}), id="default"),
    pytest.param(
        ("<img><div><meta>"),
        ("<img />\n<div>\n    <meta />\n"),
        ({"close_void_tags": True}),
        id="config",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
