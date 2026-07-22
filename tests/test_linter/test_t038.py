"""Test unclosed template block tags.

uv run pytest tests/test_linter/test_t038.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from djlint.settings import Config
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.types import LintError

django_test_data = [
    pytest.param(
        ("{% if x %}\n<p>hello</p>\n"),
        ([
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% if x %}",
                "message": "Block tag has no matching end tag.",
            }
        ]),
        id="unclosed_if",
    ),
    pytest.param(
        ("{% if x %}\n<p>hello</p>\n{% endif %}\n"), ([]), id="closed_if"
    ),
    pytest.param(
        ("<p>hello</p>\n{% endfor %}\n"),
        ([
            {
                "code": "T038",
                "line": "2:0",
                "match": "{% endfor %}",
                "message": "End tag has no matching block tag.",
            }
        ]),
        id="orphan_endfor",
    ),
    pytest.param(
        ("{% if x %}{% for y in z %}{% endif %}\n"),
        ([
            {
                "code": "T038",
                "line": "1:10",
                "match": "{% for y in z %}",
                "message": "Block tag has no matching end tag.",
            }
        ]),
        id="crossed_blocks",
    ),
    pytest.param(
        ("{% block a %}\n<p>hello</p>\n"),
        ([
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% block a %}",
                "message": "Block tag has no matching end tag.",
            }
        ]),
        id="unclosed_block",
    ),
    pytest.param(
        ("{% block a %}\n<p>hello</p>\n{% endblock b %}\n"),
        ([
            {
                "code": "T038",
                "line": "3:0",
                "match": "{% endblock b %}",
                "message": "Endblock name should match opening block name.",
            }
        ]),
        id="mismatched_endblock_name",
    ),
    pytest.param(
        ("{% block a %}\n<p>hello</p>\n{% endblock a %}\n"),
        ([]),
        id="named_endblock_matches",
    ),
    pytest.param(
        ("{% verbatim %}\n{% if x %}\n{% endverbatim %}\n"),
        ([]),
        id="inside_verbatim",
    ),
    pytest.param(
        ("{% if a %}\n{% if b %}\n{% endif %}\n{% endif %}\n"),
        ([]),
        id="nested_closed",
    ),
    pytest.param(
        ('{% url "home" %}\n{% include "a.html" %}\n'), ([]), id="single_tags"
    ),
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


jinja_test_data = [
    pytest.param(
        ("{% set x = 1 %}\n"), ([]), id="set_assignment_is_not_a_block"
    ),
    pytest.param(
        ("{% raw %}\n{% if x %}\n{% endraw %}\n"), ([]), id="inside_raw"
    ),
    pytest.param(
        ("{% set x %}\ncontent\n{% endset %}\n"), ([]), id="set_block_closed"
    ),
    pytest.param(
        ('{% macro input(name) %}\n<input name="{{ name }}">\n'),
        ([
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% macro input(name)",
                "message": "Block tag has no matching end tag.",
            }
        ]),
        id="unclosed_macro",
    ),
]


@pytest.mark.parametrize(("source", "expected"), jinja_test_data)
def test_jinja(
    source: str, expected: list[LintError], jinja_config: Config
) -> None:
    filename = "test.html"
    output = linter(jinja_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch


handlebars_test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/202
        ("{{#if asdf}}\n    {{ jkl }}\n"),
        ([
            {
                "code": "T038",
                "line": "1:0",
                "match": "{{#if asdf}}",
                "message": "Block tag has no matching end tag.",
            }
        ]),
        id="issue_202_unclosed_if",
    ),
    pytest.param(
        ("{{#if asdf}}\n    {{ jkl }}\n{{/if}}\n"), ([]), id="closed_if"
    ),
    pytest.param(
        ("{{#each items}}\n    {{ this }}\n{{/each}}\n"), ([]), id="each"
    ),
    pytest.param(
        ("{{^person}}\n    none\n{{/person}}\n"), ([]), id="inverted_section"
    ),
    pytest.param(
        ("{{#custom}}\n    {{ this }}\n{{/custom}}\n"),
        ([]),
        id="custom_section",
    ),
    pytest.param(
        ("{{ jkl }}\n{{/if}}\n"),
        ([
            {
                "code": "T038",
                "line": "2:0",
                "match": "{{/if}}",
                "message": "End tag has no matching block tag.",
            }
        ]),
        id="orphan_close",
    ),
    pytest.param(
        ("{{!-- {{#if x}} --}}\n"), ([]), id="block_tag_inside_comment"
    ),
    pytest.param(
        ("{{! {{#if x}} }}\n"), ([]), id="block_tag_inside_inline_comment"
    ),
    pytest.param(("{{{{raw}}}}{{{{/raw}}}}\n"), ([]), id="raw_block"),
    pytest.param(
        ("{{{{raw}}}}{{#if x}}{{{{/raw}}}}\n"),
        ([]),
        id="raw_block_with_content",
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


custom_blocks_test_data = [
    pytest.param(
        ("{% component 'calendar' %}\n<p>hello</p>\n"),
        ([
            {
                "code": "T038",
                "line": "1:0",
                "match": "{% component 'calend",
                "message": "Block tag has no matching end tag.",
            }
        ]),
        id="unclosed_custom_block",
    ),
    pytest.param(
        ('{% component "calendar" date="2015-06-19" / %}\n<p>hello</p>\n'),
        ([]),
        id="self_closing_custom_block",
    ),
    pytest.param(
        ('{% component "calendar" %}\n<p>hello</p>\n{% endcomponent %}\n'),
        ([]),
        id="closed_custom_block",
    ),
]


@pytest.mark.parametrize(("source", "expected"), custom_blocks_test_data)
def test_custom_blocks(source: str, expected: list[LintError]) -> None:
    config = Config(
        "dummy/source.html", profile="django", custom_blocks="component"
    )
    filename = "test.html"
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
