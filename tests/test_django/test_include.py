"""Test django include tag.

poetry run pytest tests/test_django/test_include.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from src.djlint.settings import Config

test_data = [pytest.param(('{% include "this" %}{% include "that" %}'), ('{% include "this" %}\n' '{% include "that" %}\n'), id="include_tag")]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
