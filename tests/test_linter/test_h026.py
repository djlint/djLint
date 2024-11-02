"""Test linter code H026.

uv run pytest tests/test_linter/test_h026.py
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
        ('<asdf id="" >'),
        ([
            {
                "code": "H025",
                "line": "1:0",
                "match": '<asdf id="" >',
                "message": "Tag seems to be an orphan.",
            },
            {
                "code": "H026",
                "line": "1:0",
                "match": '<asdf id=""',
                "message": "Empty id and class tags can be removed.",
            },
        ]),
        id="emptied quotes",
    ),
    pytest.param(
        ("<asdf id >"),
        ([
            {
                "code": "H025",
                "line": "1:0",
                "match": "<asdf id >",
                "message": "Tag seems to be an orphan.",
            },
            {
                "code": "H026",
                "line": "1:0",
                "match": "<asdf id",
                "message": "Empty id and class tags can be removed.",
            },
        ]),
        id="no quotes",
    ),
    pytest.param(
        ('<asdf class="" >'),
        ([
            {
                "code": "H025",
                "line": "1:0",
                "match": '<asdf class="" >',
                "message": "Tag seems to be an orphan.",
            },
            {
                "code": "H026",
                "line": "1:0",
                "match": '<asdf class=""',
                "message": "Empty id and class tags can be removed.",
            },
        ]),
        id="class",
    ),
    pytest.param(('<asdf {% class="" %}></asdf>'), ([]), id="class in tag"),
    pytest.param(
        ("<div x-id-y></div><div id-y></div><div x-id></div>"),
        ([]),
        id="prefix and suffix",
    ),
    pytest.param(
        (
            '<div x-id-y=""></div><div id-y=""></div><div x-id=""></div><div data-id=""></div>'
        ),
        ([]),
        id="prefix and suffix quoted",
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
