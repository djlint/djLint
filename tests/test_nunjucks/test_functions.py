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
            '{{ item.split("/").bar }}\n'
        ),
        ({}),
        id="test index (issue 704)",
    ),
    pytest.param(
        ("{{ url('foo').foo }}"),
        ('{{ url("foo").foo }}\n'),
        ({}),
        id="function call attribute access (issue 704)",
    ),
    pytest.param(
        ("{{ url('foo').foo().bar[1] }}"),
        ('{{ url("foo").foo().bar[1] }}\n'),
        ({}),
        id="function call attribute access multiple (issue 704)",
    ),
    pytest.param(
        ("{{ myfunc({\n  bar: {\n    baz: {\n      cux: 1\n    }\n  }\n})}}"),
        (
            "{{ myfunc({\n"
            "    bar: {\n"
            "        baz: {\n"
            "            cux: 1\n"
            "        }\n"
            "    }\n"
            "})}}\n"
        ),
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
        (
            "{{ myfunc({\n"
            "    bar: {\n"
            "        baz: {\n"
            "            cux: 1\n"
            "        }\n"
            "    }\n"
            "})}\n"
        ),
        ({}),
        id="broken",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {{ apos.singleton(data.global, 'footerHead', {\n"
            "        toolbar: ['Styles', 'Bold'],\n"
            "        styles: [\n"
            "            {\n"
            "                name: 'footerHead',\n"
            "                element: 'div'\n"
            "            }\n"
            "        ]\n"
            "    }) }}\n"
            "</div>\n"
        ),
        (
            "<div>\n"
            "    {{ apos.singleton(data.global, 'footerHead', {\n"
            "        toolbar: ['Styles', 'Bold'],\n"
            "        styles: [\n"
            "            {\n"
            "                name: 'footerHead',\n"
            "                element: 'div'\n"
            "            }\n"
            "        ]\n"
            "    }) }}\n"
            "</div>\n"
        ),
        ({}),
        id="issue 808 non json args keep indent (issue 808)",
    ),
    pytest.param(
        ("{{ url(object) }}"),
        ("{{ url(object) }}\n"),
        ({}),
        id="function param is python keyword (issue 756)",
    ),
    pytest.param(
        ("{{ _expand_attrs(kwargs) }}"),
        ("{{ _expand_attrs(kwargs) }}\n"),
        ({}),
        id="function param named kwargs",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    args["profile"] = "nunjucks"
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
