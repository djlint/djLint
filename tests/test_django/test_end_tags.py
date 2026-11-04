"""Test end tags: the old ifequal blocks, and end tags that close nothing.

uv run pytest tests/test_django/test_end_tags.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint._reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint._settings import Config

test_data = [
    pytest.param(
        ("<div>\n{% ifequal a b %}\n<p>x</p>\n{% else %}\n<p>y</p>\n{% endifequal %}\n</div>"),
        (
            "<div>\n"
            "    {% ifequal a b %}\n"
            "        <p>x</p>\n"
            "    {% else %}\n"
            "        <p>y</p>\n"
            "    {% endifequal %}\n"
            "</div>\n"
        ),
        id="ifequal",
    ),
    pytest.param(
        ("<div>\n{% ifnotequal a b %}\n<p>x</p>\n{% endifnotequal %}\n</div>"),
        ("<div>\n    {% ifnotequal a b %}\n        <p>x</p>\n    {% endifnotequal %}\n</div>\n"),
        id="ifnotequal",
    ),
    pytest.param(
        ("<div>\n{% toc %}\n<p>x</p>\n{% endtoc %}\n</div>"),
        ("<div>\n    {% toc %}\n    <p>x</p>\n    {% endtoc %}\n</div>\n"),
        id="the end of a block djLint does not know stays at its level",
    ),
    pytest.param(
        ("<div>\n<p>a</p>\n{% endif %}\n<p>b</p>\n</div>"),
        ("<div>\n    <p>a</p>\n    {% endif %}\n    <p>b</p>\n</div>\n"),
        id="a stray end tag stays at its level",
    ),
    pytest.param(
        (
            "<div>\n{% filter upper %}\n<p>x</p>\n{% endfilter %}\n"
            "<p>a</p>\n{% endif %}\n<p>b</p>\n</div>"
        ),
        (
            "<div>\n"
            "    {% filter upper %}\n"
            "<p>x</p>\n"
            "{% endfilter %}\n"
            "    <p>a</p>\n"
            "    {% endif %}\n"
            "    <p>b</p>\n"
            "</div>\n"
        ),
        id="a stray end tag after an ignored block stays at its level",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
    assert formatter(django_config, output) == output
