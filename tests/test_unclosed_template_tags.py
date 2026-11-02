"""Test that a run of unclosed template tags is read once.

uv run pytest tests/test_unclosed_template_tags.py
"""

from __future__ import annotations

import time

import pytest

from djlint.formatter.class_attributes import encode_template_string_newlines
from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import linter

# Each of these was read again from every opener in it, to the end of the
# line or the file: linting or formatting the first or the last took over
# half a minute, and linting the second fourteen seconds.
sources = [
    pytest.param("<div>" + "{{ " * 8000 + "</div>{# c #}", id="variables"),
    pytest.param("<div>" + "{% " * 4000 + "</div>{# c #}", id="blocks"),
    pytest.param(
        '<a href="/x"><input type="' + "{{" * 8000 + '" name="q"></a>', id="a brace run in a value"
    ),
]


@pytest.mark.parametrize("source", sources)
def test_lint(source: str) -> None:
    filename = "test.html"
    config = Config(filename, profile="jinja")

    started = time.perf_counter()
    linter(config, source, filename, filename)

    assert time.perf_counter() - started < 5


@pytest.mark.parametrize("source", sources)
def test_format(source: str) -> None:
    config = Config("test.html", profile="jinja")

    started = time.perf_counter()
    formatter(config, source)

    assert time.perf_counter() - started < 5


# A quote left open in a tag must not send each later one to the end of the
# file looking for its partner. An escaped quote is the one that would: each
# of `\"\"\"` read as opening a string ran to the end of the tag.
open_quotes = [
    pytest.param("<p>\n" + '{% "\n' * 20000 + "%}", id="block tags each opening a string"),
    pytest.param("<p>\n" + "{{ 'a\n" * 20000 + "}}", id="variables each opening a string"),
    pytest.param("{% x " + '\\"\n' * 40000 + "%}", id="escaped quotes in one tag"),
    pytest.param("{% x " + '"\n\\' * 40000 + "%}", id="quotes before escapes in one tag"),
    pytest.param('{% "\n' + "a\n" * 100000, id="one string never closed"),
    pytest.param("{% " + "\"'\n" * 40000 + "%}", id="both quotes in one tag"),
]


@pytest.mark.parametrize("source", open_quotes)
def test_strings_across_lines_are_found_in_linear_time(source: str) -> None:
    started = time.perf_counter()
    encode_template_string_newlines(source)

    assert time.perf_counter() - started < 1
