"""Test django with tag.

uv run pytest tests/test_django/test_with.py
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
            "{% with total=business.employees.count %}{{ total }}<div>employee</div>{{ total|pluralize }}{% endwith %}"
        ),
        (
            "{% with total=business.employees.count %}\n"
            "    {{ total }}\n"
            "    <div>employee</div>\n"
            "    {{ total|pluralize }}\n"
            "{% endwith %}\n"
        ),
        id="with_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
