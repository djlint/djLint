"""Test form action tags.

poetry run pytest tests/test_linter/test_h033.py
"""
import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("<form action=\" {% url 'foo:bar' %} \" ...>...</form>"),
        (
            [
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action="',
                    "message": "Extra whitespace found in form action.",
                },
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action=" {% ur',
                    "message": "Extra whitespace found in form action.",
                },
            ]
        ),
        id="one",
    ),
    pytest.param(
        ("<form action=\"{% url 'foo:bar' %}\" ...>...</form>"),
        ([]),
        id="one - no error",
    ),
    pytest.param(
        ("<form action=\" {% url 'foo:bar' %} {{ asdf}} \" ...>...</form>"),
        (
            [
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action="',
                    "message": "Extra whitespace found in form action.",
                },
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action=" {% ur',
                    "message": "Extra whitespace found in form action.",
                },
            ]
        ),
        id="two",
    ),
    pytest.param(
        ("<form action=\"{% url 'foo:bar' %} {{ asdf}}\" ...>...</form>"),
        ([]),
        id="two - no error",
    ),
    pytest.param(
        ("<form action=\" {% url 'foo:bar' %} \" ...>...</form>"),
        (
            [
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action="',
                    "message": "Extra whitespace found in form action.",
                },
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action=" {% ur',
                    "message": "Extra whitespace found in form action.",
                },
            ]
        ),
        id="three",
    ),
    pytest.param(
        ('<form action=" {{ asdf}} " ...>...</form>'),
        (
            [
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action="',
                    "message": "Extra whitespace found in form action.",
                },
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action=" {{ as',
                    "message": "Extra whitespace found in form action.",
                },
            ]
        ),
        id="four",
    ),
    pytest.param(
        ("<form action=\"{% url 'foo:bar' %} \" ...>...</form>"),
        (
            [
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action="{% url',
                    "message": "Extra whitespace found in form action.",
                }
            ]
        ),
        id="five",
    ),
    pytest.param(
        ('<form action="asdf " ...>...</form>'),
        (
            [
                {
                    "code": "H033",
                    "line": "1:0",
                    "match": '<form action="asdf "',
                    "message": "Extra whitespace found in form action.",
                }
            ]
        ),
        id="six",
    ),
    pytest.param(
        ('<form action="asdf" ...>...</form>'),
        ([]),
        id="six - no error",
    ),
    pytest.param(
        (
            '<form action="#"\n'
            '    method="get"\n'
            '    data-action="\n'
            "        submit:my-custom-element#handleFormSubmit\n"
            "        click:my-custom-element#handleClick\n"
            '        some-event:my-custom-element#handleSomething" >\n'
            "    <!-- some content -->\n"
            "</form>"
        ),
        ([]),
        id="gh pr #743",
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
