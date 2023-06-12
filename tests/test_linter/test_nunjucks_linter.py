"""Djlint linter rule tests for nunjucks.

poetry run pytest tests/test_linter/test_nunjucks_linter.py

"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("{%- test-%}"),
        (
            [
                {
                    "code": "T001",
                    "line": "1:0",
                    "match": "{%- test-%}",
                    "message": "Variables should be wrapped in a whitespace.",
                }
            ]
        ),
        id="T001",
    ),
    pytest.param(
        ("{%-test -%}"),
        (
            [
                {
                    "code": "T001",
                    "line": "1:0",
                    "match": "{%-test -%}",
                    "message": "Variables should be wrapped in a whitespace.",
                }
            ]
        ),
        id="T001_2",
    ),
    pytest.param(
        ("{%- test -%}"),
        ([]),
        id="T001_3",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, nunjucks_config):
    filename = "test.html"
    output = linter(nunjucks_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = list(filter(lambda x: x not in expected, output[filename])) + list(
        filter(lambda x: x not in output[filename], expected)
    )

    assert len(mismatch) == 0
