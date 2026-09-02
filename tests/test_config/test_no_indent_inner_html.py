"""Test no_indent_inner_html.

uv run pytest tests/test_config/test_no_indent_inner_html.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

_DOCUMENT = "<html><head><title>t</title></head><body><p>x</p></body></html>\n"

test_data = [
    pytest.param(
        _DOCUMENT,
        (
            "<html>\n"
            "<head>\n"
            "    <title>t</title>\n"
            "</head>\n"
            "<body>\n"
            "    <p>x</p>\n"
            "</body>\n"
            "</html>\n"
        ),
        id="head and body sit level with html",
    ),
    pytest.param(
        "<div><html><head></head></html></div>\n",
        "<div>\n    <html>\n    <head></head>\n    </html>\n</div>\n",
        id="html itself still sits where its parent puts it",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str) -> None:
    config = config_builder({"no_indent_inner_html": True})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output


def test_default_indents_below_html() -> None:
    output = formatter(config_builder({}), _DOCUMENT)

    assert output == (
        "<html>\n"
        "    <head>\n"
        "        <title>t</title>\n"
        "    </head>\n"
        "    <body>\n"
        "        <p>x</p>\n"
        "    </body>\n"
        "</html>\n"
    )
