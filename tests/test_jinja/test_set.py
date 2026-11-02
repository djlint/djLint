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
    pytest.param(
        (
            "{% set menu = menu_item(\n"
            "    title='title',\n"
            "    submenu=[\n"
            "        menu_item(\n"
            "            title='title',\n"
            "            submenu=[],\n"
            "        )\n"
            "    ],\n"
            ") %}"
        ),
        (
            "{% set menu = menu_item(\n"
            "    title='title',\n"
            "    submenu=[\n"
            "        menu_item(\n"
            "            title='title',\n"
            "            submenu=[],\n"
            "        )\n"
            "    ],\n"
            ") %}\n"
        ),
        id="nested_call_in_multiline_set_is_indented",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {% set items = pick(\n"
            "        [1,\n"
            "            2]) %}\n"
            "    <p>after</p>\n"
            "</div>"
        ),
        (
            "<div>\n"
            "    {% set items = pick(\n"
            "        [1,\n"
            "            2]) %}\n"
            "    <p>after</p>\n"
            "</div>\n"
        ),
        id="multiline_set_closing_after_an_opener_restores_the_level",
    ),
    pytest.param(
        ('{% set style = style ~\n    "url(\'data:image/svg+xml," ~\n    icon ~\n    "\');" %}'),
        ('{% set style = style ~\n    "url(\'data:image/svg+xml," ~\n    icon ~\n    "\');" %}\n'),
        id="bracket_inside_a_string_in_multiline_set_opens_nothing",
    ),
    pytest.param(
        ("{% set x = outer(\n    build(inner(),\n        1),\n    2,\n) %}"),
        ("{% set x = outer(\n    build(inner(),\n        1),\n    2,\n) %}\n"),
        id="call_left_open_after_a_closed_one_in_multiline_set",
    ),
    pytest.param(
        ("{% set x = pair(\n    first(\n        1\n    ), second(\n        2\n    )\n) %}"),
        ("{% set x = pair(\n    first(\n        1\n    ), second(\n        2\n    )\n) %}\n"),
        id="line_closing_one_call_and_opening_another_in_multiline_set",
    ),
    pytest.param(
        ("{% set x = outer(\n    inner(\n        deep(\n            1\n        )),\n    2\n) %}"),
        ("{% set x = outer(\n    inner(\n        deep(\n            1\n        )),\n    2\n) %}\n"),
        id="line_closing_two_calls_in_multiline_set",
    ),
    pytest.param(
        ("{% set value = outer(inner(\n        1\n    ),\n    2\n) %}\n<p>after</p>"),
        ("{% set value = outer(inner(\n        1\n    ),\n    2\n) %}\n<p>after</p>\n"),
        id="two_calls_opened_on_the_set_line",
    ),
    pytest.param(
        ('<div>\n    {% set x = "((\ntext" %}\n    <p>after</p>\n</div>'),
        ('<div>\n    {% set x = "((\ntext" %}\n    <p>after</p>\n</div>\n'),
        id="string_across_lines_in_set_gets_no_indentation",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
