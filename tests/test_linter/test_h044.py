"""Test linter code H044.

uv run pytest tests/test_linter/test_h044.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from djlint.settings import Config
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.types import LintError

test_data = [
    pytest.param(
        ("<table><thead><tr><th>a</th><th>b</th></tr></thead></table>"),
        ([]),
        id="all_th",
    ),
    pytest.param(
        ("<table><thead><tr><td>a</td><td>b</td></tr></thead></table>"),
        ([]),
        id="all_td",
    ),
    pytest.param(
        ("<table><thead><tr><th>a</th><td>b</td></tr></thead></table>"),
        ([
            {
                "code": "H044",
                "line": "1:28",
                "match": "<td>",
                "message": "Thead should not mix th and td cells.",
            }
        ]),
        id="td_among_th",
    ),
    pytest.param(
        ("<table><thead><tr><td>a</td><th>b</th></tr></thead></table>"),
        ([
            {
                "code": "H044",
                "line": "1:28",
                "match": "<th>",
                "message": "Thead should not mix th and td cells.",
            }
        ]),
        id="th_among_td",
    ),
    pytest.param(
        ("<table><tbody><tr><th>a</th><td>b</td></tr></tbody></table>"),
        ([]),
        id="mixture_outside_a_thead",
    ),
    pytest.param(
        (
            "<table><thead><tr><th>a</th></tr></thead></table>"
            "<table><thead><tr><td>b</td></tr></thead></table>"
        ),
        ([]),
        id="each_thead_decides_for_itself",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: list[LintError]) -> None:
    config = Config("dummy/source.html", include="H044")
    filename = "test.html"
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])
    assert output[filename] == expected
