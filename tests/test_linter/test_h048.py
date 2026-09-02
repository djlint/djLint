"""Test linter code H048.

uv run pytest tests/test_linter/test_h048.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<div aria-lable="x">y</div>'),
        (True),
        id="a misspelled name does nothing",
    ),
    pytest.param(
        ('<div aria-hidden-thing="x">y</div>'),
        (True),
        id="and neither does an invented one",
    ),
    pytest.param(
        ('<div aria-label="x">y</div>'),
        (False),
        id="a name the specification defines",
    ),
    pytest.param(
        ('<div aria-description="x">y</div>'),
        (False),
        id="including the newer ones",
    ),
    pytest.param(
        ('<div :aria-label="x">y</div>'),
        (False),
        id="a vue binding is not a plain aria name",
    ),
    pytest.param(
        ('<div [attr.aria-label]="x">y</div>'),
        (False),
        id="nor is an angular one",
    ),
    pytest.param(
        ('<div data-aria-lable="x">y</div>'),
        (False),
        id="nor is a data attribute",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h048(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H048" in codes) is reported
