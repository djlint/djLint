"""Test html tags closed in a different template block.

uv run pytest tests/test_linter/test_h041.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.settings import Config
    from djlint.types import LintError

test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/88
        (
            "{% block content %}\n"
            '<div class="pt-5 mt-3">\n'
            "<p>x</p>\n"
            "{% endblock content %}\n"
            "{% block javascript %}\n"
            "<p>y</p>\n"
            "</div>\n"
            "{% endblock javascript %}\n"
        ),
        ([
            {
                "code": "H041",
                "line": "7:0",
                "match": "</div>",
                "message": "Tag is closed in a different template block than it was opened.",
            }
        ]),
        id="issue_88_closed_in_other_block",
    ),
    pytest.param(
        (
            "{% block content %}\n"
            "<div>\n"
            "<p>x</p>\n"
            "</div>\n"
            "{% endblock content %}\n"
        ),
        ([]),
        id="closed_in_same_block",
    ),
    pytest.param(
        (
            "{% block outer %}\n"
            "<div>\n"
            "{% block inner %}\n"
            "<p>x</p>\n"
            "{% endblock inner %}\n"
            "</div>\n"
            "{% endblock outer %}\n"
        ),
        ([]),
        id="nested_block_between_open_and_close",
    ),
    pytest.param(
        (
            "{% block outer %}\n"
            "<div>\n"
            "{% block inner %}\n"
            "</div>\n"
            "{% endblock inner %}\n"
            "{% endblock outer %}\n"
        ),
        ([
            {
                "code": "H041",
                "line": "4:0",
                "match": "</div>",
                "message": "Tag is closed in a different template block than it was opened.",
            }
        ]),
        id="closed_inside_nested_block",
    ),
    pytest.param(
        ("<div>\n{% block content %}\n</div>\n{% endblock content %}\n"),
        ([
            {
                "code": "H041",
                "line": "3:0",
                "match": "</div>",
                "message": "Tag is closed in a different template block than it was opened.",
            }
        ]),
        id="opened_outside_closed_inside",
    ),
    pytest.param(("<div>\n<p>x</p>\n</div>\n"), ([]), id="no_blocks_in_file"),
    pytest.param(
        (
            '<div class="card">\n'
            "{# override {% block sidebar %} in child templates #}\n"
            "<p>x</p>\n"
            "</div>\n"
        ),
        ([]),
        id="block_mentioned_in_comment_ignored",
    ),
    pytest.param(
        (
            "{% block docs %}\n"
            '<div class="example">\n'
            "{% verbatim %}\n"
            "Use {% block content %} to define an overridable area.\n"
            "{% endverbatim %}\n"
            "</div>\n"
            "{% endblock docs %}\n"
        ),
        ([]),
        id="block_mentioned_in_verbatim_ignored",
    ),
    pytest.param(
        (
            "<div>\n"
            "{% comment %} old: {% block inner %} {% endcomment %}\n"
            "</div>\n"
        ),
        ([]),
        id="block_mentioned_in_comment_block_ignored",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(
    source: str, expected: list[LintError], django_config: Config
) -> None:
    filename = "test.html"
    output = linter(django_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
