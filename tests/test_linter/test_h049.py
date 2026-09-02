"""Test linter code H049.

uv run pytest tests/test_linter/test_h049.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        (
            '<meta name="viewport" content="width=device-width, user-scalable=no">'
        ),
        (True),
        id="zoom turned off",
    ),
    pytest.param(
        ('<meta name="viewport" content="maximum-scale=1.0">'),
        (True),
        id="a maximum below two",
    ),
    pytest.param(
        ('<meta name="viewport" content="maximum-scale=1.5">'),
        (True),
        id="still below two",
    ),
    pytest.param(
        ('<meta content="user-scalable=no" name="viewport">'),
        (True),
        id="written the other way round",
    ),
    pytest.param(
        (
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
        ),
        (False),
        id="an ordinary viewport",
    ),
    pytest.param(
        ('<meta name="viewport" content="maximum-scale=5">'),
        (False),
        id="a maximum that allows zoom",
    ),
    pytest.param(
        ('<meta name="viewport" content="user-scalable=yes">'),
        (False),
        id="zoom left on",
    ),
    pytest.param(
        ('<meta name="description" content="user-scalable=no">'),
        (False),
        id="another meta tag entirely",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h049(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H049" in codes) is reported
