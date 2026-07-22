"""Test unclosed template tags.

uv run pytest tests/test_linter/test_t039.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.settings import Config
    from djlint.types import LintError

django_test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/705
        ("{% url 'journal:user_tag_list\" user.url }}\n"),
        ([
            {
                "code": "T039",
                "line": "1:0",
                "match": "{% url 'journal:user",
                "message": "Unclosed template tag found.",
            }
        ]),
        id="issue_705_unclosed_quote_and_wrong_delimiter",
    ),
    pytest.param(
        ('{% url "home" }}\n'),
        ([
            {
                "code": "T039",
                "line": "1:0",
                "match": '{% url "home" }}',
                "message": "Unclosed template tag found.",
            }
        ]),
        id="block_tag_closed_by_variable_delimiter",
    ),
    pytest.param(
        ("<p>{{ user.name }</p>\n"),
        ([
            {
                "code": "T039",
                "line": "1:3",
                "match": "{{ user.name }</p>",
                "message": "Unclosed template tag found.",
            }
        ]),
        id="variable_missing_a_brace",
    ),
    pytest.param(
        ("{% if x %\n{% endif %}\n"),
        ([
            {
                "code": "T039",
                "line": "1:0",
                "match": "{% if x %\n{%",
                "message": "Unclosed template tag found.",
            },
            # T038 sees one garbled tag spanning to the endif's %} and
            # reports the if block as unclosed too
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% if x %\n{% endif %",
                "message": "Block tag has no matching end tag.",
            },
        ]),
        id="tag_open_before_close",
    ),
    pytest.param(
        ('{% url "home" %}\n{{ user.name }}\n'), ([]), id="closed_tags"
    ),
    pytest.param(('{% trans "a}b" %}\n'), ([]), id="brace_inside_string"),
    pytest.param(
        ("{% verbatim %}\n{% broken\n{% endverbatim %}\n"),
        ([]),
        id="inside_verbatim",
    ),
    pytest.param(("<p>plain</p>\n"), ([]), id="no_template_syntax"),
]


@pytest.mark.parametrize(("source", "expected"), django_test_data)
def test_django(
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


handlebars_test_data = [
    pytest.param(
        ("{{!-- {{ note --}}\n{{ name }}\n"), ([]), id="comment_tags_skipped"
    ),
    pytest.param(("{{#if a}}\n{{ b }}\n{{/if}}\n"), ([]), id="closed_tags"),
    pytest.param(("{{{{raw}}}}{{{{/raw}}}}\n"), ([]), id="raw_block"),
    pytest.param(
        ("{{{{raw}}}}{{#if x}}{{/if}}{{{{/raw}}}}\n"),
        ([]),
        id="raw_block_with_content",
    ),
    pytest.param(
        ("{{#if a}\n"),
        ([
            {
                "code": "T039",
                "line": "1:0",
                "match": "{{#if a}",
                "message": "Unclosed template tag found.",
            }
        ]),
        id="unclosed_section_open",
    ),
]


@pytest.mark.parametrize(("source", "expected"), handlebars_test_data)
def test_handlebars(
    source: str, expected: list[LintError], handlebars_config: Config
) -> None:
    filename = "test.html"
    output = linter(handlebars_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
