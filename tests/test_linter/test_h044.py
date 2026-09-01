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
        # https://www.w3.org/WAI/tutorials/tables/two-headers/ opens the
        # header row with an empty corner cell
        (
            "<table><thead><tr><td></td>"
            "<th scope='col'>Mon</th><th scope='col'>Tue</th>"
            "</tr></thead></table>"
        ),
        ([]),
        id="w3c_wai_corner_cell",
    ),
    pytest.param(
        # the html specification puts a row of th and a row of td in one
        # thead, the second explaining how to fill the table in
        (
            "<table><thead>"
            "<tr><th>a</th><th>b</th></tr>"
            "<tr><td>fill in</td><td>fill in</td></tr>"
            "</thead></table>"
        ),
        ([]),
        id="explanation_row",
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


def test_mutually_exclusive_branches_are_not_a_mixture(
    django_config: Config,
) -> None:
    source = (
        "<table><thead><tr>"
        "{% if numeric %}<th>Total</th>{% else %}<td>Total</td>{% endif %}"
        "</tr></thead></table>\n"
    )
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]
