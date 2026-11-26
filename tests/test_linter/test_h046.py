"""Test linter code H046.

uv run pytest tests/test_linter/test_h046.py
"""

from __future__ import annotations

import pytest

from djlint.settings import Config
from tests.conftest import linter

test_data = [
    pytest.param(('<input tabindex="1">'), (True), id="a positive value jumps the tab order"),
    pytest.param(("<input tabindex=3>"), (True), id="an unquoted value counts too"),
    pytest.param(('<div\n     tabindex="2">x</div>'), (True), id="the attribute may start a line"),
    pytest.param(('<input tabindex="0">'), (False), id="zero keeps the document order"),
    pytest.param(('<input tabindex="-1">'), (False), id="minus one leaves the tab order"),
    pytest.param(
        ('<div data-tabindex="1">x</div>'), (False), id="a name that merely ends in tabindex"
    ),
    pytest.param(
        ('<div tabindex="{{ i }}">x</div>'), (False), id="a value written by a template tag"
    ),
    pytest.param(
        ('<div title="tabindex=1">x</div>'), (False), id="text inside a value is not an attribute"
    ),
    pytest.param(
        ('<div title="press tabindex=1">x</div>'),
        (False),
        id="spaced text inside a value is not an attribute either",
    ),
    pytest.param(("<p>set tabindex=1 on it</p>"), (False), id="text between tags"),
    pytest.param(('<div :tabindex="1">x</div>'), (False), id="a framework binding"),
    pytest.param(
        ('<li {% if active %} tabindex="1" {% endif %}>x</li>'),
        (True),
        id="an attribute written by a template branch",
    ),
    pytest.param(('<div tabindex =\n"1">x</div>'), (True), id="spaced across a line"),
    pytest.param(
        ('<a title=don\'t>x</a>\n<div tabindex="3">x</div>'),
        (True),
        id="after a tag that leaves a quote open",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h046(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H046" in codes) is reported
