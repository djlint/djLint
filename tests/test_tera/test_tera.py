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
        # https://github.com/djlint/djLint/issues/1322 follow-up: tera v2
        # components are block tags
        ('{% component card(title="x") %}\n<p>body</p>\n{% endcomponent %}\n'),
        (
            '{% component card(title="x") %}\n'
            "    <p>body</p>\n"
            "{% endcomponent %}\n"
        ),
        id="component_block_indents",
    ),
    pytest.param(
        # django-components style self-closing component must not indent
        ('{% component "calendar" / %}\n<p>after</p>\n'),
        ('{% component "calendar" / %}\n<p>after</p>\n'),
        id="self_closing_component_does_not_indent",
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
        # raw blocks indent (as under jinja) but content is not reformatted
        ("{% raw %}\n{{ not  parsed }}\n{% endraw %}\n"),
        ("{% raw %}\n    {{ not  parsed }}\n{% endraw %}\n"),
        id="raw_content_not_reformatted",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_formatter(source: str, expected: str) -> None:
    output = formatter(config_builder({"profile": "tera"}), source)

    printer(expected, source, output)
    assert expected == output


def test_profile_defaults() -> None:
    config = Config("dummy/source.html", profile="tera")

    # tera expressions are jinja-like, not rust: formatting stays enabled
    assert not config.no_function_formatting
    assert not config.no_set_formatting

    names = {x["rule"]["name"] for x in config.linter_rules}
    assert "D004" not in names
    assert "J004" not in names
    assert "J018" not in names
    assert "H005" in names
    assert "T038" in names
