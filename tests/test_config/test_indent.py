"""Test for indent.

--indent 4

poetry run pytest tests/test_config/test_indent.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("<section><p><div><span></span></div></p></section>"),
        (
            "<section>\n"
            "  <p>\n"
            "    <div>\n"
            "      <span></span>\n"
            "    </div>\n"
            "  </p>\n"
            "</section>\n"
        ),
        ({"indent": 2}),
        id="int",
    ),
    pytest.param(
        ("<section><p><div><span></span></div></p></section>"),
        (
            "<section>\n"
            "  <p>\n"
            "    <div>\n"
            "      <span></span>\n"
            "    </div>\n"
            "  </p>\n"
            "</section>\n"
        ),
        ({"indent": "2"}),
        id="str",
    ),
    pytest.param(
        ("<section><p><div><span></span></div></p></section>"),
        (
            "<section>\n"
            " <p>\n"
            "  <div>\n"
            "   <span></span>\n"
            "  </div>\n"
            " </p>\n"
            "</section>\n"
        ),
        ({"indent": 1}),
        id="one",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
