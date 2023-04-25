"""Test for max_attribute_length.

--max-attribute-length 4

poetry run pytest tests/test_config/test_max_attribute_length.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            "<div required\n"
            "     long\n"
            "     attributenamesarereallycool\n"
            '     class="asdf"\n'
            '     data-attr="asdf"\n'
            '     id="asdf">\n'
            "</div>\n"
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        ({"max_attribute_length": 10, "max_line_length": 1}),
        id="short lines",
    ),
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            "<div required\n"
            "     long\n"
            "     attributenamesarereallycool\n"
            '     class="asdf"\n'
            '     data-attr="asdf"\n'
            '     id="asdf"></div>\n'
            '<div class="my long classes"\n'
            '     required="true"\n'
            '     checked="checked"\n'
            '     data-attr="some long junk"\n'
            '     style="margin-left: 90px;\n'
            "            display: contents;\n"
            "            font-weight: bold;\n"
            '            font-size: 1.5rem">\n'
        ),
        ({"max_attribute_length": 10, "max_line_length": 1000}),
        id="longer lines",
    ),
    pytest.param(
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf" ></div>\n'
            '<div class="my long classes" required="true"\n'
            '    checked="checked"\n'
            '    data-attr="some long junk"\n'
            '    style="margin-left: 90px;\n'
            "        display: contents;\n"
            "       font-weight: bold;\n"
            '       font-size: 1.5rem">\n'
        ),
        (
            '<div required long attributenamesarereallycool class="asdf" data-attr="asdf" id="asdf"></div>\n'
            '<div class="my long classes" required="true" checked="checked" data-attr="some long junk" style="margin-left: 90px; display: contents; font-weight: bold; font-size: 1.5rem">\n'
        ),
        ({"max_attribute_length": 10000, "max_line_length": 1000}),
        id="longest lines",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
