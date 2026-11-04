"""Test the block tags of twig.

uv run pytest tests/test_twig/test_blocks.py
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
        ("<div>\n{% apply upper %}\n<p>x</p>\n{% endapply %}\n</div>"),
        ("<div>\n    {% apply upper %}\n        <p>x</p>\n    {% endapply %}\n</div>\n"),
        id="apply",
    ),
    pytest.param(
        ("<div>\n{% sandbox %}\n{% include 'a.twig' %}\n{% endsandbox %}\n</div>"),
        (
            "<div>\n"
            "    {% sandbox %}\n"
            '        {% include "a.twig" %}\n'
            "    {% endsandbox %}\n"
            "</div>\n"
        ),
        id="sandbox",
    ),
    pytest.param(
        ("<div>\n{% guard function x %}\n<p>x</p>\n{% else %}\n<p>y</p>\n{% endguard %}\n</div>"),
        (
            "<div>\n"
            "    {% guard function x %}\n"
            "        <p>x</p>\n"
            "    {% else %}\n"
            "        <p>y</p>\n"
            "    {% endguard %}\n"
            "</div>\n"
        ),
        id="guard",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, nunjucks_config: Config) -> None:
    output = formatter(nunjucks_config, source)

    printer(expected, source, output)
    assert expected == output
    assert formatter(nunjucks_config, output) == output
