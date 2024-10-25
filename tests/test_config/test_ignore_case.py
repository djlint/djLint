"""Test for ignore case.

--ignore-case

uv run pytest tests/test_config/test_ignore_case.py
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
        ("<Div></dIV><CaTs></CaTs>"),
        ("<Div></dIV>\n<CaTs></CaTs>\n"),
        ({"ignore_case": True}),
        id="ignore",
    ),
    pytest.param(
        ("<Div></dIV><CaTs></CaTs>"),
        ("<div></div>\n<CaTs></CaTs>\n"),
        ({"ignore_case": False}),
        id="specify keep",
    ),
    pytest.param(
        ("<Div></dIV><CaTs></CaTs>"),
        ("<div></div>\n<CaTs></CaTs>\n"),
        (),
        id="keep",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
