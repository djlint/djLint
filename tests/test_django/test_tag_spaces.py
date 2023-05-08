"""Test django spaceless tag.

poetry run pytest tests/test_django/test_tag_spaces.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ("{% a %}\n" "{%b       %}{%+c%}{%-d+%}\n" "{#a}{{g {%a%}}}{%l{{q}}+%}"),
        (
            "{% a %}\n"
            "{% b %}{%+ c %}{%- d +%}\n"
            "{#a}{{ g {% a % }}}{% l{{ q }} +%}\n"
        ),
        ({}),
        id="messy stuff",
    ),
    pytest.param(
        ("{% a %}\n" "{%b%}{%c%}{%-d+%}\n" "{#a}{{g {%a%}}}{%l{{q}}+%}"),
        ("{% a %}\n" "{%b%}{%c%}{%-d+%}\n" "{#a}{{g {%a%}}}{%l{{q}}+%}\n"),
        ({"profile": "handlebars"}),
        id="messy stuff",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
