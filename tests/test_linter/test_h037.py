"""Test twig comment tags.

poetry run pytest tests/test_linter/test_h037.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ('<br class="a" id="asdf" class="b" />'),
        (
            [
                {
                    "code": "H037",
                    "line": "1:4",
                    "match": "class",
                    "message": "Duplicate attribute found.",
                }
            ]
        ),
        id="one",
    ),
    pytest.param(
        ('<div data-class="a" id="asdf" data-class="b"></div>'),
        (
            [
                {
                    "code": "H037",
                    "line": "1:5",
                    "match": "data-class",
                    "message": "Duplicate attribute found.",
                }
            ]
        ),
        id="two",
    ),
    pytest.param(
        ('<div data-class="a" data=asdf class="b"></div>'),
        ([]),
        id="mismatch names",
    ),
    pytest.param(
        ('<svg -width="16" -width="2"></svg>'),
        (
            [
                {
                    "code": "H037",
                    "line": "1:5",
                    "match": "-width",
                    "message": "Duplicate attribute found.",
                }
            ]
        ),
        id="leading hyphen names",
    ),
    pytest.param(
        ('<svg width="16" stroke-width="2"></svg>'),
        ([]),
        id="mismatch hyphen names",
    ),
    pytest.param(
        (
            '<a href="" ></a><a href=""></a><a href=""></a><a href=""></a><a href=""></a><a href=""></a>'
        ),
        ([]),
        id="repeating tags",
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
