"""Test the attribute values the formatter rewrites.

uv run pytest tests/test_html/test_attribute_values.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        '<form method="POST" action="/"></form>\n',
        '<form method="post" action="/">\n</form>\n',
        id="form method is lowercased",
    ),
    pytest.param(
        (
            '<script type="text/javascript"></script>\n'
            '<style type="text/css"></style>\n'
            '<link type="text/css" rel="stylesheet" href="a.css">\n'
        ),
        (
            "<script></script>\n"
            "<style></style>\n"
            '<link rel="stylesheet" href="a.css">\n'
        ),
        id="default types are dropped",
    ),
    pytest.param(
        '<script type="module"></script>\n',
        '<script type="module"></script>\n',
        id="a type that means something is kept",
    ),
    pytest.param(
        '<pre><form method="POST"><script type="text/javascript"></pre>\n',
        '<pre><form method="POST"><script type="text/javascript"></pre>\n',
        id="verbatim content is left alone",
    ),
    pytest.param(
        (
            '{% include "a.html" with s=\'<form method="POST">\' %}\n'
            '{% include "b.html" with t=\'<script type="text/javascript">\' %}\n'
        ),
        (
            '{% include "a.html" with s=\'<form method="POST">\' %}\n'
            '{% include "b.html" with t=\'<script type="text/javascript">\' %}\n'
        ),
        id="a tag written inside a template tag is left alone",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
