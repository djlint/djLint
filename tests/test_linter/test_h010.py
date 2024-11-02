"""Test linter code H010.

uv run pytest tests/test_linter/test_h010.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.settings import Config
    from djlint.types import LintError

test_data = [
    pytest.param(
        ('<img HEIGHT="12" Width="3" alT="none" />'),
        ([
            {
                "code": "H010",
                "line": "1:0",
                "match": "<img HEIGHT=",
                "message": "Attribute names should be lowercase.",
            }
        ]),
        id="opening",
    ),
    pytest.param(("<li>ID=username</li>"), ([]), id="opening"),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(
    source: str, expected: list[LintError], basic_config: Config
) -> None:
    filename = "test.html"
    output = linter(basic_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
