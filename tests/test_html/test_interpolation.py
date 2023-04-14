"""Test interpolation.

poetry run pytest tests/test_html/test_interpolation.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<!--interpolations in html should be treated as normal text--><div>Fuga magnam facilis. Voluptatem quaerat porro.{{\n"
            "x => {\n"
            "    const hello = 'world'\n"
            "    return hello;\n"
            "}\n"
            "}} Magni consectetur in et molestias neque esse voluptatibus voluptas. {{\n"
            "\n"
            "\n"
            "    some_variable\n"
            "}} Eum quia nihil nulla esse. Dolorem asperiores vero est error {{\n"
            "                    preserve\n"
            "                    invalid\n"
            "\n"
            "                    interpolation\n"
            "}} reprehenderit voluptates minus {{console.log(  short_interpolation )}} nemo.</div>\n"
        ),
        (
            "<!--interpolations in html should be treated as normal text-->\n"
            "<div>\n"
            "    Fuga magnam facilis. Voluptatem quaerat porro.{{ x => { const hello = 'world'\n"
            "    return hello; } }} Magni consectetur in et molestias neque esse voluptatibus\n"
            "    voluptas. {{ some_variable }} Eum quia nihil nulla esse. Dolorem asperiores\n"
            "    vero est error {{ preserve invalid interpolation }} reprehenderit voluptates\n"
            "    minus {{console.log( short_interpolation )}} nemo.\n"
            "</div>\n"
        ),
        id="interpolation_in_text",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, source, output)
    assert expected == output
