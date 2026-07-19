"""Test empty or missing template names in extends/include tags.

uv run pytest tests/test_linter/test_t040.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.settings import Config
    from djlint.types import LintError

test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/722
        ('{% extends "" %}\n'),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": '{% extends ""',
                "message": "Missing or empty template name in extends or include tag.",
            }
        ]),
        id="empty_extends",
    ),
    pytest.param(
        ("{% include '' %}\n"),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": "{% include ''",
                "message": "Missing or empty template name in extends or include tag.",
            },
            {
                "code": "T002",
                "line": "1:0",
                "match": "{% include '' %}",
                "message": "Double quotes should be used in tags.",
            },
        ]),
        id="empty_include_single_quotes",
    ),
    pytest.param(
        ("{% extends %}\n"),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": "{% extends %}",
                "message": "Missing or empty template name in extends or include tag.",
            }
        ]),
        id="bare_extends",
    ),
    pytest.param(
        ("{%- include -%}\n"),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": "{%- include -%}",
                "message": "Missing or empty template name in extends or include tag.",
            }
        ]),
        id="bare_include_whitespace_control",
    ),
    pytest.param(
        ('{% extends " " %}\n'),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": '{% extends " "',
                "message": "Missing or empty template name in extends or include tag.",
            }
        ]),
        id="whitespace_only_name",
    ),
    pytest.param(
        ("{%\tinclude\t%}\n"),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": "{%\tinclude\t%}",
                "message": "Missing or empty template name in extends or include tag.",
            }
        ]),
        id="bare_include_tabs",
    ),
    pytest.param(
        ('{% include"" %}\n'),
        ([
            {
                "code": "T040",
                "line": "1:0",
                "match": '{% include""',
                "message": "Missing or empty template name in extends or include tag.",
            }
        ]),
        id="empty_include_no_space",
    ),
    pytest.param(('{% extends "base.html" %}\n'), ([]), id="named_extends"),
    pytest.param(("{% extends base_var %}\n"), ([]), id="variable_extends"),
    pytest.param(
        ('{% include "partial.html" with x=1 %}\n'), ([]), id="named_include"
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(
    source: str, expected: list[LintError], django_config: Config
) -> None:
    filename = "test.html"
    output = linter(django_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
