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
            "{% filter force_escape|lower %}This text will be HTML-escaped, and will appear in all lowercase.{% endfilter %}\n"
        ),
        id="filter_tag",
    ),
    pytest.param(
        (
            "{% filter capfirst %}{% blocktrans %}dear {{ name }}{% endblocktrans %}{% endfilter %},\n"
            "\n"
            "How are you?"
        ),
        (
            "{% filter capfirst %}{% blocktrans %}dear {{ name }}{% endblocktrans %}{% endfilter %},\n"
            "How are you?\n"
        ),
        id="issue_165_inline_filter",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
