"""Test srcset.

poetry run pytest tests/test_html/test_srcset.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '<img src="a"\n'
            'srcset="\n'
            " should-not-format  400w 100h,\n"
            "       should-not-format  500w 200h\n"
            '"\n'
            ' alt=""      />\n'
            '<img src="a"\n'
            'srcset="\n'
            " should-not-format ,, should-not-format 0q,,,\n"
            '"\n'
            ' alt=""/>\n'
        ),
        (
            '<img src="a"\n'
            '     srcset="should-not-format  400w 100h, should-not-format  500w 200h"\n'
            '     alt="" />\n'
            '<img src="a"\n'
            '     srcset="should-not-format ,, should-not-format 0q,,,"\n'
            '     alt="" />\n'
        ),
        id="invalid",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, basic_config):
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output
