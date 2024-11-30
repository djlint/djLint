"""Test template tag special django-components syntax.

uv run pytest tests/test_django/test_django_components.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing import Any

test_data = [
    pytest.param(
        ('{% component "icon" name="save" /%}\nHello World\n'),
        ('{% component "icon" name="save" / %}\nHello World\n'),
        ({"custom_blocks": "component"}),
        id="self_closing_tag",
    )
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
