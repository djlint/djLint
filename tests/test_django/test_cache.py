"""Test django cache tag.

uv run pytest tests/test_django/test_cache.py
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
            "<body>\n"
            "    {% block top_navbar %}\n"
            "        {% cache 600 sidebar %}\n"
            "            <p>hi</p>\n"
            "        {% endcache %}\n"
            "    {% endblock top_navbar %}\n"
            "</body>\n"
        ),
        (
            "<body>\n"
            "    {% block top_navbar %}\n"
            "        {% cache 600 sidebar %}\n"
            "            <p>hi</p>\n"
            "        {% endcache %}\n"
            "    {% endblock top_navbar %}\n"
            "</body>\n"
        ),
        id="cache_tag_indent",
    ),
    pytest.param(
        (
            "<body>\n"
            "{% cache 600 sidebar %}\n"
            "<p>hi</p>\n"
            "{% endcache %}\n"
            "</body>\n"
        ),
        (
            "<body>\n"
            "    {% cache 600 sidebar %}\n"
            "        <p>hi</p>\n"
            "    {% endcache %}\n"
            "</body>\n"
        ),
        id="cache_tag_fixes_indent",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
