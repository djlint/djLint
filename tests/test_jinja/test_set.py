"""Test jinja set tags.

uv run pytest tests/test_jinja/test_set.py
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
        '{% set dir = "example" %}\n{% set foo = dir %}',
        '{% set dir = "example" %}\n{% set foo = dir %}\n',
        id="shadow_builtin",
    ),
    pytest.param(
        '{% set x = print("Hello") %}',
        '{% set x = print("Hello") %}\n',
        id="do_not_execute_expression",
    ),
    pytest.param(
        "{% set card_title_1 = object %}",
        "{% set card_title_1 = object %}\n",
        id="object_context_var",
    ),
    pytest.param(
        (
            "<div>\n"
            "    <div>\n"
            "        {% set image_params = {\n"
            "            image: item.image,\n"
            "            lazy: loop.first\n"
            "        } %}\n"
            "    </div>\n"
            "</div>"
        ),
        (
            "<div>\n"
            "    <div>\n"
            "        {% set image_params = {\n"
            "            image: item.image,\n"
            "            lazy: loop.first\n"
            "        } %}\n"
            "    </div>\n"
            "</div>\n"
        ),
        id="nested_multiline_set_keeps_relative_indent",
    ),
    pytest.param(
        "{% set hero_content %}{% block hero %}{% endblock %}{% endset %}",
        "{% set hero_content %}{% block hero %}{% endblock %}{% endset %}\n",
        id="single_line_set_block_captures_verbatim",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {% set hero_content %}{% block hero %}{% endblock %}{% endset %}\n"
            "    <p>after</p>\n"
            "</div>"
        ),
        (
            "<div>\n"
            "    {% set hero_content %}{% block hero %}{% endblock %}{% endset %}\n"
            "    <p>after</p>\n"
            "</div>\n"
        ),
        id="single_line_set_block_nested_in_html",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
