"""Test tera profile.

uv run pytest tests/test_tera/test_tera.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        ('{% component card(title="x") %}\n<p>body</p>\n{% endcomponent %}\n'),
        (
            '{% component card(title="x") %}\n'
            "    <p>body</p>\n"
            "{% endcomponent %}\n"
        ),
        id="follow-up: tera v2 components are block tags (issue 1322)",
    ),
    pytest.param(
        ('{% component "calendar" / %}\n<p>after</p>\n'),
        ('{% component "calendar" / %}\n<p>after</p>\n'),
        id="django-components style self-closing component must not indent",
    ),
    pytest.param(
        ("{% set_global counter = 1 %}\n<p>x</p>\n"),
        ("{% set_global counter = 1 %}\n<p>x</p>\n"),
        id="set_global_is_a_single_tag",
    ),
    pytest.param(
        ("{% component chip() %}x{% endcomponent %}\n<p>after</p>\n"),
        ("{% component chip() %}x{% endcomponent %}\n<p>after</p>\n"),
        id="single_line_component_does_not_leak_indent",
    ),
    pytest.param(
        (
            "{% if x %}\n<p>y</p>\n{% elif z %}\n<p>w</p>\n{% endif %}\n"
            "{# note #}\n"
        ),
        (
            "{% if x %}\n    <p>y</p>\n{% elif z %}\n    <p>w</p>\n"
            "{% endif %}\n{# note #}\n"
        ),
        id="jinja_style_blocks_and_comments",
    ),
    pytest.param(
        ("{% raw %}\n{{ not  parsed }}\n{% endraw %}\n"),
        ("{% raw %}\n    {{ not  parsed }}\n{% endraw %}\n"),
        id="raw blocks indent (as under jinja) but content is not reformatted",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_formatter(source: str, expected: str) -> None:
    output = formatter(config_builder({"profile": "tera"}), source)

    printer(expected, source, output)
    assert expected == output


def test_profile_defaults() -> None:
    """Tera expressions are jinja-like, not rust: formatting stays enabled."""
    config = Config("dummy/source.html", profile="tera")

    assert not config.no_function_formatting
    assert not config.no_set_formatting

    names = {x["rule"]["name"] for x in config.linter_rules}
    assert "D004" not in names
    assert "J004" not in names
    assert "J018" not in names
    assert "H005" in names
    assert "T038" in names
