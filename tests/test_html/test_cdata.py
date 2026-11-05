"""Test cdata.

uv run pytest tests/test_html/test_cdata.py
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
            "<span><![CDATA[<sender>John Smith</sender>]]></span>\n"
            "<span><![CDATA[1]]> a <![CDATA[2]]></span>\n"
            "<span><![CDATA[1]]> <br> <![CDATA[2]]></span>\n"
        ),
        (
            "<span><![CDATA[<sender>John Smith</sender>]]></span>\n"
            "<span><![CDATA[1]]> a <![CDATA[2]]></span>\n"
            "<span><![CDATA[1]]>\n"
            "    <br>\n"
            "<![CDATA[2]]></span>\n"
        ),
        id="cdata",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
