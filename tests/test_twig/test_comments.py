"""Test twig comment tags.

uv run pytest tests/test_twig/test_comments.py
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
        ("{% if %}\n    {#\n        line\n    #}\n{% endif %}"),
        ("{% if %}\n    {#\n        line\n    #}\n{% endif %}\n"),
        id="comments",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {#\n"
            "    multi\n"
            "    line\n"
            "    comment\n"
            "    #}\n"
            "</div>\n"
            "<div>\n"
            "    <p></p>\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    {#\n"
            "    multi\n"
            "    line\n"
            "    comment\n"
            "    #}\n"
            "</div>\n"
            "<div>\n"
            "    <p></p>\n"
            "</div>\n"
        ),
        id="comments",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, nunjucks_config: Config) -> None:
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
