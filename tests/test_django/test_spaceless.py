"""Test django spaceless tag.

poetry run pytest tests/test_django/test_spaceless.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ('{% spaceless %}<p><a href="foo/">Foo</a></p>{% endspaceless %}'),
        (
            "{% spaceless %}\n"
            "    <p>\n"
            '        <a href="foo/">Foo</a>\n'
            "    </p>\n"
            "{% endspaceless %}\n"
        ),
        id="spaceless_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
