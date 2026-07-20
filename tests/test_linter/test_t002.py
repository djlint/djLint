"""Test double quote style in template tags (opt-in rule).

uv run pytest tests/test_linter/test_t002.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from djlint.settings import Config
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.types import LintError

test_data = [
    pytest.param(
        ("{% extends 'this' %}"),
        ([
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% extends 'this' %}",
                "message": "Double quotes should be used in tags.",
            }
        ]),
        id="T002",
    ),
    pytest.param(("{% extends this %}"), ([]), id="unquoted_var_names"),
    pytest.param(
        ("{% with a='this' %}"),
        ([
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% with a='this' %}",
                "message": "Double quotes should be used in tags.",
            },
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% with a='this' %}",
                "message": "Block tag has no matching end tag.",
            },
        ]),
        id="with",
    ),
    pytest.param(
        ("{% trans 'this' %}"),
        ([
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% trans 'this' %}",
                "message": "Double quotes should be used in tags.",
            }
        ]),
        id="trans",
    ),
    pytest.param(
        ("{% translate 'this' %}"),
        ([
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% translate 'this' ",
                "message": "Double quotes should be used in tags.",
            }
        ]),
        id="translate",
    ),
    pytest.param(
        ("<span title=\"{% translate 'this' %}\"></span>"),
        ([]),
        id="translate_in_attribute",
    ),
    pytest.param(
        ("{% include 'this' %}"),
        ([
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% include 'this' %}",
                "message": "Double quotes should be used in tags.",
            }
        ]),
        id="include",
    ),
    pytest.param(
        ("{% now 'Y-m-d G:i:s' %}"),
        ([
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% now 'Y-m-d G:i:s'",
                "message": "Double quotes should be used in tags.",
            }
        ]),
        id="now",
    ),
    pytest.param(
        (
            '{% extends "layout.h" %}\n'
            '<div class="card" data-list=\'{"name": "blah"}\'>\n'
            '{% include "template.html" %}\n'
            "<div {% for %} data-{{ name }}='{{ value }}'{% endfor %}/>"
        ),
        ([
            {
                "code": "H025",
                "line": "2:0",
                "match": '<div class="card" da',
                "message": "Tag seems to be an orphan.",
            }
        ]),
        id="test_greedy_regex",
    ),
    pytest.param(
        ("{% if form.action_url %}\n   ='stuff'\n {% endif %}"),
        ([]),
        id="test_greedy_regex_2",
    ),
    pytest.param(
        (
            '{% include "template.html" %}\n'
            " {% include \"template.html\" with type='mono' %}"
        ),
        ([
            {
                "code": "T002",
                "line": "2:1",
                "match": '{% include "template',
                "message": "Double quotes should be used in tags.",
            }
        ]),
        id="test_line_num",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: list[LintError]) -> None:
    config = Config("dummy/source.html", profile="django", include="T002")
    filename = "test.html"
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
