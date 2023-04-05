"""Test django filter tag.

poetry run pytest tests/test_django/test_filter.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "{% filter force_escape|lower %}This text will be HTML-escaped, and will appear in all lowercase.{% endfilter %}"
        ),
        (
            "{% filter force_escape|lower %}\n"
            "    This text will be HTML-escaped, and will appear in all lowercase.\n"
            "{% endfilter %}\n"
        ),
        id="filter_tag",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
