"""Test linter code H009.

poetry run pytest tests/test_linter/test_h009.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("<H1>h1</H1>"),
        (
            [
                {
                    "code": "H009",
                    "line": "1:1",
                    "match": "H1",
                    "message": "Tag names should be lowercase.",
                },
                {
                    "code": "H009",
                    "line": "1:7",
                    "match": "/H1",
                    "message": "Tag names should be lowercase.",
                },
            ]
        ),
        id="opening",
    ),
    pytest.param(
        ("<A\n>"),
        (
            [
                {
                    "code": "H009",
                    "line": "1:1",
                    "match": "A",
                    "message": "Tag names should be lowercase.",
                },
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<A\n>",
                    "message": "Tag seems to be an orphan.",
                },
            ]
        ),
        id="line break",
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
