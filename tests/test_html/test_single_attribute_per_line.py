"""Test single attribute per line.

uv run pytest tests/test_html/test_single_attribute_per_line.py
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
            '<div data-a="1">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="1" data-b="2" data-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="Lorem ipsum dolor sit amet" data-b="Lorem ipsum dolor sit amet" data-c="Lorem ipsum dolor sit amet">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-long-attribute-a="1" data-long-attribute-b="2" data-long-attribute-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            '<img src="/images/foo.png" alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />\n'
        ),
        (
            '<div data-a="1">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-a="1" data-b="2" data-c="3">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-a="Lorem ipsum dolor sit amet"\n'
            '     data-b="Lorem ipsum dolor sit amet"\n'
            '     data-c="Lorem ipsum dolor sit amet">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-long-attribute-a="1"\n'
            '     data-long-attribute-b="2"\n'
            '     data-long-attribute-c="3">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            '<img src="/images/foo.png"\n'
            '     alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />\n'
        ),
        id="single_attrib_per_line_enabled",
    ),
    pytest.param(
        (
            '<div data-a="1">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="1" data-b="2" data-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-a="Lorem ipsum dolor sit amet" data-b="Lorem ipsum dolor sit amet" data-c="Lorem ipsum dolor sit amet">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<div data-long-attribute-a="1" data-long-attribute-b="2" data-long-attribute-c="3">\n'
            "  Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "</div>\n"
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            '<img src="/images/foo.png" alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit."     />\n'
        ),
        (
            '<div data-a="1">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-a="1" data-b="2" data-c="3">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-a="Lorem ipsum dolor sit amet"\n'
            '     data-b="Lorem ipsum dolor sit amet"\n'
            '     data-c="Lorem ipsum dolor sit amet">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<div data-long-attribute-a="1"\n'
            '     data-long-attribute-b="2"\n'
            '     data-long-attribute-c="3">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>\n'
            '<img src="/images/foo.png" />\n'
            '<img src="/images/foo.png" alt="bar" />\n'
            '<img src="/images/foo.png"\n'
            '     alt="Lorem ipsum dolor sit amet, consectetur adipiscing elit." />\n'
        ),
        id="single_attrib_per_line_disabled",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
