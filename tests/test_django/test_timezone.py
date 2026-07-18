"""Test django tz and l10n tags.

uv run pytest tests/test_django/test_timezone.py
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
            "<div>\n"
            '    {% timezone "Europe/Paris" %}\n'
            "        {{ value }}\n"
            "    {% endtimezone %}\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    {% timezone "Europe/Paris" %}\n'
            "        {{ value }}\n"
            "    {% endtimezone %}\n"
            "</div>\n"
        ),
        id="timezone_tag_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {% localtime on %}\n"
            "        {{ value }}\n"
            "    {% endlocaltime %}\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    {% localtime on %}\n"
            "        {{ value }}\n"
            "    {% endlocaltime %}\n"
            "</div>\n"
        ),
        id="localtime_tag_indent",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {% localize on %}\n"
            "        {{ value }}\n"
            "    {% endlocalize %}\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    {% localize on %}\n"
            "        {{ value }}\n"
            "    {% endlocalize %}\n"
            "</div>\n"
        ),
        id="localize_tag_indent",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
