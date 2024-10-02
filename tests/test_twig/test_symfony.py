"""Test twig symfony form tags.

uv run pytest tests/test_twig/test_symfony.py
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
        (
            "{{ form_start(form) }}\n"
            "        {{ form_widget(form) }}\n"
            "\n"
            '        <button type="submit" class="btn btn-primary">\n'
            '            <i class="fa fa-save" aria-hidden="true"></i> {{ \'action.save\'|trans }}\n'
            "        </button>\n"
            "    {{ form_end(form) }}"
        ),
        (
            "{{ form_start(form) }}\n"
            "    {{ form_widget(form) }}\n"
            '    <button type="submit" class="btn btn-primary">\n'
            '        <i class="fa fa-save" aria-hidden="true"></i> {{ \'action.save\'|trans }}\n'
            "    </button>\n"
            "{{ form_end(form) }}\n"
        ),
        id="comments",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, nunjucks_config: Config) -> None:
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
