"""Test handlebars with tag.

poetry run pytest tests/test_handlebars/test_with.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{{#with person}}<p>{{firstname}} {{lastname}}</p>{{/with}}"),
        ("{{#with person}}\n" "    <p>{{firstname}} {{lastname}}</p>\n" "{{/with}}\n"),
        id="with_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, handlebars_config):
    output = formatter(handlebars_config, source)

    printer(expected, source, output)
    assert expected == output
