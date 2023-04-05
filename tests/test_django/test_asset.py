"""Test django asset tag.

poetry run pytest tests/test_django/test_asset.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '{% block css %}{% assets "css_error" %}<link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />{% endassets %}{% endblock css %}'
        ),
        (
            "{% block css %}\n"
            '    {% assets "css_error" %}\n'
            '        <link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />\n'
            "    {% endassets %}\n"
            "{% endblock css %}\n"
        ),
        id="asset_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
