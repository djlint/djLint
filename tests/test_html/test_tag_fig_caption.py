"""Test html figure tag.

uv run pytest tests/test_html/test_tag_fig_caption.py
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
            '<figure><img src="" alt=""><figcaption>caption</figcaption></figure>'
        ),
        (
            "<figure>\n"
            '    <img src="" alt="">\n'
            "    <figcaption>caption</figcaption>\n"
            "</figure>\n"
        ),
        id="figure_figcaption_tags",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
