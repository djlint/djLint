"""Test django partialdef tag."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        (
            '<label class="swap">\n'
            "    {% partialdef theme_change %}\n"
            "    {% render_field profile_theme_form.selected_theme %}\n"
            "    {% endpartialdef theme_change %}\n"
            "    <svg></svg>\n"
            "</label>"
        ),
        (
            '<label class="swap">\n'
            "    {% partialdef theme_change %}\n"
            "        {% render_field profile_theme_form.selected_theme %}\n"
            "    {% endpartialdef theme_change %}\n"
            "    <svg>\n"
            "    </svg>\n"
            "</label>\n"
        ),
        id="named_partialdef",
    ),
    pytest.param(
        (
            "{% partialdef user_info %}\n"
            "<div>{{ user.name }}</div>\n"
            "{% endpartialdef %}"
        ),
        (
            "{% partialdef user_info %}\n"
            "    <div>{{ user.name }}</div>\n"
            "{% endpartialdef %}\n"
        ),
        id="unnamed_endpartialdef",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
