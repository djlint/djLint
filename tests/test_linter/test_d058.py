"""Test linter code D058.

uv run pytest tests/test_linter/test_d058.py
"""

from __future__ import annotations

import pytest

from djlint.settings import Config
from tests.conftest import linter

test_data = [
    pytest.param(("{# a\nb #}"), ("django"), (["1:0"]), id="a comment over two lines"),
    pytest.param(("{# a\r\nb #}"), ("django"), (["1:0"]), id="a comment over windows lines"),
    pytest.param(('{{ a|default:\n"b" }}'), ("django"), (["1:0"]), id="a variable over two lines"),
    pytest.param(
        ('{% include "a.html" with a=1\n   b=2 %}'),
        ("django"),
        (["1:0"]),
        id="a block tag over two lines",
    ),
    pytest.param(
        ('<p>\n  {# {% include "a.html" %}\n  #}\n</p>'),
        ("django"),
        (["2:2"]),
        id="a comment holding a tag",
    ),
    pytest.param(
        ("{# a\n{{ b }}\nc #}"), ("django"), (["1:0"]), id="a tag inside the comment is not another"
    ),
    pytest.param(
        ("{# a #} {# b\nc #}"), ("django"), (["1:8"]), id="a comment after one closed on its line"
    ),
    pytest.param(("<!-- {# a\nb #} -->"), ("django"), (["1:5"]), id="inside an html comment"),
    pytest.param(
        ("{# a #}\n{{ b }}\n{% if c %}{% endif %}"), ("django"), ([]), id="tags each on one line"
    ),
    pytest.param(
        ("{% if a\n<p>x</p>{% endif %}"),
        ("django"),
        ([]),
        id="a tag another opener follows is left to T039",
    ),
    pytest.param(("{{ a\n<p>x</p>"), ("django"), ([]), id="a tag nothing closes"),
    pytest.param(
        ('{{ value|default:\n"{{ fallback }}" }}'),
        ("django"),
        (["1:0"]),
        id="a quoted opener does not end the tag",
    ),
    pytest.param(
        ("{% if a\n{# b #}\n%}"),
        ("django"),
        (["1:0"]),
        id="a comment inside the tag does not end it",
    ),
    pytest.param(("{% if a\n}%"), ("django"), ([]), id="a typo for the closing is left to T034"),
    pytest.param(
        ('{{ "a\n}}'), ("django"), ([]), id="a closing in an unterminated string is left to T027"
    ),
    pytest.param(
        ("{{% if a %}\n}}"), ("django"), ([]), id="a brace before a tag is text of its own"
    ),
    pytest.param(
        ("{% comment %}\n{# a\nb #}\n{% endcomment %}"),
        ("django"),
        ([]),
        id="inside a comment block",
    ),
    pytest.param(
        ('{% comment "note" %}{{ a\n}}{%endcomment%}'),
        ("django"),
        ([]),
        id="inside a comment block with a note and no spaces",
    ),
    pytest.param(
        ("{% comment %}{% endcomment x %}{# a\nb #}"),
        ("django"),
        ([]),
        id="an endcomment with arguments does not close the block",
    ),
    pytest.param(
        ("{% comment %}{% endcomment %}{# a\nb #}"),
        ("django"),
        (["1:29"]),
        id="after a comment block",
    ),
    pytest.param(
        ("{% verbatim %}{{ a\n}}{% endverbatim %}"), ("django"), ([]), id="inside a verbatim block"
    ),
    pytest.param(
        ("{% verbatim vue %}{% endverbatim %}{{ a\n}}{% endverbatim vue %}"),
        ("django"),
        ([]),
        id="a named verbatim block closes only on its own name",
    ),
    pytest.param(
        ("{% verbatim vue %}{% endverbatim vue %}{{ a\n}}"),
        ("django"),
        (["1:39"]),
        id="after a named verbatim block",
    ),
    pytest.param(
        ("{# djlint:off D058 #}\n{# a\nb #}\n{# djlint:on #}"),
        ("django"),
        ([]),
        id="inside a djlint:off region for the rule",
    ),
    pytest.param(("{# a\nb #}"), ("jinja"), ([]), id="jinja reads the comment"),
    pytest.param(("{{" * 8000), ("django"), ([]), id="a file of openings nothing closes"),
    pytest.param(
        ("{# a\n" * 4000 + "#}"), ("django"), (["1:0"]), id="a run of openings sharing a closing"
    ),
]


@pytest.mark.parametrize(("source", "profile", "lines"), test_data)
def test_d058(source: str, profile: str, lines: list[str]) -> None:
    filename = "test.html"
    config = Config(filename, profile=profile)

    findings = linter(config, source, filename, filename)[filename]

    assert [error["line"] for error in findings if error["code"] == "D058"] == lines
