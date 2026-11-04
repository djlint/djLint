"""Test html picture tag.

uv run pytest tests/test_html/test_tag_picture.py
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
            '<picture><source media="(max-width:640px)"\n'
            'srcset="image.jpg"><img src="image.jpg" alt="image"></picture>\n'
        ),
        (
            "<picture>\n"
            '    <source media="(max-width:640px)" srcset="image.jpg">\n'
            '    <img src="image.jpg" alt="image">\n'
            "</picture>\n"
        ),
        id="picture_source_img_tags",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
