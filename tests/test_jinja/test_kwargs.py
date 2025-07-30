"""Test jinja kwargs preservation.

Tests to ensure **kwargs syntax is preserved in template function calls.
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
        ("{{ button(**kwargs) }}"),
        ("{{ button(**kwargs) }}\n"),
        id="simple_kwargs",
    ),
    pytest.param(
        ("{{ button(text, **kwargs) }}"),
        ("{{ button(text, **kwargs) }}\n"),
        id="kwargs_with_arg",
    ),
    pytest.param(
        ("{{ button(text, type=\"link\", **kwargs) }}"),
        ("{{ button(text, type=\"link\", **kwargs) }}\n"),
        id="kwargs_with_multiple_args",
    ),
    pytest.param(
        ("{{ button(text, type=\"link\", _=\"on click go to url '\"~href~\"'\", **kwargs) }}"),
        ("{{ button(text, type=\"link\", _=\"on click go to url '\"~href~\"'\", **kwargs) }}\n"),
        id="kwargs_with_complex_string",
    ),
    pytest.param(
        (
            "{% macro link_button(text, href='') %}\n"
            "    {{ button(text, type=\"link\", **kwargs) }}\n"
            "{% endmacro %}"
        ),
        (
            "{% macro link_button(text, href='') %}\n"
            "    {{ button(text, type=\"link\", **kwargs) }}\n"
            "{% endmacro %}\n"
        ),
        id="kwargs_in_macro",
    ),
    pytest.param(
        ("{{ func(a=1, b=2, **kwargs) }}"),
        ("{{ func(a=1, b=2, **kwargs) }}\n"),
        id="kwargs_with_keyword_args",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_kwargs_preservation(source: str, expected: str, jinja_config: Config) -> None:
    """Test that **kwargs syntax is preserved and not replaced with {}."""
    output = formatter(jinja_config, source)

    # Ensure **kwargs is preserved
    if "**kwargs" in source:
        assert "**kwargs" in output, f"**kwargs was removed from output: {output}"
        assert "{}" not in output.replace("{%", "").replace("%}", "").replace("{{", "").replace("}}", ""), \
            f"**kwargs appears to have been replaced with {{}}: {output}"

    printer(expected, source, output)
    assert expected == output