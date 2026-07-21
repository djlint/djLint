"""Test askama profile.

uv run pytest tests/test_askama/test_askama.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/1322
        ('{{ some_macro!("foo", bar = baz)? }}\n'),
        ('{{ some_macro!("foo", bar = baz)? }}\n'),
        id="rust_macro_call_untouched",
    ),
    pytest.param(
        ('{{ some_macro!(\n"foo",\nbar = baz\n)? }}\n'),
        ('{{ some_macro!(\n    "foo",\n    bar = baz\n)? }}\n'),
        id="multiline_macro_indented_but_not_reformatted",
    ),
    pytest.param(
        ('{% if x %}\n<p>{{ foo("bar") }}</p>\n{% endif %}\n'),
        ('{% if x %}\n    <p>{{ foo("bar") }}</p>\n{% endif %}\n'),
        id="jinja_style_blocks_indent",
    ),
    pytest.param(
        ("{# comment #}\n<div>\n<p>x</p>\n</div>\n"),
        ("{# comment #}\n<div>\n    <p>x</p>\n</div>\n"),
        id="template_comments_handled",
    ),
    pytest.param(
        # set is an askama alias for let; 'a' is a rust char literal and
        # ("ab", "cd") is a tuple; neither survives python-style
        # literal formatting
        ('{% set x = \'a\' %}\n{% set y = ("ab", "cd") %}\n'),
        ('{% set x = \'a\' %}\n{% set y = ("ab", "cd") %}\n'),
        id="set_rhs_is_rust_and_untouched",
    ),
    pytest.param(
        ("{% let x = 'a' %}\n"), ("{% let x = 'a' %}\n"), id="let_untouched"
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_formatter(source: str, expected: str) -> None:
    output = formatter(config_builder({"profile": "askama"}), source)

    printer(expected, source, output)
    assert expected == output


def test_profile_defaults() -> None:
    config = Config("dummy/source.html", profile="askama")

    # rust expressions don't survive python-style function formatting
    assert config.no_function_formatting

    # django/flask/nunjucks/handlebars specific rules don't apply to rust
    names = {x["rule"]["name"] for x in config.linter_rules}
    assert "D004" not in names
    assert "D018" not in names
    assert "J004" not in names
    assert "J018" not in names
    # html and generic template rules do
    assert "H005" in names
    assert "T038" in names


def test_other_profiles_keep_function_formatting() -> None:
    assert not Config(
        "dummy/source.html", profile="jinja"
    ).no_function_formatting
