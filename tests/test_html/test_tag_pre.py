"""Test html pre tag.

uv run pytest tests/test_html/test_tag_pre.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

# added for https://github.com/djlint/djLint/issues/187
test_data = [
    pytest.param(
        (
            "{% if a %}\n"
            "    <div>\n"
            "        <pre><code>asdf</code></pre>\n"
            "        <pre><code>asdf\n"
            "            </code></pre>\n"
            "        <!-- other html -->\n"
            "        <h2>title</h2>\n"
            "    </div>\n"
            "{% endif %}\n"
        ),
        (
            "{% if a %}\n"
            "    <div>\n"
            "        <pre><code>asdf</code></pre>\n"
            "        <pre><code>asdf\n"
            "            </code></pre>\n"
            "        <!-- other html -->\n"
            "        <h2>title</h2>\n"
            "    </div>\n"
            "{% endif %}\n"
        ),
        id="pre_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
