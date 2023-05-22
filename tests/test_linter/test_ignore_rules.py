"""Test linter code H005.

poetry run pytest tests/test_linter/test_ignore_rules.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("<img>{# djlint:off H004,H006,H013 #}\n" "<img>\n"),
        (
            [
                {
                    "code": "H006",
                    "line": "1:0",
                    "match": "<img>",
                    "message": "Img tag should have height and width attributes.",
                },
                {
                    "code": "H013",
                    "line": "1:0",
                    "match": "<img>",
                    "message": "Img tag should have an alt attribute.",
                },
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
