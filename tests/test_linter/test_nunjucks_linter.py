"""Djlint linter rule tests for nunjucks.

uv run pytest tests/test_linter/test_nunjucks_linter.py

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
        ("{%- test-%}"),
        ([
            {
                "code": "T001",
                "line": "1:0",
                "match": "{%- test-%}",
                "message": "Variables should be wrapped in a whitespace.",
            }
        ]),
        id="T001",
    ),
    pytest.param(
        ("{%-test -%}"),
        ([
            {
                "code": "T001",
                "line": "1:0",
                "match": "{%-test -%}",
                "message": "Variables should be wrapped in a whitespace.",
            }
        ]),
        id="T001_2",
    ),
    pytest.param(("{%- test -%}"), ([]), id="T001_3"),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(
    source: str, expected: list[LintError], nunjucks_config: Config
) -> None:
    filename = "test.html"
    output = linter(nunjucks_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
