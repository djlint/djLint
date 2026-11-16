"""Test linter code D059 (opt-in rule).

uv run pytest tests/test_linter/test_d059.py
"""

from __future__ import annotations

import pytest

from djlint.settings import Config
from tests.conftest import linter

test_data = [
    pytest.param(
        ("{# This #}\n{# Is #}\n{# a comment #}\n<p>Some text</p>"),
        (["1:0"]),
        id="three comment lines",
    ),
    pytest.param(("{# a #}\n{# b #}"), (["1:0"]), id="two comment lines"),
    pytest.param(("{# a #}\r\n{# b #}"), (["1:0"]), id="two windows lines"),
    pytest.param(
        ("<div>\n    {# a #}  \n    {# b #}\n</div>"), (["2:4"]), id="indented, with trailing space"
    ),
    pytest.param(("{# a #}\n<p>x</p>\n{# b #}"), ([]), id="one comment line"),
    pytest.param(("{# a #}\n\n{# b #}"), ([]), id="a blank line between"),
    pytest.param(
        ("{# a #}\n{# b #}\n\n{# c #}\n{# d #}"), (["1:0", "4:0"]), id="two runs a blank line apart"
    ),
    pytest.param(("{# a #} <p>x</p>\n{# b #}"), ([]), id="a comment sharing its line"),
    pytest.param(("{# a #}{# b #}\n{# c #}"), ([]), id="two comments on one line"),
    pytest.param(("{# a #}\n{# b\nc #}"), ([]), id="a comment Django reads as text"),
    pytest.param(
        ("{# djlint:off H006 #}\n{# a #}\n{# b #}\n{# djlint:on #}"),
        (["2:0"]),
        id="a djlint directive does not join a run",
    ),
    pytest.param(("{# DJLINT:OFF H006 #}\n{# a #}"), ([]), id="a directive in capitals"),
    pytest.param(
        ("{# djlint:off #}\n{# a #}\n{# b #}\n{# djlint:on #}"),
        ([]),
        id="inside a djlint:off region",
    ),
    pytest.param(
        ('{# Translators: a greeting #}\n{# shown on the home page #}\n{% translate "Hi" %}'),
        ([]),
        id="a translator comment does not join a run",
    ),
    pytest.param(
        ('{# a #}\n{# b #}\n{# Translators: a greeting #}\n{% translate "Hi" %}'),
        (["1:0"]),
        id="the lines before a translator comment",
    ),
    pytest.param(("<pre>\n{# a #}\n{# b #}\n</pre>"), ([]), id="inside a pre"),
    pytest.param(("<TEXTAREA>\n{# a #}\n{# b #}\n</TEXTAREA>"), ([]), id="inside a textarea"),
    pytest.param(("<pre>\n{# a #}\n{# b #}"), ([]), id="inside a pre nothing closes"),
    pytest.param(("<pre></pre>\n{# a #}\n{# b #}"), (["2:0"]), id="after a pre"),
    pytest.param(
        ("<pre>\n{% comment %}\n</pre>\n{% endcomment %}\n{# a #}\n{# b #}\n</pre>"),
        ([]),
        id="a pre closing inside a comment block closes nothing",
    ),
    pytest.param(
        ("{% comment %}<pre>{% endcomment %}\n{# a #}\n{# b #}"),
        (["2:0"]),
        id="a pre opening inside a comment block opens nothing",
    ),
    pytest.param(
        ("{% comment %}\n{# a #}\n{# b #}\n{% endcomment %}"), ([]), id="inside a comment block"
    ),
    pytest.param(
        ("{% verbatim %}\n{# a #}\n{# b #}\n{% endverbatim %}"), ([]), id="inside a verbatim block"
    ),
]


@pytest.mark.parametrize(("source", "lines"), test_data)
def test_d059(source: str, lines: list[str]) -> None:
    filename = "test.html"
    config = Config(filename, profile="django", include="D059")

    findings = linter(config, source, filename, filename)[filename]

    assert [error["line"] for error in findings if error["code"] == "D059"] == lines


def test_d059_is_off_by_default() -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, "{# a #}\n{# b #}", filename, filename)[filename]

    assert [error for error in findings if error["code"] == "D059"] == []
