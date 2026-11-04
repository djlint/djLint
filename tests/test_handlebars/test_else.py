"""Test handlebars else tag.

uv run pytest tests/test_handlebars/test_else.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [pytest.param(("{{^}}"), ("{{^}}\n"), id="else_tag")]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, handlebars_config: Config) -> None:
    output = formatter(handlebars_config, source)

    printer(expected, source, output)
    assert expected == output
