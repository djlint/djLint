"""Test linter code H026.

poetry run pytest tests/test_linter/test_h026.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<asdf id="" >'),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": '<asdf id="" >',
                    "message": "Tag seems to be an orphan.",
                },
                {
                    "code": "H026",
                    "line": "1:0",
                    "match": '<asdf id=""',
                    "message": "Empty id and class tags can be removed.",
                },
            ]
        ),
        id="empted quotes",
    ),
    pytest.param(
        ("<asdf id >"),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": "<asdf id >",
                    "message": "Tag seems to be an orphan.",
                },
                {
                    "code": "H026",
                    "line": "1:0",
                    "match": "<asdf id",
                    "message": "Empty id and class tags can be removed.",
                },
            ]
        ),
        id="no quotes",
    ),
    pytest.param(
        ('<asdf class="" >'),
        (
            [
                {
                    "code": "H025",
                    "line": "1:0",
                    "match": '<asdf class="" >',
                    "message": "Tag seems to be an orphan.",
                },
                {
                    "code": "H026",
                    "line": "1:0",
                    "match": '<asdf class=""',
                    "message": "Empty id and class tags can be removed.",
                },
            ]
        ),
        id="class",
    ),
    pytest.param(
        ('<asdf {% class="" %}></asdf>'),
        ([]),
        id="class in tag",
    ),
    pytest.param(
        ("<div x-id-y></div><div id-y></div><div x-id></div>"),
        ([]),
        id="prefix and suffix",
    ),
    pytest.param(
        (
            '<div x-id-y=""></div><div id-y=""></div><div x-id=""></div><div data-id=""></div>'
        ),
        ([]),
        id="prefix and suffix quoted",
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
