"""Test linter code H052.

uv run pytest tests/test_linter/test_h052.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<meta http-equiv="refresh" content="30">'),
        (True),
        id="a page that reloads itself",
    ),
    pytest.param(
        ('<meta content="5; url=/next" http-equiv="refresh">'),
        (True),
        id="the attributes are found in either order",
    ),
    pytest.param(
        ("<meta http-equiv=refresh content=10>"),
        (True),
        id="written without quotes",
    ),
    pytest.param(
        ('<meta http-equiv="REFRESH" content="30">'),
        (True),
        id="the value is read whatever its case",
    ),
    pytest.param(
        ('<meta http-equiv="refresh" content="0; url=/next">'),
        (False),
        id="a delay of zero is an immediate redirect",
    ),
    pytest.param(
        ('<meta http-equiv="refresh" content="0">'),
        (False),
        id="and so is a bare zero",
    ),
    pytest.param(
        ('<meta name="refresh" content="30">'),
        (False),
        id="a name that is not http-equiv",
    ),
    pytest.param(
        ('<meta data-http-equiv="refresh" content="30">'),
        (False),
        id="a name that merely ends in http-equiv",
    ),
    pytest.param(('<meta charset="utf-8">'), (False), id="another meta tag"),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h052(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H052" in codes) is reported
