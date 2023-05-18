"""Test interpolation.

poetry run pytest tests/test_html/test_interpolation.py
"""
import pytest

from src.djlint.reformat import formatter
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
            "    Fuga magnam facilis. Voluptatem quaerat porro.{{\n"
            "    x => {\n"
            "    const hello = 'world'\n"
            "    return hello;\n"
            "    }\n"
            "    }} Magni consectetur in et molestias neque esse voluptatibus voluptas. {{\n"
            "    some_variable\n"
            "    }} Eum quia nihil nulla esse. Dolorem asperiores vero est error {{\n"
            "    preserve\n"
            "    invalid\n"
            "    interpolation\n"
            "    }} reprehenderit voluptates minus {{ console.log(short_interpolation) }} nemo.\n"
            "</div>\n"
        ),
        id="interpolation_in_text",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
