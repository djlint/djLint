"""Test that a run of unclosed template tags is read once.

uv run pytest tests/test_unclosed_template_tags.py
"""

from __future__ import annotations

import time

import pytest

from djlint.lint import linter
from djlint.reformat import formatter
from djlint.settings import Config

# Each of these was read again from every opener in it, to the end of the
# line or the file: linting or formatting the first or the last took over
# half a minute, and linting the second fourteen seconds.
sources = [
    pytest.param("<div>" + "{{ " * 8000 + "</div>{# c #}", id="variables"),
    pytest.param("<div>" + "{% " * 4000 + "</div>{# c #}", id="blocks"),
    pytest.param(
        '<a href="/x"><input type="' + "{{" * 8000 + '" name="q"></a>',
        id="a brace run in a value",
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
