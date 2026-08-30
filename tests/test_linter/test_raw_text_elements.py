"""Test that raw text elements hide their body and not their tags.

uv run pytest tests/test_linter/test_raw_text_elements.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from djlint.settings import Config
from tests.conftest import lint_printer

if TYPE_CHECKING:
    from djlint.types import LintError

reported_test_data = [
    pytest.param(
        ('<script type="text/javascript" src="app.js"></script>'),
        (["H024"]),
        id="script_type",
    ),
    pytest.param(
        ('<style type="text/css">a{color:red}</style>'),
        (["H024"]),
        id="style_type",
    ),
    pytest.param(
        ('<script SRC="app.js"></script>'), (["H010"]), id="script_case"
    ),
    pytest.param(('<pre CLASS="a">text</pre>'), (["H010"]), id="pre_case"),
    pytest.param(
        ('<textarea CLASS="a">text</textarea>'), (["H010"]), id="textarea_case"
    ),
]


@pytest.mark.parametrize(("source", "expected"), reported_test_data)
def test_opening_tag_is_checked(source: str, expected: list[str]) -> None:
    config = Config("dummy/source.html")
    output = linter(config, source, "t.html", "t.html")["t.html"]

    lint_printer(source, [], output)
    assert sorted({error["code"] for error in output}) == expected


ignored_test_data = [
    pytest.param(
        ('<div><script>var s = "<DIV CLASS=x>";</script></div>'),
        id="markup_in_a_script_string",
    ),
    pytest.param(
        ("<div><script>// don't warn about <DIV CLASS=x>\n</script></div>"),
        id="apostrophe_in_a_script_comment",
    ),
    pytest.param(
        ('<div><style>a[title="<b>"]{color:red}</style></div>'),
        id="markup_in_a_style_selector",
    ),
    pytest.param(
        ("<div><textarea>&lt;DIV CLASS=x&gt;</textarea></div>"),
        id="markup_shown_in_a_textarea",
    ),
    pytest.param(
        ("<div>\n  <script>\n  var x = 1;\n  </script>\n</div>\n"),
        id="multiline_script_pairs_with_its_closing_tag",
    ),
]


@pytest.mark.parametrize("source", ignored_test_data)
def test_body_is_not_markup(source: str) -> None:
    config = Config("dummy/source.html")
    output: list[LintError] = linter(config, source, "t.html", "t.html")[
        "t.html"
    ]

    lint_printer(source, [], output)
    assert not output
