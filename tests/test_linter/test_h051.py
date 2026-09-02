"""Test linter code H051.

uv run pytest tests/test_linter/test_h051.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(('<div role="buton">x</div>'), (True), id="a misspelled role"),
    pytest.param(
        ("<div role=buton>x</div>"),
        (True),
        id="the same written without quotes",
    ),
    pytest.param(
        ('<div role="landmark">x</div>'),
        (True),
        id="an abstract role, which authors may not write",
    ),
    pytest.param(
        ('<div role="doc-subtitle headin">x</div>'),
        (True),
        id="a fallback list whose second word is wrong",
    ),
    pytest.param(
        ('<div role="button">x</div>'), (False), id="a role ARIA defines"
    ),
    pytest.param(
        ('<div role="BUTTON">x</div>'),
        (False),
        id="the name is read whatever its case",
    ),
    pytest.param(
        ('<div role="doc-subtitle heading">x</div>'),
        (False),
        id="a fallback list of two good roles",
    ),
    pytest.param(
        ('<svg><g role="graphics-symbol"></g></svg>'),
        (False),
        id="a role the graphics module adds",
    ),
    pytest.param(
        ('<div role="{{ r }}">x</div>'),
        (False),
        id="a value a template writes is unknowable",
    ),
    pytest.param(
        ('<div role="{% if a %}tab{% endif %}">x</div>'),
        (False),
        id="and so is one built by a block tag",
    ),
    pytest.param(
        ('<div :role="r">x</div>'),
        (False),
        id="a framework binding is not a plain role",
    ),
    pytest.param(
        ('<div data-role="buton">x</div>'),
        (False),
        id="a name that merely ends in role",
    ),
    pytest.param(("<div>x</div>"), (False), id="no role at all"),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h051(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H051" in codes) is reported
