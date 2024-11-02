"""Test linter code H005.

uv run pytest tests/test_linter/test_ignore_rules.py
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
        ("<img>{# djlint:off H004,H006,H013 #}\n<img>\n"),
        ([
            {
                "code": "H006",
                "line": "1:0",
                "match": "<img>",
                "message": "Img tag should have height and width attributes.",
            },
            {
                "code": "H013",
                "line": "1:0",
                "match": "<img>",
                "message": "Img tag should have an alt attribute.",
            },
        ]),
        id="one",
    )
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
