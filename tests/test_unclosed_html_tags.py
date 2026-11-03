"""Test that a run of html tags left open is read once.

uv run pytest tests/test_unclosed_html_tags.py
"""

from __future__ import annotations

import time

import pytest

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import linter

# Each tag, or each body of a raw text element, was read up to the end of
# the file again from every tag after it. A line that opens a tag is indented
# a level deeper than the one before, so the output of the first ones grows
# with the square of their count; reading it again from each tag took minutes
# or ran out of memory.
sources = [
    pytest.param("<p\n" * 1500, id="tags never ended"),
    pytest.param('<p data-x="a\n' * 1000, id="tags each opening a value"),
    pytest.param("<li>a\n" * 1500, id="elements never closed"),
    pytest.param('<p>"\n' * 2000, id="elements each holding a quote"),
    pytest.param("<p {% if a %}\n" * 1500, id="tags each holding a template tag"),
    pytest.param('<p x="a">b</p\n' * 4000, id="closing tags never ended"),
    pytest.param("<script>\n" * 4000, id="scripts never closed"),
    pytest.param('<script data-x="a\n' * 4000, id="script tags each opening a value"),
    pytest.param("<style>\n" * 4000, id="styles never closed"),
    pytest.param("<textarea>\n" * 4000, id="textareas never closed"),
    pytest.param("<!-- a\n" * 20000, id="comments never closed"),
    pytest.param("</p\n" * 20000, id="closing tags with no > after them"),
    pytest.param('</p x="a\n' * 20000, id="closing tags each opening a value"),
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
    config = Config("test.html", profile="jinja", format_css=True, format_js=True)

    started = time.perf_counter()
    formatter(config, source)

    assert time.perf_counter() - started < 5


def test_a_closing_tag_runs_to_its_gt() -> None:
    """As browsers read it, the "<p" after `</p` is junk inside the closing tag.

    Read as a tag of its own, each paragraph was nested in the one before, so
    the output grew with the square of their count.
    """
    config = Config("test.html", profile="jinja")
    source = '<p x="a">b</p\n' * 4

    output = formatter(config, source)

    assert output.startswith('<p x="a">b</p <p x="a">\n')
    assert len(output) < 2 * len(source)
    assert formatter(config, output) == output
