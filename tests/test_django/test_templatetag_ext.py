"""Test template tag extended usage.

uv run pytest tests/test_django/test_templatetag_ext.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        ('{% component "img" src="{% url \'my_image\' %}" %}'),
        ('{% component "img" src="{% url \'my_image\' %}" %}\n'),
        ({"custom_blocks": "component"}),
        id="template_tag_inside_template_tag",
    )
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
