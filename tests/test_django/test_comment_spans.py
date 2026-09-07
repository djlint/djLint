"""Test how far an inline `{# #}` comment reaches.

uv run pytest tests/test_django/test_comment_spans.py
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
        '{# start #}<div class="card-body" id="main-panel">Hi</div>{# end #}\n',
        (
            "{# start #}\n"
            '<div class="card-body"\n'
            '     id="main-panel">Hi</div>\n'
            "{# end #}\n"
        ),
        ({"profile": "django", "max_line_length": 40}),
        id="a comment on either side of a tag does not put the tag out of reach",
    ),
    pytest.param(
        '{# start #}<div class="card-body" id="main-panel">Hi</div>{# end #}\n',
        (
            "{# start #}\n"
            '<div class="card-body" id="main-panel">Hi</div>\n'
            "{# end #}\n"
        ),
        ({"profile": "django"}),
        id="and a limit the tag already fits leaves its attributes joined",
    ),
    pytest.param(
        "{# a #}<div><p>x</p></div>{# b #}<div><p>y</p></div>{# c #}\n",
        (
            "{# a #}\n"
            "<div>\n"
            "    <p>x</p>\n"
            "</div>\n"
            "{# b #}\n"
            "<div>\n"
            "    <p>y</p>\n"
            "</div>\n"
            "{# c #}\n"
        ),
        ({"profile": "django"}),
        id="three comments on one line leave both stretches between them to format",
    ),
    pytest.param(
        "{# a #}<!-- b --><div><p>x</p></div>{# c #}\n",
        ("{# a #}<!-- b -->\n<div>\n    <p>x</p>\n</div>\n{# c #}\n"),
        ({"profile": "django"}),
        id="an html comment between two of them is no different",
    ),
    pytest.param(
        "{# outer {# inner #} tail #}<div><p>x</p></div>\n",
        ("{# outer {# inner #} tail #}\n<div>\n    <p>x</p>\n</div>\n"),
        ({"profile": "django"}),
        id="a comment ends at its first close, since the template engine ends it there too",
    ),
    pytest.param(
        "<div>{# a #}text{# b #}</div>\n",
        "<div>{# a #}text{# b #}</div>\n",
        ({"profile": "django"}),
        id="text between two comments is still text and is left where it is",
    ),
    pytest.param(
        (
            "{# a #}<div><p>x</p></div>{# djlint:off #}\n"
            "<div><p>  y  </p></div>\n"
            "{# djlint:on #}\n"
        ),
        (
            "{# a #}\n"
            "<div>\n"
            "    <p>x</p>\n"
            "</div>\n"
            "{# djlint:off #}\n"
            "<div><p>  y  </p></div>\n"
            "{# djlint:on #}\n"
        ),
        ({"profile": "django"}),
        id="a pragma written after a comment still opens its own region",
    ),
    pytest.param(
        "{# a #}<div><p>x</p></div>{# b #}\n",
        ("{# a #}\n<div>\n    <p>x</p>\n</div>\n{# b #}\n"),
        ({"profile": "nunjucks"}),
        id="nunjucks reads the pair the same way",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    config = config_builder(args)

    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
    assert formatter(config, output) == output
