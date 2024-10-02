"""Test django asset tag.

uv run pytest tests/test_django/test_asset.py
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
            '{% block css %}{% assets "css_error" %}<link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />{% endassets %}{% endblock css %}'
        ),
        (
            "{% block css %}\n"
            '    {% assets "css_error" %}\n'
            '        <link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />\n'
            "    {% endassets %}\n"
            "{% endblock css %}\n"
        ),
        id="asset_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
