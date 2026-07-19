"""Test jinja trans tags.

uv run pytest tests/test_jinja/test_trans.py
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
        (
            "<div>\n"
            "    {% trans %}\n"
            "    <p>content</p>\n"
            "    {% endtrans %}\n"
            "</div>"
        ),
        (
            "<div>\n"
            "    {% trans %}\n"
            "    <p>content</p>\n"
            "    {% endtrans %}\n"
            "</div>\n"
        ),
        id="endtrans_keeps_indent_level",
    ),
    pytest.param(
        (
            "<section>\n"
            "    <div>\n"
            "        {% trans count=counter %}\n"
            "        text here\n"
            "        {% endtrans %}\n"
            "    </div>\n"
            "    <p>after</p>\n"
            "</section>"
        ),
        (
            "<section>\n"
            "    <div>\n"
            "        {% trans count=counter %}\n"
            "        text here\n"
            "        {% endtrans %}\n"
            "    </div>\n"
            "    <p>after</p>\n"
            "</section>\n"
        ),
        id="endtrans_does_not_shift_following_tags",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
