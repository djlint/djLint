"""Test html inside template tags for tag.

uv run pytest tests/test_django/test_html_tags_in_template_tag.py
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
        ("{{ some_val | default:'some_comment1<br>some_comment2' }}"),
        ("{{ some_val | default:'some_comment1<br>some_comment2' }}\n"),
        id="test",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
