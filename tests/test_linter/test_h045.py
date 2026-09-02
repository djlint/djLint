"""Test linter code H045.

uv run pytest tests/test_linter/test_h045.py
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
        ('<iframe src="/report/"></iframe>'),
        ([
            {
                "code": "H045",
                "line": "1:0",
                "match": '<iframe src="/report',
                "message": "Iframe tag should have a title attribute.",
            }
        ]),
        id="no accessible name",
    ),
    pytest.param(
        ('<iframe src="/report/" title="Quarterly report"></iframe>'),
        ([]),
        id="title",
    ),
    pytest.param(
        ('<iframe src="/report/" aria-label="Quarterly report"></iframe>'),
        ([]),
        id="aria-label also names the frame",
    ),
    pytest.param(
        ('<iframe src="/report/" aria-labelledby="heading"></iframe>'),
        ([]),
        id="and so does aria-labelledby",
    ),
    pytest.param(
        ('<iframe src="/report/" title="{{ report.name }}"></iframe>'),
        ([]),
        id="a name written by a template tag counts",
    ),
    pytest.param(
        ('<iframe {% if x %}title="a"{% endif %} src="/report/"></iframe>'),
        ([]),
        id="the scan steps over a template block",
    ),
    pytest.param(
        ('<iframe src="/report/" data-title="x"></iframe>'),
        ([
            {
                "code": "H045",
                "line": "1:0",
                "match": '<iframe src="/report',
                "message": "Iframe tag should have a title attribute.",
            }
        ]),
        id="a name that merely ends in title is a different attribute",
    ),
    pytest.param(
        ('<p title="<iframe src=x>">t</p>'),
        ([]),
        id="markup inside an attribute value is not a tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_h045(source: str, expected: list[LintError]) -> None:
    filename = "test.html"
    output = linter(Config(filename), source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = list(
        filter(lambda x: x not in expected, output[filename])
    ) + list(filter(lambda x: x not in output[filename], expected))

    assert not mismatch
