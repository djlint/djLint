"""Test disable.

uv run pytest tests/test_djlint/test_ignore.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

    from djlint.settings import Config

test_data = [
    pytest.param(
        ("{# djlint:off #}\n<img \n/>"),
        ("{# djlint:off #}\n<img \n/>\n"),
        id="don't compress",
    )
]

test_off_blocks = [
    pytest.param(
        (
            "<script>\n"
            "    {# djlint:off #}\n"
            "    const _steps = {\n"
            "      {% for step in steps %}\n"
            "        '{{ step.id }}': true\n"
            "        {% if not forloop.last %},{% endif %}\n"
            "      {% endfor %}\n"
            "    };\n"
            "    {# djlint:on #}\n"
            "\n"
            '    document.addEventListener("alpine:init", () => {\n'
            '        Alpine.data("steps-table", () => ({ steps: _steps }));\n'
            "    });\n"
            "</script>"
        ),
        (
            "    {# djlint:off #}\n"
            "    const _steps = {\n"
            "      {% for step in steps %}\n"
            "        '{{ step.id }}': true\n"
            "        {% if not forloop.last %},{% endif %}\n"
            "      {% endfor %}\n"
            "    };\n"
            "    {# djlint:on #}"
        ),
        {"profile": "django", "format_js": True},
        id="inside formatted script",
    ),
    pytest.param(
        (
            "{# djlint:off #}\n"
            "{% block javascript %}\n"
            "    <script>\n"
            '        const someJavascript = "foo";\n'
            "    </script>\n"
            "{% endblock %}\n"
            "{# djlint:on #}"
        ),
        (
            "{# djlint:off #}\n"
            "{% block javascript %}\n"
            "    <script>\n"
            '        const someJavascript = "foo";\n'
            "    </script>\n"
            "{% endblock %}\n"
            "{# djlint:on #}"
        ),
        {"profile": "django", "format_js": False, "format_css": False},
        id="around script block",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, basic_config: Config) -> None:
    output = formatter(basic_config, source)

    printer(expected, source, output)
    assert expected == output


def test_djlint_off_inside_attribute_list_is_preserved() -> None:
    source = (
        '<p class="text-gray-500"\n'
        "  {# djlint:off #}\n"
        '  x-text="\n'
        "  items.length > 3\n"
        "    ? items.slice(0, 3).join(', ') + '...'\n"
        "    : items.join(', ')\n"
        '  "{# djlint:on #}></p>'
    )
    expected = f"{source}\n"
    output = formatter(
        config_builder({"profile": "django", "indent": 2}), source
    )

    printer(expected, source, output)
    assert expected == output


@pytest.mark.parametrize(("source", "ignored_block", "config"), test_off_blocks)
def test_off_blocks_are_preserved(
    source: str, ignored_block: str, config: dict[str, Any]
) -> None:
    output = formatter(config_builder(config), source)

    printer(ignored_block, source, output)
    assert ignored_block in output
