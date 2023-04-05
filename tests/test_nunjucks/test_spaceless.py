"""Test nunjucks spaceless tag.

poetry run pytest tests/test_nunjucks/test_spaceless.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{%- if entry.children.length -%}<strong>{%- endif -%}"),
        ("{%- if entry.children.length -%}<strong>{%- endif -%}\n"),
        id="spaceless_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, nunjucks_config):
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
