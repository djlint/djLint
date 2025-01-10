"""Test for _hyperscript.

uv run pytest tests/test_html/test_hyperscript.py
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
            "<div _='on click increment :x then put it into the <output/> in me'>\n"
            "    Clicks:\n"
            "    <output>0</output>\n"
            "</div>\n"
        ),
        (
            "<div _='on click increment :x then put it into the <output/> in me'>\n"
            "    Clicks:\n"
            "    <output>0</output>\n"
            "</div>\n"
        ),
        id="html_tags_in_attributes",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
