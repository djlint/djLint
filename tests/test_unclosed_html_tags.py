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
