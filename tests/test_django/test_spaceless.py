"""Test django spaceless tag.

poetry run pytest tests/test_django/test_spaceless.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from src.djlint.settings import Config

test_data = [
    pytest.param(
        ('{% spaceless %}<p><a href="foo/">Foo</a></p>{% endspaceless %}'),
        (
            "{% spaceless %}\n"
            "    <p>\n"
            '        <a href="foo/">Foo</a>\n'
            "    </p>\n"
            "{% endspaceless %}\n"
        ),
        id="spaceless_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
