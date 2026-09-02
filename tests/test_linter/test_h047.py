"""Test linter code H047.

uv run pytest tests/test_linter/test_h047.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<button aria-hidden="true">x</button>'),
        (True),
        id="a button takes focus",
    ),
    pytest.param(
        ('<a href="/x" aria-hidden="true">x</a>'),
        (True),
        id="a link with an href takes focus",
    ),
    pytest.param(
        ('<div tabindex="0" aria-hidden="true">x</div>'),
        (True),
        id="so does a tabindex of zero",
    ),
    pytest.param(
        ('<div contenteditable aria-hidden="true">x</div>'),
        (True),
        id="and so does contenteditable",
    ),
    pytest.param(
        ('<span aria-hidden="true">x</span>'),
        (False),
        id="hiding a decorative icon is the ordinary use",
    ),
    pytest.param(
        ('<i class="fa" aria-hidden="true"></i>'),
        (False),
        id="the same icon written as an i",
    ),
    pytest.param(
        ('<a aria-hidden="true">x</a>'),
        (False),
        id="a link with no href is not focusable",
    ),
    pytest.param(
        ('<button disabled aria-hidden="true">x</button>'),
        (False),
        id="a disabled control is out of the order",
    ),
    pytest.param(
        ('<button tabindex="-1" aria-hidden="true">x</button>'),
        (False),
        id="and so is one taken out by hand",
    ),
    pytest.param(
        ('<input type="hidden" aria-hidden="true">'),
        (False),
        id="a hidden input is not focusable",
    ),
    pytest.param(
        ('<button aria-hidden="false">x</button>'),
        (False),
        id="only true hides the element",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h047(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H047" in codes) is reported
