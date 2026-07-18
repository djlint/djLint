"""Test twig comment tags.

uv run pytest tests/test_linter/test_h037.py
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
        ('<br class="a" id="asdf" class="b" />'),
        ([
            {
                "code": "H037",
                "line": "1:4",
                "match": "class",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="one",
    ),
    pytest.param(
        ('<div data-class="a" id="asdf" data-class="b"></div>'),
        ([
            {
                "code": "H037",
                "line": "1:5",
                "match": "data-class",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="two",
    ),
    pytest.param(
        ('<div data-class="a" data=asdf class="b"></div>'),
        ([]),
        id="mismatch names",
    ),
    pytest.param(
        ('<input class="foo" placeholder="class=bar"/>'),
        ([]),
        id="name in quoted value",
    ),
    pytest.param(
        (
            '<c-recipe-card url="{{ recipe.url }}" '
            'thumbnail_url="{{ recipe.thumbnail_url }}" />'
        ),
        ([]),
        id="substring in underscore name",
    ),
    pytest.param(('<rect x="2" y="3" rx="1" />'), ([]), id="substring names"),
    pytest.param(
        ('<svg -width="16" -width="2"></svg>'),
        ([
            {
                "code": "H037",
                "line": "1:5",
                "match": "-width",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="leading hyphen names",
    ),
    pytest.param(
        ('<svg width="16" stroke-width="2"></svg>'),
        ([]),
        id="mismatch hyphen names",
    ),
    pytest.param(
        (
            '<button {% if active %} class="on" title="On" '
            '{% else %} class="off" title="Off" {% endif %}></button>'
        ),
        ([]),
        id="attributes in mutually exclusive branches",
    ),
    pytest.param(
        (
            '<button {% if active %} class="on" '
            '{% else %} id="off" {% endif %} class="always"></button>'
        ),
        ([
            {
                "code": "H037",
                "line": "1:24",
                "match": "class",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="attribute inside and outside conditional",
    ),
    pytest.param(
        (
            '<a href="" ></a><a href=""></a><a href=""></a><a href=""></a><a href=""></a><a href=""></a>'
        ),
        ([]),
        id="repeating tags",
    ),
    pytest.param(
        (
            '<img {% if lazyload %}data-{% endif %}srcset="{{ full }}"\n'
            '     {% if lazyload %}srcset="{{ placeholder }}"{% endif %}\n'
            '     class="card-img-top"\n'
            '     width="256"\n'
            '     height="256"\n'
            '     alt="x">'
        ),
        ([]),
        id="issue_2246_conditional_attribute_name_prefix",
    ),
    pytest.param(
        ('<br {% if a %}class="x" {% endif %}class="b" />'),
        ([
            {
                "code": "H037",
                "line": "1:14",
                "match": "class",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="unprefixed name after conditional block still reported",
    ),
    pytest.param(
        (
            '<img src="img.jpg" :src="isLoaded ? url : defaultValue" />\n'
            '<tbody class="bg-white" x-data="{ open{{ item.history_id }}: false }" x-bind:class="open{{ item.history_id }} ? \'bg-gray-50\' : '
            '">'
        ),
        ([
            {
                "code": "H006",
                "line": "1:0",
                "match": '<img src="img.jpg" :',
                "message": "Img tag should have height and width attributes.",
            },
            {
                "code": "H013",
                "line": "1:0",
                "match": '<img src="img.jpg" :',
                "message": "Img tag should have an alt attribute.",
            },
            {
                "code": "H025",
                "line": "2:0",
                "match": '<tbody class="bg-whi',
                "message": "Tag seems to be an orphan.",
            },
        ]),
        id="apline tags no match",
    ),
    pytest.param(
        (
            '<img :src="img.jpg" :src="isLoaded ? url : defaultValue" />\n'
            '<tbody x-bind:class="bg-white" x-data="{ open{{ item.history_id }}: false }" x-bind:class="open{{ item.history_id }} ? \'bg-gray-50\' : '
            '">'
        ),
        ([
            {
                "code": "H006",
                "line": "1:0",
                "match": '<img :src="img.jpg" ',
                "message": "Img tag should have height and width attributes.",
            },
            {
                "code": "H013",
                "line": "1:0",
                "match": '<img :src="img.jpg" ',
                "message": "Img tag should have an alt attribute.",
            },
            {
                "code": "H025",
                "line": "2:0",
                "match": "<tbody x-bind:class=",
                "message": "Tag seems to be an orphan.",
            },
            {
                "code": "H037",
                "line": "1:5",
                "match": ":src",
                "message": "Duplicate attribute found.",
            },
            {
                "code": "H037",
                "line": "2:7",
                "match": "x-bind:class",
                "message": "Duplicate attribute found.",
            },
        ]),
        id="apline tags match",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(
    source: str, expected: list[LintError], basic_config: Config
) -> None:
    filename = "test.html"
    output = linter(basic_config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
