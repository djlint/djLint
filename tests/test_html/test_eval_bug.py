"""Test case for the error replacement bug.

This test checks that template variables are not evaluated as Python expressions.
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder


test_data = [
    pytest.param(
        ("{{_(error)}}"),
        ("{{ _(error) }}\n"),
        ({}),
        id="error_without_quotes",
    ),
    pytest.param(
        ('{{ _("error") }}'),
        ('{{ _("error") }}\n'),
        ({}),
        id="error_with_quotes",
    ),
    pytest.param(
        ("{{ func(error) }}"),
        ("{{ func(error) }}\n"),
        ({}),
        id="function_with_error_param",
    ),
    pytest.param(
        ("{{ error }}"),
        ("{{ error }}\n"),
        ({}),
        id="plain_error_variable",
    ),
    pytest.param(
        ("{{ _(open) }}"),
        ("{{ _(open) }}\n"),
        ({}),
        id="builtin_function_name",
    ),
    pytest.param(
        ("{{ func(len) }}"),
        ("{{ func(len) }}\n"),
        ({}),
        id="function_with_builtin_param",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_template_variables_not_evaluated(source: str, expected: str, args: dict) -> None:
    """Test that template variables are not evaluated as Python expressions."""
    output = formatter(config_builder(args), source)
    assert expected == output