"""Test that a mako code block is left as written.

uv run pytest tests/test_html/test_mako_code_block.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.reformat import formatter
from tests.conftest import config_builder, printer

format_data = [
    pytest.param(
        "<ul>\n"
        "  <li>\n"
        "    <%\n"
        "      if is_unit:\n"
        '          name = "unit"\n'
        "    %>\n"
        "    <span>x</span>\n"
        "  </li>\n"
        "</ul>\n",
        "<ul>\n"
        "    <li>\n"
        "        <%\n"
        "      if is_unit:\n"
        '          name = "unit"\n'
        "    %>\n"
        "        <span>x</span>\n"
        "    </li>\n"
        "</ul>\n",
        id="python keeps its own indentation",
    ),
    pytest.param(
        "<div>\n    <%!\n    from a import b\n    %>\n</div>\n",
        "<div>\n    <%!\n    from a import b\n    %>\n</div>\n",
        id="a module level block is left alone too",
    ),
    pytest.param(
        '<%def name="f()"><div><span>x</span></div></%def>\n',
        '<%def name="f()">\n<div><span>x</span></div>\n</%def>\n',
        id="a def body is markup and is still put on its own line",
    ),
]


@pytest.mark.parametrize(("source", "expected"), format_data)
def test_mako_code_block_formatting(source: str, expected: str) -> None:
    config = config_builder({"profile": "django", "indent": 4})

    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
    assert formatter(config, output) == output


lint_data = [
    pytest.param(
        "<ul>\n  <%\n    link = HTML(u\"<a href='{}'>\").format(x)\n  %>\n</ul>\n",
        (False),
        id="a tag in a python string is not markup",
    ),
    pytest.param(
        "<div>\n  <%\n    x = 1\n  %>\n  {{date}}\n</div>\n",
        (True),
        id="markup beside the block is still linted",
    ),
]


@pytest.mark.parametrize(("source", "reported"), lint_data)
def test_mako_code_block_linting(source: str, reported: bool) -> None:
    config = config_builder({"profile": "django"})
    filename = "test.html"

    findings = linter(config, source, filename, filename)[filename]

    assert bool(findings) is reported
