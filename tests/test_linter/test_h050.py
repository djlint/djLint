"""Test linter code H050.

uv run pytest tests/test_linter/test_h050.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ("<center>x</center>"), (True), id="center was replaced by css"
    ),
    pytest.param(('<font color="red">x</font>'), (True), id="so was font"),
    pytest.param(
        ("<marquee>x</marquee>"), (True), id="marquee was never standard"
    ),
    pytest.param(
        ("<TT>x</TT>"), (True), id="the name is read whatever its case"
    ),
    pytest.param(
        ("<frameset><frame src=/a></frameset>"),
        (True),
        id="frames are gone from html",
    ),
    pytest.param(
        ("<p>a<strike>b</strike></p>"),
        (True),
        id="strike gave way to del and s",
    ),
    pytest.param(("<div>x</div>"), (False), id="an element html still defines"),
    pytest.param(
        ("<font-picker></font-picker>"),
        (False),
        id="a custom element whose name starts with one",
    ),
    pytest.param(
        ("<centered-box>x</centered-box>"),
        (False),
        id="and one that starts with center",
    ),
    pytest.param(
        ('<p title="write <center> here">x</p>'),
        (False),
        id="a name written inside an attribute value is text",
    ),
    pytest.param(
        ("<del>x</del><s>y</s><em>z</em>"),
        (False),
        id="the elements that replaced them",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h050(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H050" in codes) is reported
