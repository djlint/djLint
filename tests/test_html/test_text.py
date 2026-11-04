"""Test text.

uv run pytest tests/test_html/test_text.py
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
            "<a-long-long-long-element>foo bar foo bar\n"
            "  foo bar foo bar foo bar foo bar foo bar\n"
            "  foo bar foo bar</a-long-long-long-element>\n"
            "<!-- The end tag should stay in 80 print width -->\n"
        ),
        (
            "<a-long-long-long-element>foo bar foo bar\n"
            "    foo bar foo bar foo bar foo bar foo bar\n"
            "    foo bar foo bar</a-long-long-long-element>\n"
            "    <!-- The end tag should stay in 80 print width -->\n"
        ),
        id="tag_should_in_fill",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
