"""Test twig comment tags.

uv run pytest tests/test_linter/test_h037.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.lint import linter
from tests.conftest import config_builder, lint_printer

if TYPE_CHECKING:
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
        # https://github.com/djlint/djLint/issues/2352
        ('<a data-a.checked="1" data-b.checked="2">x</a>'),
        ([]),
        id="issue_2352_mismatch_dot_names",
    ),
    pytest.param(
        ('<a data-a.checked="1" data-a.checked="2">x</a>'),
        ([
            {
                "code": "H037",
                "line": "1:3",
                "match": "data-a.checked",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="dot names",
    ),
    pytest.param(
        ('<div x-on:click.prevent="a" x-on:keyup.prevent="b"></div>'),
        ([]),
        id="mismatch modifier names",
    ),
    pytest.param(
        ('<div x-on:click.prevent="a" x-on:click.prevent="b"></div>'),
        ([
            {
                "code": "H037",
                "line": "1:5",
                "match": "x-on:click.prevent",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="modifier names",
    ),
    pytest.param(('<input .value="1" value="2">'), ([]), id="leading dot name"),
    pytest.param(
        ('<div 1a="x" 2a="y"></div>'), ([]), id="mismatch digit names"
    ),
    pytest.param(
        ('<div 1a="x" 1a="y"></div>'),
        ([
            {
                "code": "H037",
                "line": "1:5",
                "match": "1a",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="digit names",
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
        (
            '<img {% if lazyload %}data.{% endif %}srcset="{{ full }}"\n'
            '     {% if lazyload %}srcset="{{ placeholder }}"{% endif %}\n'
            '     alt="x">'
        ),
        ([]),
        id="dot_ended_conditional_attribute_name_prefix",
    ),
    pytest.param(
        ('<br {{! c }}class="a" class="b" />'),
        ([
            {
                "code": "H037",
                "line": "1:12",
                "match": "class",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="comment_does_not_prefix_attribute_name",
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


golang_test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/2299
        ('<a {{if .A}}href="a"{{else}}{{/* c */}}href="b"{{end}}>x</a>'),
        ([]),
        id="issue_2299_comment_keeps_branch_tracking",
    ),
    pytest.param(
        ('<a {{if .A}}href="a"{{else}}{{- /* c */ -}}href="b"{{end}}>x</a>'),
        ([]),
        id="trimmed_comment_keeps_branch_tracking",
    ),
    pytest.param(
        ('<a {{/* c */}}href="a" href="b">x</a>'),
        ([
            {
                "code": "H037",
                "line": "1:14",
                "match": "href",
                "message": "Duplicate attribute found.",
            }
        ]),
        id="comment_does_not_hide_duplicate",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: list[LintError]) -> None:
    # H043 is not what these fixtures are about
    config = config_builder({"ignore": "H043"})
    filename = "test.html"
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch


@pytest.mark.parametrize(("source", "expected"), golang_test_data)
def test_golang(source: str, expected: list[LintError]) -> None:
    filename = "test.html"
    config = config_builder({"profile": "golang"})
    output = linter(config, source, filename, filename)

    lint_printer(source, expected, output[filename])

    mismatch = (
        *(x for x in output[filename] if x not in expected),
        *(x for x in expected if x not in output[filename]),
    )
    assert not mismatch
