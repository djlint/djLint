"""Test for ignore case.

--ignore-case

poetry run pytest tests/test_config/test_ignore_case.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("<Div></dIV><CaTs></CaTs>"),
        ("<Div></dIV>\n" "<CaTs></CaTs>\n"),
        ({"ignore_case": True}),
        id="ignore",
    ),
    pytest.param(
        ("<Div></dIV><CaTs></CaTs>"),
        ("<div></div>\n" "<CaTs></CaTs>\n"),
        ({"ignore_case": False}),
        id="specify keep",
    ),
    pytest.param(
        ("<Div></dIV><CaTs></CaTs>"),
        ("<div></div>\n" "<CaTs></CaTs>\n"),
        (),
        id="keep",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
