"""Test linter code H010.

poetry run pytest tests/test_linter/test_h010.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<img HEIGHT="12" Width="3" alT="none" />'),
        (
            [
                {
                    "code": "H010",
                    "line": "1:0",
                    "match": "<img HEIGHT=",
                    "message": "Attribute names should be lowercase.",
                }
            ]
        ),
        id="opening",
    ),
    pytest.param(
        ("<li>ID=username</li>"),
        ([]),
        id="opening",
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
