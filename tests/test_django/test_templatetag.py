"""Test django templatetags.

poetry run pytest tests/test_django/test_templatetag.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        ("{% if stuff %}\n{% endif %}"),
        ("{% if stuff %}{% endif %}\n"),
        id="tags_on_one_line",
    ),
    pytest.param(
        ("{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}"),
        ("{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}\n"),
        id="tags_random_text",
    ),
    pytest.param(
        (
            "{% if messages|length %}{% for message in messages %}{{ message }}{% endfor %}{% endif %}"
        ),
        (
            "{% if messages|length %}\n"
            "    {% for message in messages %}{{ message }}{% endfor %}\n"
            "{% endif %}\n"
        ),
        id="single_liner",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
