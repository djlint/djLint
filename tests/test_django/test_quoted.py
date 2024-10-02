"""Test django quoted tags.

uv run pytest tests/test_django/test_quoted.py
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
            "<h1>\n"
            '    {% if condition1 %}<span class="cls"></span>{% endif %}\n'
            ' {% if condition2 %}"{{ text }}"{% endif %}\n'
            "     </h1>\n"
        ),
        (
            "<h1>\n"
            '    {% if condition1 %}<span class="cls"></span>{% endif %}\n'
            '    {% if condition2 %}"{{ text }}"{% endif %}\n'
            "</h1>\n"
        ),
        id="issue #640",
    ),
    pytest.param(
        (
            '<a {% if piece.owner == request.user %} class="disabled {% if not piece.like_count %}hidden{% endif %}"\n'
            "   {% else %}\n"
            '   hx-post="x"\n'
            "   {% endif %}>\n"
            "    test\n"
            "    {% if piece.like_count %}<span>{{ piece.like_count }}</span>{% endif %}\n"
            "</a>\n"
        ),
        (
            '<a {% if piece.owner == request.user %} class="disabled {% if not piece.like_count %}hidden{% endif %}\n'
            '   "\n'
            "   {% else %}\n"
            '   hx-post="x"\n'
            "   {% endif %}>\n"
            "    test\n"
            "    {% if piece.like_count %}<span>{{ piece.like_count }}</span>{% endif %}\n"
            "</a>\n"
        ),
        id="issue #652",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
