"""Test linter code H005.

poetry run pytest tests/test_linter/test_h005.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("<!DOCTYPE html>\n<html>"),
        (
            [
                {
                    "code": "H005",
                    "line": "2:0",
                    "match": "<html>",
                    "message": "Html tag should have lang attribute.",
                },
                {
                    "code": "H025",
                    "line": "2:0",
                    "match": "<html>",
                    "message": "Tag seems to be an orphan.",
                },
            ]
        ),
        id="one",
    ),
    pytest.param(
        ("<a\n>"),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<a\n>",
                    "message": "Tag seems to be an orphan.",
                }
            ]
        ),
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
