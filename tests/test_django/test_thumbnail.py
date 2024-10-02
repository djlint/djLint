"""Test jazzband sorl-thumbnail tag.

https://github.com/jazzband/sorl-thumbnail

uv run pytest tests/test_django/test_thumbnail.py
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
            '{% thumbnail person.profile_photo "200x200" crop="center" as im %}\n'
            '   <img src="{{ im.url }}"\n'
            '        width="{{ im.width }}"\n'
            '          height="{{ im.height }}"\n'
            '         class="img-thumbnail"\n'
            '         alt="{{ person.name }}">\n'
            "{% endthumbnail %}\n"
        ),
        (
            '{% thumbnail person.profile_photo "200x200" crop="center" as im %}\n'
            '    <img src="{{ im.url }}"\n'
            '         width="{{ im.width }}"\n'
            '         height="{{ im.height }}"\n'
            '         class="img-thumbnail"\n'
            '         alt="{{ person.name }}">\n'
            "{% endthumbnail %}\n"
        ),
        id="thumbnail",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
