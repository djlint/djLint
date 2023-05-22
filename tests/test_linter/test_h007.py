"""Test linter code H007.

poetry run pytest tests/test_linter/test_h007.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<html lang="en">'),
        (
            [
                {
                    "code": "H007",
                    "line": "1:0",
                    "match": "<html",
                    "message": "<!DOCTYPE ... > should be present before the html tag.",
                },
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": '<html lang="en">',
                    "message": "Tag seems to be an orphan.",
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
