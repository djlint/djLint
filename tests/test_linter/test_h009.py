"""Test linter code H009.

uv run pytest tests/test_linter/test_h009.py
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
        ("<H1>h1</H1>"),
        ([
            {
                "code": "H009",
                "line": "1:1",
                "match": "H1",
                "message": "Tag names should be lowercase.",
            },
            {
                "code": "H009",
                "line": "1:7",
                "match": "/H1",
                "message": "Tag names should be lowercase.",
            },
        ]),
        id="opening",
    ),
    pytest.param(
        ("<A\n>"),
        ([
            {
                "code": "H009",
                "line": "1:1",
                "match": "A",
                "message": "Tag names should be lowercase.",
            },
            {
                "code": "H025",
                "line": "1:0",
                "match": "<A\n>",
                "message": "Tag seems to be an orphan.",
            },
        ]),
        id="line break",
    ),
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
