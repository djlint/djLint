"""Test django templatetags.

uv run pytest tests/test_django/test_templatetag.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        ("{% if stuff %}\n{% endif %}"),
        ("{% if stuff %}{% endif %}\n"),
        id="tags_on_one_line",
    ),
    pytest.param(
        (
            "{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}"
        ),
        (
            "{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}\n"
        ),
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
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
