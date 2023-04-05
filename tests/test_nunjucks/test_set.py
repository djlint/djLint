"""Test nunjucks set tags.

poetry run pytest tests/test_nunjucks/test_set.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{%- set posts = collections.docs -%}"),
        ("{%- set posts = collections.docs -%}\n"),
        id="set",
    ),
    pytest.param(
        ("{%-set posts = collections.docs-%}\n{%asdf%}"),
        ("{%- set posts = collections.docs -%}\n" "{% asdf %}\n"),
        id="set_with_sibling",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, nunjucks_config):
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
