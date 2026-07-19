"""Test django spaceless tag.

uv run pytest tests/test_django/test_tag_spaces.py
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
        ("{% a %}\n{%b       %}{%+c%}{%-d+%}\n{#a}{{g {%a%}}}{%l{{q}}+%}"),
        (
            "{% a %}\n"
            "{% b %}{%+ c %}{%- d +%}\n"
            "{#a}{{ g {% a % }}}{% l{{ q }} +%}\n"
        ),
        ({}),
        id="messy stuff",
    ),
    pytest.param(
        ("{% a %}\n{%b%}{%c%}{%-d+%}\n{#a}{{g {%a%}}}{%l{{q}}+%}"),
        ("{% a %}\n{%b%}{%c%}{%-d+%}\n{#a}{{g {%a%}}}{%l{{q}}+%}\n"),
        ({"profile": "handlebars"}),
        id="messy stuff",
    ),
    pytest.param(
        # https://github.com/djlint/djLint/issues/262
        ("{% if   abc == 101 %}\n<p>x</p>\n{% endif %}\n{{ name |  upper }}\n"),
        (
            "{% if abc == 101 %}\n"
            "    <p>x</p>\n"
            "{% endif %}\n"
            "{{ name | upper }}\n"
        ),
        ({}),
        id="issue_262_extra_whitespace_condensed",
    ),
    pytest.param(
        ("{% if x == \"a  b\"   and y == 'c\td' %}\n<p>x</p>\n{% endif %}\n"),
        ("{% if x == \"a  b\" and y == 'c\td' %}\n    <p>x</p>\n{% endif %}\n"),
        ({}),
        id="string_literals_keep_whitespace",
    ),
    pytest.param(
        (
            "{% verbatim %}\n"
            "{% foo   bar %}\n"
            "{{ baz   qux }}\n"
            "{% endverbatim %}\n"
        ),
        (
            "{% verbatim %}\n"
            "    {% foo   bar %}\n"
            "    {{ baz   qux }}\n"
            "{% endverbatim %}\n"
        ),
        ({}),
        id="verbatim_content_not_condensed",
    ),
    pytest.param(
        ('{{ x|default:"a \\"b  c\\" d" }}\n'),
        ('{{ x|default:"a \\"b  c\\" d" }}\n'),
        ({}),
        id="escaped_quote_string_keeps_whitespace",
    ),
    pytest.param(
        (
            "{% if aaa                  ==  bbb %}\n"
            "{% comment %}{{ x  |  y }}{% endcomment %}\n"
            "{% endif %}\n"
        ),
        (
            "{% if aaa == bbb %}\n"
            "    {% comment %}{{ x  |  y }}{% endcomment %}\n"
            "{% endif %}\n"
        ),
        ({}),
        id="condensing_does_not_shift_ignored_block_offsets",
    ),
    pytest.param(
        ("{% if x \t%}\n<p>x</p>\n{% endif %}\n"),
        ("{% if x %}\n    <p>x</p>\n{% endif %}\n"),
        ({}),
        id="trailing_tab_condensed_idempotently",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
