"""Test for alpine.js.

uv run pytest tests/test_html/test_alpinejs.py
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
            "<div\n"
            '    id="collapse"\n'
            '    x-data="{ show: true }"\n'
            '    x-show="show"\n'
            "    x-transition.duration.500ms\n"
            '    :disabled="!$store.userPreferences.deleteConfirm"\n'
            '    @click="clicked=true"\n'
            "></div>\n"
        ),
        (
            '<div id="collapse"\n'
            '     x-data="{ show: true }"\n'
            '     x-show="show"\n'
            "     x-transition.duration.500ms\n"
            '     :disabled="!$store.userPreferences.deleteConfirm"\n'
            '     @click="clicked=true"></div>\n'
        ),
        id="alpine_js",
    ),
    pytest.param(
        (
            '<html lang="en">\n'
            "    <body>\n"
            "        <!-- x-data , x-text , x-html -->\n"
            "        <div x-data=\"{key: ' value', message:'hello <b>world</b> '}\">\n"
            '            <p x-text="key"></p>\n'
            '            <p x-html="message"></p>\n'
            "        </div>\n"
            "    </body>\n"
            "</html>\n\n"
        ),
        (
            '<html lang="en">\n'
            "    <body>\n"
            "        <!-- x-data , x-text , x-html -->\n"
            "        <div x-data=\"{key: ' value', message:'hello <b>world</b> '}\">\n"
            '            <p x-text="key"></p>\n'
            '            <p x-html="message"></p>\n'
            "        </div>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="alpine_nested_html",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
