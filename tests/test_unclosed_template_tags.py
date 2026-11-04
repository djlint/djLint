"""Test that a run of unclosed template tags is read once.

uv run pytest tests/test_unclosed_template_tags.py
"""

from __future__ import annotations

import time

import pytest

from djlint._formatter.class_attributes import (
    encode_template_string_newlines,
    multiline_template_tag_spans,
)
from djlint._reformat import formatter
from djlint._settings import Config
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
    # Each line opens a tag left open, so each is indented one level deeper
    # than the last; reading every run of that indentation from each of its
    # spaces, or each tag to the end of the file, took 45 seconds for the
    # first and nearly seven minutes for the second.
    pytest.param("<p>\n" + "{{ 'a\n" * 400 + "</p>", id="lines each opening a variable"),
    pytest.param("<p>\n" + "{% set a = 'a\n" * 400 + "</p>", id="lines each opening a set"),
    pytest.param("<p>\n" + "{{ f('a\n" * 400 + "</p>", id="lines each opening a call"),
    pytest.param("<p>\n" + "{% include 'a\n" * 2000 + "</p>", id="lines each opening an include"),
    # `{%a%}` reads both as a template tag and as a braced run, and trying
    # the other reading of each made an opening tag never ended quadratic.
    pytest.param("<script " + "{%a%}" * 8000 + ">x", id="a script tag of tags never closed"),
    pytest.param("<form " + "{#a#}" * 8000 + " x>", id="a form tag of comments"),
    pytest.param("<b " + "{%a%}" * 8000 + ">x", id="an inline tag of tags never closed"),
    pytest.param("<img " + "{%a%}" * 8000 + ">x", id="an img tag of tags"),
    pytest.param("<html " + "{%a%}" * 8000 + ">x", id="an html tag of tags"),
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
# of `\"\"\"` read as opening a string ran to the end of the tag. A string may
# hold an opener, so the ones that hide each next tag are here too.
open_quotes = [
    pytest.param('{% "{%\n' * 20000 + "%}", id="strings each holding the next opener"),
    pytest.param("{% '\n" + "{% x\n" * 40000 + "'%}", id="one string holding many tags"),
    pytest.param(("{% '\n" + '{% "" \n' * 50) * 400 + "%}", id="odd and even runs of quotes"),
    pytest.param("".join("{% '\n" if i % 2 else '{% "\n' for i in range(20000)), id="kinds"),
    pytest.param('\\{% "\n' * 20000 + "%}", id="escapes before openers"),
    pytest.param('{# "\n' * 20000 + "#}", id="comments never closed"),
    pytest.param("{% comment %}'\n" * 20000 + "{% endcomment %}", id="comment blocks never ended"),
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


# A mako expression is read up to the brace that balances its own, so one
# left open must not send each later one to the end of the file either.
open_expressions = [
    pytest.param("<p>\n" + "${ f('a\n" * 20000, id="expressions each opening a string"),
    pytest.param("${ " + "{\n" * 20000, id="braces never closed"),
    pytest.param("${ {\n" * 2000 + "}", id="expressions nested in braces never closed"),
]


@pytest.mark.parametrize("source", open_expressions)
def test_tags_across_lines_are_found_in_linear_time(source: str) -> None:
    started = time.perf_counter()
    multiline_template_tag_spans(source)

    assert time.perf_counter() - started < 1
