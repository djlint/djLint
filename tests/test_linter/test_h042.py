"""Test label for attributes matching element ids.

uv run pytest tests/test_linter/test_h042.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from djlint.settings import Config
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.types import LintError

test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/820
        ('<label for="wine">Wine</label>\n<input id="cheese">\n'),
        ([
            {
                "code": "H042",
                "line": "1:0",
                "match": '<label for="wine">',
                "message": "Label for attribute has no matching element id in this file.",
            }
        ]),
        id="issue_820_no_matching_id",
    ),
    pytest.param(
        (
            '<label for="wine">Wine</label>\n'
            '<input id="cheese">\n'
            '<input id="cheese">\n'
        ),
        ([
            {
                "code": "H042",
                "line": "1:0",
                "match": '<label for="wine">',
                "message": "Label for attribute has no matching element id in this file.",
            }
        ]),
        id="issue_820_duplicate_other_ids",
    ),
    pytest.param(
        ('<label for="cheese">Cheese</label>\n<input id="cheese">\n'),
        ([]),
        id="matching_id",
    ),
    pytest.param(
        ('<label for=wine>Wine</label>\n<div id="wine"></div>\n'),
        ([]),
        id="unquoted_attributes",
    ),
    pytest.param(
        ('<label for="{{ field.id_for_label }}">Field</label>\n'),
        ([]),
        id="output_expression_silences_file",
    ),
    pytest.param(
        ('<label for="wine">Wine</label>\n<input id="{{ prefix }}-wine">\n'),
        ([]),
        id="dynamic_id_silences_file",
    ),
    pytest.param(
        ('<label for="id_email">Email</label>\n{{ form.email }}\n'),
        ([]),
        id="widget_output_silences_file",
    ),
    pytest.param(
        ('<label for="x">X</label>\n{% include "form.html" %}\n'),
        ([]),
        id="include_silences_file",
    ),
    pytest.param(
        ('<label for="x">X</label>\n{% render_field form.x %}\n'),
        ([]),
        id="unknown_tag_silences_file",
    ),
    pytest.param(
        (
            "{% if a %}\n"
            '<label for="wine">Wine</label>\n'
            '<input id="cheese">\n'
            "{% endif %}\n"
        ),
        ([
            {
                "code": "H042",
                "line": "2:0",
                "match": '<label for="wine">',
                "message": "Label for attribute has no matching element id in this file.",
            }
        ]),
        id="control_flow_only_file_is_checked",
    ),
    pytest.param(
        ("<label>Wine <input></label>\n"), ([]), id="label_without_for"
    ),
    pytest.param(
        (
            '<label data-for="ghost" for="x">X</label>\n'
            '<input id="x" placeholder=\'for="phantom"\'>\n'
        ),
        ([]),
        id="data_for_and_quoted_lookalikes_ignored",
    ),
    pytest.param(
        ('<label for>W</label>\n<input id="x">\n'),
        ([
            {
                "code": "H042",
                "line": "1:0",
                "match": "<label for>",
                "message": "Label for attribute has no matching element id in this file.",
            }
        ]),
        id="valueless_for_reported_like_empty",
    ),
    pytest.param(
        (
            '<label for="qty">Quantity</label>\n'
            "<script>\n"
            "    // if qty<max we shouldn't warn\n"
            "    if (qty < max) warn();\n"
            "</script>\n"
            '<input id="qty" type="number">\n'
        ),
        ([]),
        id="script_body_cannot_hide_later_ids",
    ),
    pytest.param(
        ('<label for="a&amp;b">A</label>\n<input id="a&b">\n'),
        ([]),
        id="entities_decoded_before_comparison",
    ),
    pytest.param(
        ('<label for=" x ">X</label>\n<input id="x">\n'),
        ([
            {
                "code": "H042",
                "line": "1:0",
                "match": '<label for=" x ">',
                "message": "Label for attribute has no matching element id in this file.",
            }
        ]),
        id="whitespace_padded_for_is_broken_in_browsers",
    ),
    pytest.param(
        (
            '<label for="x">X</label>\n'
            '{% comment %}<input id="x">{% endcomment %}\n'
        ),
        ([
            {
                "code": "H042",
                "line": "1:0",
                "match": '<label for="x">',
                "message": "Label for attribute has no matching element id in this file.",
            }
        ]),
        id="commented_out_id_does_not_count",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: list[LintError]) -> None:
    config = Config("dummy/source.html", profile="django", include="H042")
    filename = "test.html"
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
