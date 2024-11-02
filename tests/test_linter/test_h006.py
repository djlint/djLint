"""Test linter code H006.

uv run pytest tests/test_linter/test_h006.py
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
        ('<img alt="test"/>'),
        ([
            {
                "code": "H006",
                "line": "1:0",
                "match": '<img alt="test"/>',
                "message": "Img tag should have height and width attributes.",
            }
        ]),
        id="one",
    ),
    pytest.param(
        ('<img \n alt="test" width="10" height="10"/>'), ([]), id="line break"
    ),
    pytest.param(
        (
            '{# [INFO][JINJA] I use syntax "{% if <img alt=""\n'
            ' if I want that something happened solely if "img" exists in the content of my articles #}\n'
            "\n"
            ' <script src="script.js" defer></script>\n'
        ),
        ([]),
        id="partial ignored",
    ),
    pytest.param(
        ("<img><img>"),
        ([
            {
                "code": "H006",
                "line": "1:0",
                "match": "<img>",
                "message": "Img tag should have height and width attributes.",
            },
            {
                "code": "H006",
                "line": "1:5",
                "match": "<img>",
                "message": "Img tag should have height and width attributes.",
            },
            {
                "code": "H013",
                "line": "1:0",
                "match": "<img>",
                "message": "Img tag should have an alt attribute.",
            },
            {
                "code": "H013",
                "line": "1:5",
                "match": "<img>",
                "message": "Img tag should have an alt attribute.",
            },
        ]),
        id="test empty with two blocks",
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
