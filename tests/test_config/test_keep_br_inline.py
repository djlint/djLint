"""Test keep_br_inline.

uv run pytest tests/test_config/test_keep_br_inline.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "<p>\n  first<br>\n  second<br>\n  third\n</p>\n",
        "<p>\n  first<br>\n  second<br>\n  third\n</p>\n",
        id="a break stays on the line of the text it breaks",
    ),
    pytest.param(
        "<p>a<br />b</p>\n",
        "<p>\n  a<br />b\n</p>\n",
        id="self closing form, the p breaks as it always does",
    ),
    pytest.param(
        "<p>a<hr>b</p>\n",
        "<p>\n  a\n  <hr>\n  b\n</p>\n",
        id="hr is unaffected",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str) -> None:
    config = config_builder({"indent": 2, "keep_br_inline": True})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output


def test_default_gives_a_break_its_own_line() -> None:
    config = config_builder({"indent": 2})
    output = formatter(config, "<p>\n  first<br>\n  second\n</p>\n")

    assert output == "<p>\n  first\n  <br>\n  second\n</p>\n"
