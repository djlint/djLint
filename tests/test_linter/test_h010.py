"""Test linter code H010.

uv run pytest tests/test_linter/test_h010.py
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import yaml

import djlint
from djlint.const import HTML_LOWERCASE_ATTRIBUTE_NAMES
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
    pytest.param(
        ('<div title="the ID=5">y</div>'), ([]), id="name inside a value"
    ),
    pytest.param(
        ('<div data-ID="5">y</div>'),
        ([
            {
                "code": "H010",
                "line": "1:0",
                "match": "<div data-ID=",
                "message": "Attribute names should be lowercase.",
            }
        ]),
        id="uppercase inside a longer name",
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


def test_lowercased_names_agree_with_the_rule() -> None:
    """The formatter must fix exactly the names the rule reports.

    H010 spells its names out in a regex; the formatter reads them from a
    frozenset. A name in one and not the other is a report the formatter
    cannot answer, or a rewrite nothing asked for.
    """
    with (Path(djlint.__file__).parent / "rules.yaml").open("rb") as f:
        rules = yaml.safe_load(f)

    pattern = next(
        rule["rule"]["patterns"][0]
        for rule in rules
        if rule["rule"]["name"] == "H010"
    )
    names = pattern.rpartition("(?:")[2].partition(")")[0].split("|")

    assert {name.lower() for name in names} == HTML_LOWERCASE_ATTRIBUTE_NAMES
