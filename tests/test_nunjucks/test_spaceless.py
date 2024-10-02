"""Test nunjucks spaceless tag.

uv run pytest tests/test_nunjucks/test_spaceless.py
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
        ("{%- if entry.children.length -%}<strong>{%- endif -%}"),
        ("{%- if entry.children.length -%}<strong>{%- endif -%}\n"),
        id="spaceless_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, nunjucks_config: Config) -> None:
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
