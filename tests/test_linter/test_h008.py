"""Test linter code H008.

poetry run pytest tests/test_linter/test_h008.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("<div class='test'>"),
        (
            [
                {
                    "code": "H008",
                    "line": "1:0",
                    "match": "<div class='test'",
                    "message": "Attributes should be double quoted.",
                },
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<div class='test'>",
                    "message": "Tag seems to be an orphan.",
                },
            ]
        ),
        id="one",
    ),
    pytest.param(
        ("<div class='test\nclass-two'>"),
        (
            [
                {
                    "code": "H008",
                    "line": "1:0",
                    "match": "<div class='test\ncla",
                    "message": "Attributes should be double quoted.",
                },
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<div class='test\ncla",
                    "message": "Tag seems to be an orphan.",
                },
            ]
        ),
        id="line break",
    ),
    pytest.param(
        (
            '<link rel="stylesheet" href="styles.css" media="print" onload="this.media=\'all\'" media='
            "/>"
        ),
        ([]),
        id="one",
    ),
    pytest.param(
        (
            '<link rel="stylesheet" href="styles.css" media="print" onload="this.media=\'all\'"/>'
        ),
        ([]),
        id="one",
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
