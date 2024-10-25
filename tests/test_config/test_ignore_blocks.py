"""Test for ignored blocks.

--ignore-blocks 'raw'

uv run pytest tests/test_config/test_ignore_blocks.py
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
        ("{% raw%}   {%endraw %}"),
        ("{% raw %}   {% endraw %}\n"),
        ({"ignore_blocks": "raw"}),
        id="ignore_raw",
    ),
    pytest.param(
        ("{% raw%} <div><img/></div>  {%endraw %}"),
        ("{% raw %}\n<div>\n    <img />\n</div>\n{% endraw %}\n"),
        ({"ignore_blocks": "raw"}),
        id="ignore_raw",
    ),
    pytest.param(
        ("{% raw%}<div></div>{%endraw %}"),
        ("{% raw %}\n    <div></div>\n{% endraw %}\n"),
        ({"ignore_blocks": "junk"}),
        id="dont_ignore_raw",
    ),
    pytest.param(
        ("{% raws%}<div></div>{%endraws %}"),
        ("{% raws %}\n    <div></div>\n{% endraws %}\n"),
        ({"ignore_blocks": "raw", "custom_blocks": "raws"}),
        id="test overlap",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
