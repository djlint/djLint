"""Test django autoescape tag.

uv run pytest tests/test_django/test_autoescape.py
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
        ("{% autoescape on %}{{ body }}{% endautoescape %}"),
        ("{% autoescape on %}{{ body }}{% endautoescape %}\n"),
        id="autoescape_tag",
    ),
    pytest.param(
        ("<p>\n    {% autoescape on %}Something{% endautoescape %}\n    <span>Test</span>\n</p>\n"),
        ("<p>\n    {% autoescape on %}Something{% endautoescape %}\n    <span>Test</span>\n</p>\n"),
        id="issue_2411_siblings_keep_their_level",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
