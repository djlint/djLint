"""Test for custom html.

--custom-html 'dov'

uv run pytest tests/test_config/test_custom_html.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        ("<mjml><mj-body>this is a email text</mj-body></mjml>"),
        (
            "<mjml>\n"
            "    <mj-body>\n"
            "        this is a email text\n"
            "    </mj-body>\n"
            "</mjml>\n"
        ),
        ({"custom_html": "mjml,mj-body"}),
        id="with_flag",
    ),
    pytest.param(
        ("<mjml><mj-body>this is a email text</mj-body></mjml>"),
        ("<mjml><mj-body>this is a email text</mj-body></mjml>\n"),
        (),
        id="without_flag",
    ),
    pytest.param(
        ("<some-long-custom-element></some-long-custom-element>"),
        ("<some-long-custom-element></some-long-custom-element>\n"),
        ({"custom_html": "mjml,mj-body"}),
        id="other tag",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
