"""Test disable.

uv run pytest tests/test_djlint/test_ignore.py
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
        ("{# djlint:off #}\n<img \n/>"),
        ("{# djlint:off #}\n<img \n/>\n"),
        id="don't compress",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
