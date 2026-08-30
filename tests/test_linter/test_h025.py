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


def test_apostrophe_in_translated_attribute_is_not_an_orphan(
    django_config: Config,
) -> None:
    # The quotes of a template tag nested in an attribute value must not be
    # read as ending the attribute, or the apostrophe in the translated text
    # opens a value that never closes and swallows the rest of the document.
    source = (
        "<div>\n"
        "<p>\n"
        '<a href="#"\n'
        '   title="{% translate "You don\'t have permission" %}">/</a>\n'
        "</p>\n"
        "</div>"
    )
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_multiline_script_is_not_an_orphan(django_config: Config) -> None:
    # https://github.com/djlint/djLint/issues/2302
    # The ignored block covering a <script> body stops at the "<" of its
    # closing tag, so the closer must still pair with the opener.
    source = "<div>\n  <script>\n  var x = 1;\n  </script>\n</div>\n"
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_multiline_style_is_not_an_orphan(django_config: Config) -> None:
    source = "<div>\n  <style>\n  a { color: red; }\n  </style>\n</div>\n"
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_multiline_script_opening_tag_is_not_an_orphan(
    django_config: Config,
) -> None:
    source = (
        "<div>\n"
        '  <script src="a.js"\n'
        '          integrity="sha384-x"\n'
        '          crossorigin="anonymous"></script>\n'
        "</div>\n"
    )
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_multiline_ld_json_script_is_not_an_orphan(
    django_config: Config,
) -> None:
    source = (
        "<div>\n"
        '  <script type="application/ld+json">\n'
        '  {"a": 1}\n'
        "  </script>\n"
        "</div>\n"
    )
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_genuinely_orphan_script_close_is_still_reported(
    django_config: Config,
) -> None:
    source = "<div>\n  </script>\n</div>\n"
    filename = "test.html"
    expected: list[LintError] = [
        {
            "code": "H025",
            "line": "2:2",
            "match": "</script>",
            "message": "Tag seems to be an orphan.",
        }
    ]

    output = linter(django_config, source, filename, filename)

    lint_printer(source, expected, output[filename])
    assert output[filename] == expected


def test_html_inside_multiline_script_is_still_ignored(
    django_config: Config,
) -> None:
    # The <div> in the JS string is not markup and must not pair with, or
    # orphan against, the real tags around it.
    source = '<div>\n  <script>\n  var s = "<div>";\n  </script>\n</div>\n'
    filename = "test.html"

    output = linter(django_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]


def test_nested_jinja_for_else_is_not_an_orphan(jinja_config: Config) -> None:
    # https://github.com/djlint/djLint/issues/2412
    source = (
        "<div>\n"
        "  {% if not thing %}\n"
        "  <div>Message</div>\n"
        "  {% else %}\n"
        "  <div>\n"
        "  {% for item in items %}\n"
        "    <div>{{ item }}</div>\n"
        "  {% else %}\n"
        "    <div>No items!</div>\n"
        "  {% endfor %}\n"
        "  </div>\n"
        "  {% endif %}\n"
        "</div>\n"
    )
    filename = "test.html"

    output = linter(jinja_config, source, filename, filename)

    lint_printer(source, [], output[filename])
    assert not output[filename]
