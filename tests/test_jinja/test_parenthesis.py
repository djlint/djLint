"""Test jinja parenthesis.

uv run pytest tests/test_jinja/test_parenthesis.py
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from djlint._reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from djlint._settings import Config

test_data = [
    pytest.param("{{ url('foo') }}", '{{ url("foo") }}\n', id="single_parenthesis_tag"),
    pytest.param("{{_(error)}}", "{{ _(error) }}\n", id="function_arg_named_error"),
    pytest.param(
        "{{ content | addID(id) | toc(tags=['h2']) | safe }}",
        "{{ content | addID(id) | toc(tags=['h2']) | safe }}\n",
        id="function_arg_named_id",
    ),
    pytest.param(
        "<a href=\"{{ url(\"fo'o\") }}\">Test</a>\n<a href='{{ url('fo\"o') }}'>Test</a>",
        "<a href=\"{{ url('fo\\'o') }}\">Test</a>\n<a href='{{ url(\"fo\\\"o\") }}'>Test</a>\n",
        id="attribute_quote_escaping",
    ),
    pytest.param(
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>',
        '<a href="{{ url_for(\'test_reminders\') }}" class="btn clr sm">Test reminders</a>\n',
        id="single_url_for",
    ),
    pytest.param(
        "<a href = \"{{ url_for('test_reminders') }}\">Test reminders</a>",
        "<a href=\"{{ url_for('test_reminders') }}\">Test reminders</a>\n",
        id="single_url_for_spaced_attribute_equals",
    ),
    pytest.param(
        "<a href=\"/{{ url_for('test_reminders') }}/\">Test reminders</a>",
        "<a href=\"/{{ url_for('test_reminders') }}/\">Test reminders</a>\n",
        id="single_url_for_partial_attribute_value",
    ),
    pytest.param('{{ url("foo") }}', '{{ url("foo") }}\n', id="double_parenthesis_tag"),
    pytest.param(
        (
            "<div>\n"
            "    {{ render_partial('components/button.html.jinja2',\n"
            "       content='Press me!',\n"
            "       icon=render_partial('components/icon.html.jinja2', icon='icon'),\n"
            "       some_other_arg='hello') }}\n"
            "</div>"
        ),
        (
            "<div>\n"
            "    {{ render_partial('components/button.html.jinja2',\n"
            "        content='Press me!',\n"
            "        icon=render_partial('components/icon.html.jinja2', icon='icon'),\n"
            "        some_other_arg='hello') }}\n"
            "</div>\n"
        ),
        id="issue_805_nested_call_no_space_before_comma",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {{ render(value }}\n"
            "    <a href=\"{{ url_for('page') }}\">{{ label(name='n') }}</a>\n"
            "</div>"
        ),
        (
            "<div>\n"
            "    {{ render(value }}\n"
            "    <a href=\"{{ url_for('page') }}\">{{ label(name='n') }}</a>\n"
            "</div>\n"
        ),
        id="unbalanced_parenthesis_does_not_hang",
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
    pytest.param(
        '{{ _("test")|upper }}', '{{ _("test")|upper }}\n', id="issue_2409_filter_against_call"
    ),
    pytest.param(
        '{{ _("test") | upper }}',
        '{{ _("test") | upper }}\n',
        id="issue_2409_filter_spaced_from_call",
    ),
    pytest.param(
        "{{ function(\n    a=1,\n    b=2,\n) }}",
        "{{ function(\n    a=1,\n    b=2,\n) }}\n",
        id="issue_2410_arguments_on_their_own_lines",
    ),
    pytest.param(
        '{{ _("Hello " "world") }}',
        '{{ _("Hello " "world") }}\n',
        id="adjacent_strings_stay_strings",
    ),
    pytest.param(
        '{{ f("""a""") }}', '{{ f("""a""") }}\n', id="triple_quoted_string_stays_a_string"
    ),
    pytest.param(
        '<a href="{{ url_for(page, 2) }}">x</a>',
        '<a href="{{ url_for(page, 2) }}">x</a>\n',
        id="arguments in an attribute holding no string",
    ),
    pytest.param(
        '<a href="{{ url_for(page, [) }}">x</a>',
        '<a href="{{ url_for(page, [) }}">x</a>\n',
        id="arguments in an attribute that python cannot read are left alone",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, jinja_config: Config) -> None:
    output = formatter(jinja_config, source)

    printer(expected, source, output)
    assert expected == output


def test_a_number_too_long_to_write_out_stays_as_written(jinja_config: Config) -> None:
    """str() refuses an integer past the conversion limit, so the call is left as written."""
    source = "{{ f(0x" + "f" * 4000 + ") }}"
    limit = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(4300)
    try:
        assert formatter(jinja_config, source) == source + "\n"
    finally:
        sys.set_int_max_str_digits(limit)


def test_issue_1428_no_trailing_whitespace(jinja_config: Config) -> None:
    source = (
        "{%- macro fix_user_string(value) -%}\n"
        "    {{ value\n"
        "    | replace('\\\\', '\\\\\\\\')\n"
        '    | replace("\\n", "\\\\n")\n'
        "    }}\n"
        "{%- endmacro -%}\n"
    )
    expected = (
        "{%- macro fix_user_string(value) -%}\n"
        "    {{ value\n"
        "        | replace('\\\\', '\\\\\\\\')\n"
        '        | replace("\\n", "\\\\n")\n'
        "    }}\n"
        "{%- endmacro -%}\n"
    )

    output = formatter(jinja_config, source)
    assert output == expected
    assert formatter(jinja_config, output) == output


def test_quote_style_single() -> None:
    config = config_builder({"profile": "jinja", "quote_style": "single"})
    source = '{{ url("foo") }}\n{% set x = "a" %}\n<a href=\'{{ url("bar") }}\'>x</a>\n'
    expected = "{{ url('foo') }}\n{% set x = 'a' %}\n<a href='{{ url(\"bar\") }}'>x</a>\n"

    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
