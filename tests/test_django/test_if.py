"""Test django if tag.

uv run pytest tests/test_django/test_if.py
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
            "{% if athlete_list %}Number of athletes: {{ athlete_list|length }}{% elif athlete_in_locker_room_list %}Athletes should be out of the locker room soon!{% else %}No athletes.{% endif %}"
        ),
        (
            "{% if athlete_list %}\n"
            "    Number of athletes: {{ athlete_list|length }}\n"
            "{% elif athlete_in_locker_room_list %}\n"
            "    Athletes should be out of the locker room soon!\n"
            "{% else %}\n"
            "    No athletes.\n"
            "{% endif %}\n"
        ),
        id="if_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
