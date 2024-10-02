"""Test django filter tag.

uv run pytest tests/test_django/test_filter.py
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
            "{% filter force_escape|lower %}This text will be HTML-escaped, and will appear in all lowercase.{% endfilter %}"
        ),
        (
            "{% filter force_escape|lower %}\n"
            "    This text will be HTML-escaped, and will appear in all lowercase.\n"
            "{% endfilter %}\n"
        ),
        id="filter_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
