"""Test linter code H005.

uv run pytest tests/test_linter/test_h005.py
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
        ("<!DOCTYPE html>\n<html>"),
        ([
            {
                "code": "H005",
                "line": "2:0",
                "match": "<html>",
                "message": "Html tag should have lang attribute.",
            },
            {
                "code": "H025",
                "line": "2:0",
                "match": "<html>",
                "message": "Tag seems to be an orphan.",
            },
        ]),
        id="one",
    ),
    pytest.param(
        ("<a\n>"),
        ([
            {
                "code": "H025",
                "line": "1:0",
                "match": "<a\n>",
                "message": "Tag seems to be an orphan.",
            }
        ]),
        id="one",
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
