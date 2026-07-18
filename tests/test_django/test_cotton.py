"""Test django-cotton component tags.

uv run pytest tests/test_django/test_cotton.py
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
        ('<c-card size="large"><p>hi</p><c-vars color="blue" /></c-card>'),
        (
            '<c-card size="large">\n'
            "    <p>hi</p>\n"
            '    <c-vars color="blue" />\n'
            "</c-card>\n"
        ),
        id="cotton_tag_expand",
    ),
    pytest.param(
        (
            "<div>\n"
            '    <c-card size="large">\n'
            "        <p>content</p>\n"
            '        <c-forms.input name="email" type="email" />\n'
            "    </c-card>\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            '    <c-card size="large">\n'
            "        <p>content</p>\n"
            '        <c-forms.input name="email" type="email" />\n'
            "    </c-card>\n"
            "</div>\n"
        ),
        id="cotton_tag_indent",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
