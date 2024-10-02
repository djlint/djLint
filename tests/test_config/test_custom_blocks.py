"""Test for custom blocks.

--custom-blocks 'toc'

uv run pytest tests/test_config/test_custom_blocks.py
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
        (
            "{% example stuff %}<p>this is a very very long paragraph that does nothing except be a long paragraph asdfasdfasdfasdfasdf fasdf asdfasdfasdf</p>{% endexample %}\n"
            "\n"
            "{% verylongexampletagthatiskindaneattolookat stuff%}{{ tag }}{% endverylongexampletagthatiskindaneattolookat %}"
        ),
        (
            "{% example stuff %}\n"
            "    <p>\n"
            "        this is a very very long paragraph that does nothing except be a long paragraph asdfasdfasdfasdfasdf fasdf asdfasdfasdf\n"
            "    </p>\n"
            "{% endexample %}\n"
            "{% verylongexampletagthatiskindaneattolookat stuff %}\n"
            "    {{ tag }}\n"
            "{% endverylongexampletagthatiskindaneattolookat %}\n"
        ),
        ({
            "custom_blocks": "toc,example,verylongexampletagthatiskindaneattolookat"
        }),
        id="one",
    ),
    pytest.param(
        (
            "{% custom_block %}\n"
            "    {% custom_block_but_different %}\n"
            "    <p>some other content</p>\n"
            "{% endcustom_block %}\n"
        ),
        (
            "{% custom_block %}\n"
            "    {% custom_block_but_different %}\n"
            "    <p>some other content</p>\n"
            "{% endcustom_block %}\n"
        ),
        ({"custom_blocks": "custom_block"}),
        id="custom_block_with_similar_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
