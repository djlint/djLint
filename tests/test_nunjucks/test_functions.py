"""Test nunjucks functions.

uv run pytest tests/test_nunjucks/test_functions.py
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
        ("{{ myfunc({\n  bar: {\n    baz: {\n      cux: 1\n    }\n  }\n})}}"),
        ('{{ myfunc({"bar": {"baz": {"cux": 1}}}) }}\n'),
        ({}),
        id="long line",
    ),
    pytest.param(
        ('<span class="nav">{{ _("Orders (Selling)") }}</span>'),
        ('<span class="nav">{{ _("Orders (Selling)") }}</span>\n'),
        ({}),
        id="test quoting",
    ),
    pytest.param(
        (
            '{{ item.split("/")[1] }}\n'
            '{{ item.split("/").123 }}\n'
            '{{ item.split("/").bar }}'
        ),
        (
            '{{ item.split("/")[1] }}\n'
            '{{ item.split("/").123 }}\n'
            # https://github.com/djlint/djLint/issues/704
            '{{ item.split("/").bar }}\n'
        ),
        ({}),
        id="test index",
    ),
    pytest.param(
        ("{{ url('foo').foo }}"),
        # https://github.com/djlint/djLint/issues/704
        ('{{ url("foo").foo }}\n'),
        ({}),
        id="function_call_attribute_access",
    ),
    pytest.param(
        ("{{ url('foo').foo().bar[1] }}"),
        # https://github.com/djlint/djLint/issues/704
        ('{{ url("foo").foo().bar[1] }}\n'),
        ({}),
        id="function_call_attribute_access_multiple",
    ),
    pytest.param(
        ("{{ myfunc({\n  bar: {\n    baz: {\n      cux: 1\n    }\n  }\n})}}"),
        ("{{ myfunc({\nbar: {\nbaz: {\ncux: 1\n}\n}\n})}}\n"),
        ({"no_function_formatting": True}),
        id="disabled",
    ),
    pytest.param(
        ("{{ myfunc({\n  bar: {\n    baz: {\n      cux: 1\n    }\n  }\n})}}"),
        (
            "{{ myfunc({\n"
            '    "bar": {\n'
            '        "baz": {\n'
            '            "cux": 1\n'
            "        }\n"
            "    }\n"
            "}) }}\n"
        ),
        ({"max_line_length": 1}),
        id="short line",
    ),
    pytest.param(
        (
            "<div>{{ myfunc({\n"
            "  bar: {\n"
            "    baz: {\n"
            "      cux: 1\n"
            "    }\n"
            "  }\n"
            "})}}</div>"
        ),
        (
            "<div>\n"
            "    {{ myfunc({\n"
            '        "bar": {\n'
            '            "baz": {\n'
            '                "cux": 1\n'
            "            }\n"
            "        }\n"
            "    }) }}\n"
            "</div>\n"
        ),
        ({"max_line_length": 1}),
        id="nested",
    ),
    pytest.param(
        ("{{ myfunc({\n  bar: {\n    baz: {\n      cux: 1\n    }\n  }\n})}"),
        ("{{ myfunc({\nbar: {\nbaz: {\ncux: 1\n}\n}\n})}\n"),
        ({}),
        id="broken",
    ),
    pytest.param(
        ("{{ url(object) }}"),
        # https://github.com/djlint/djLint/issues/756
        ("{{ url(object) }}\n"),
        ({}),
        id="function param is python keyword",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    args["profile"] = "nunjucks"
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
