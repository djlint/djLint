"""Test jinja template variables that shadow HTML tag names.

uv run pytest tests/test_jinja/test_template_variables.py
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
        ("{% set dir = \"example\" %}\n{% set foo = dir %}"),
        ("{% set dir = \"example\" %}\n{% set foo = dir %}\n"),
        id="template_variable_dir_shadowing_html_tag",
    ),
    pytest.param(
        ("{% set span = \"value\" %}\n{{ span }}"),
        ("{% set span = \"value\" %}\n{{ span }}\n"),
        id="template_variable_span_shadowing_html_tag",
    ),
    pytest.param(
        ("{% set var = \"test\" %}\n{% set result = var %}"),
        ("{% set var = \"test\" %}\n{% set result = var %}\n"),
        id="template_variable_var_shadowing_html_tag",
    ),
    pytest.param(
        ("{% set button = \"click me\" %}\n<button>{{ button }}</button>"),
        ("{% set button = \"click me\" %}\n<button>{{ button }}</button>\n"),
        id="template_variable_and_html_tag_mixed",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_template_variables_shadowing_html_tags(source: str, expected: str, jinja_config: Config) -> None:
    """Test that template variables shadowing HTML tag names are not incorrectly processed."""
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output