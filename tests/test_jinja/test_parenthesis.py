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
        "{{_(error)}}", "{{ _(error) }}\n", id="function_arg_named_error"
    ),
    pytest.param(
        "{{ content | addID(id) | toc(tags=['h2']) | safe }}",
        "{{ content | addID(id) | toc(tags=['h2']) | safe }}\n",
        id="function_arg_named_id",
    ),
    pytest.param(
        '<a href="{{ url("fo\'o") }}">Test</a>\n'
        "<a href='{{ url('fo\"o') }}'>Test</a>",
        "<a href=\"{{ url('fo\\'o') }}\">Test</a>\n"
        '<a href=\'{{ url("fo\\"o") }}\'>Test</a>\n',
        id="attribute_quote_escaping",
    ),
    pytest.param(
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>',
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>\n',
        id="single_url_for",
    ),
    pytest.param(
        "<a href = \"{{ url_for('test_reminders') }}\">Test reminders</a>",
        "<a href = \"{{ url_for('test_reminders') }}\">Test reminders</a>\n",
        id="single_url_for_spaced_attribute_equals",
    ),
    pytest.param(
        "<a href=\"/{{ url_for('test_reminders') }}/\">Test reminders</a>",
        "<a href=\"/{{ url_for('test_reminders') }}/\">Test reminders</a>\n",
        id="single_url_for_partial_attribute_value",
    ),
    pytest.param(
        '{{ url("foo") }}', '{{ url("foo") }}\n', id="double_parenthesis_tag"
    ),
    pytest.param(
        '<a href="{{ url_for("test_reminders") }}" class="btn clr sm">Test reminders</a>',
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>\n',
        id="double_url_for",
    ),
    pytest.param(
        '<a href="/{{ url_for("test_reminders") }}/">Test reminders</a>',
        "<a href=\"/{{ url_for('test_reminders') }}/\">Test reminders</a>\n",
        id="double_url_for_partial_attribute_value",
    ),
    pytest.param(
        '<a href="{{ url_for("test_reminders", next="foo") }}">Test reminders</a>',
        "<a href=\"{{ url_for('test_reminders', next='foo') }}\">Test reminders</a>\n",
        id="double_url_for_keyword_args",
    ),
    pytest.param(
        "{{ foo('foo').bar }}",
        '{{ foo("foo").bar }}\n',
        id="issue_704_function_call_attribute_access",
    ),
    pytest.param(
        "{{ url('foo').foo().bar[1] }}",
        '{{ url("foo").foo().bar[1] }}\n',
        id="issue_704_function_call_attribute_access_multiple",
    ),
    pytest.param(
        "<a href='{{ url_for('test_reminders') }}'>Test reminders</a>",
        "<a href='{{ url_for(\"test_reminders\") }}'>Test reminders</a>\n",
        id="single_quoted_attribute_url_for",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output
