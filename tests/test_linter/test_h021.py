"""Test linter code H010.

poetry run pytest tests/test_linter/test_h021.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<div style="asdf"></div>'),
        (
            [
                {
                    "code": "H021",
                    "line": "1:0",
                    "match": "<div style=",
                    "message": "Inline styles should be avoided.",
                }
            ]
        ),
        id="simple",
    ),
    pytest.param(
        (
            '<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet" />'
        ),
        ([]),
        id="missing",
    ),
    pytest.param(
        ('<acronym title="Cascading Style Sheets">CSS</acronym>'),
        ([]),
        id="outside tag",
    ),
    pytest.param(
        ('<div style="test {%"><div style="test {{">'),
        (
            [
                {
                    "code": "H025",
                    "line": "1:21",
                    "match": '<div style="test {{"',
                    "message": "Tag seems to be an orphan.",
                },
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": '<div style="test {%"',
                    "message": "Tag seems to be an orphan.",
                },
            ]
        ),
        id="template syntax in style",
    ),
    pytest.param(
        ('<acronym title="Cascading Style Sheets">CSS</acronym>'),
        ([]),
        id="outside tag",
    ),
    pytest.param(
        ('<div style="color:green"\n' '     class="foo">\n' "</div>"),
        (
            [
                {
                    "code": "H021",
                    "line": "1:0",
                    "match": "<div style=",
                    "message": "Inline styles should be avoided.",
                }
            ]
        ),
        id="line breaks",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    filename = "test.html"
    output = linter(basic_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = list(filter(lambda x: x not in expected, output[filename])) + list(
        filter(lambda x: x not in output[filename], expected)
    )

    assert len(mismatch) == 0
