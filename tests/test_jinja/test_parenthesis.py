"""Test jinja parenthesis.

uv run pytest tests/test_jinja/test_parenthesis.py
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
        "{{ url('foo') }}", '{{ url("foo") }}\n', id="single_parenthesis_tag"
    ),
    pytest.param(
        '<a href="{{ url(\'fo"o\') }}"\n'
        '   href="{{ url(\'fo\\"o\') }}"\n'
        '   href="{{ url("fo\'o") }}"\n'
        '   href="{{ url("fo\\\'o") }}"\n'
        "   href=\"{{ url('foo') }}\"\n"
        '   href="{{ url("foo") }}"></a>',
        '<a href="{{ url("fo\\"o") }}"\n'
        '   href="{{ url("fo\\"o") }}"\n'
        '   href="{{ url("fo\'o") }}"\n'
        '   href="{{ url("fo\'o") }}"\n'
        "   href=\"{{ url('foo') }}\"\n"
        "   href=\"{{ url('foo') }}\"></a>\n",
        id="single_escaped quote",
    ),
    pytest.param(
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>',
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>\n',
        id="single_url_for",
    ),
    pytest.param(
        '{{ url("foo") }}', '{{ url("foo") }}\n', id="double_parenthesis_tag"
    ),
    pytest.param(
        '<a href="{{ url_for("test_reminders") }}" class="btn clr sm">Test reminders</a>',
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>\n',
        id="double_url_for",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
