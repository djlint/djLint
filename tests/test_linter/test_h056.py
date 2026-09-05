"""Test linter code H056.

uv run pytest tests/test_linter/test_h056.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(('<img src="">'), (True), id="an empty src"),
    pytest.param(
        ("<img src='' alt=\"x\">"), (True), id="empty in single quotes"
    ),
    pytest.param(
        ('<img alt="x" src="">'), (True), id="found after another attribute"
    ),
    pytest.param(('<script src=""></script>'), (True), id="a script"),
    pytest.param(('<iframe src=""></iframe>'), (True), id="an iframe"),
    pytest.param(("<img src>"), (True), id="a src with no value at all"),
    pytest.param(('<video src=""></video>'), (True), id="a video"),
    pytest.param(('<source src="" type="video/mp4">'), (True), id="a source"),
    pytest.param(
        ("<img src=>"), (True), id="an equals sign with nothing after"
    ),
    pytest.param(("<img src/>"), (True), id="valueless on a self-closing tag"),
    pytest.param(('<IMG SRC="">'), (True), id="read whatever the case"),
    pytest.param(
        ('<img {% if x %}class="a"{% endif %} src="">'),
        (True),
        id="a template tag between the attributes is stepped over",
    ),
    pytest.param(('<img src="a.png">'), (False), id="a src with a value"),
    pytest.param(
        ('<img src="{{ url }}">'), (False), id="a value written by a variable"
    ),
    pytest.param(
        ("<img src=\"{% static 'a.png' %}\">"),
        (False),
        id="a value written by a template tag",
    ),
    pytest.param(
        ('<img data-src="" src="a.png">'),
        (False),
        id="a name that merely ends in src",
    ),
    pytest.param(
        ('<img srcset="" src="a.png">'),
        (False),
        id="srcset is a different attribute",
    ),
    pytest.param(
        ('<img src=" ">'), (False), id="a value that is only whitespace"
    ),
    pytest.param(('<a href="">x</a>'), (False), id="href is not src"),
    pytest.param(
        ("<p title=\"<img src=''>\">x</p>"),
        (False),
        id="markup inside an attribute value",
    ),
    pytest.param(('<div src="">'), (False), id="not a media or script element"),
    pytest.param(
        ('<img src = "a.png">'),
        (False),
        id="spaces around the equals sign with a value",
    ),
    pytest.param(
        ('<img-lazy src="">'),
        (False),
        id="a custom element whose name starts with img",
    ),
    pytest.param(('<img :src="" alt="x">'), (False), id="a framework binding"),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h056(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H056" in codes) is reported
