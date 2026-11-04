"""Tests for Aurelia.

uv run pytest tests/test_html/test_aurelia.py
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
        ('<template>\n    <i class.bind="icon"></i>\n</template>\n'),
        ('<template>\n    <i class.bind="icon"></i>\n</template>\n'),
        id="aurelia",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
