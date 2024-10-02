"""Test symbol entities.

uv run pytest tests/test_html/test_symbol_entities.py
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
            "<p>I will display &euro;</p>\n"
            "<p>I will display &excl;</p>\n"
            "<p>I will display &#8364;</p>\n"
            "<p>I will display &#x20AC;</p>\n"
        ),
        (
            "<p>I will display &euro;</p>\n"
            "<p>I will display &excl;</p>\n"
            "<p>I will display &#8364;</p>\n"
            "<p>I will display &#x20AC;</p>\n"
        ),
        id="symbol_entities",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
