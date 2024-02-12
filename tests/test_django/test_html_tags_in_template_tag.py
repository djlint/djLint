"""Test html inside template tags for tag.

poetry run pytest tests/test_django/test_html_tags_in_template_tag.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{{ some_val | default:'some_comment1<br>some_comment2' }}"),
        ("{{ some_val | default:'some_comment1<br>some_comment2' }}\n"),
        id="test",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
