"""Test H025 orphan tag tokenizer regressions.

uv run pytest tests/test_linter/test_h025.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.lint import linter
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.settings import Config
    from djlint.types import LintError


def test_stray_html_comment_in_template_comment_is_not_an_orphan(
    django_config: Config,
) -> None:
    # A stray "<!--" inside a {# #} template comment must not swallow the
    # closing tag and turn a balanced element into a false H025 orphan.
    source = "<div>\n{# <!-- #}\n</div>"
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_genuine_orphan_after_template_comment_is_still_reported(
    django_config: Config,
) -> None:
    source = "{# <!-- #}\n<div>"
    filename = "test.html"
    expected: list[LintError] = [
        {
            "code": "H025",
            "line": "2:0",
            "match": "<div>",
            "message": "Tag seems to be an orphan.",
        }
    ]

    output = linter(django_config, source, filename, filename)

    lint_printer(source, expected, output[filename])
    assert output[filename] == expected


def test_stray_html_comment_in_raw_text_element_is_not_an_orphan(
    basic_config: Config,
) -> None:
    source = "<div>\n<textarea><!--</textarea>\n</div>"
    filename = "test.html"

    output = linter(basic_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_triple_stache_attribute_is_not_an_orphan(
    handlebars_config: Config,
) -> None:
    source = "<a {{{u}}}></a>"
    filename = "test.html"

    output = linter(handlebars_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]
