"""Test for single_attribute_per_line.

uv run pytest tests/test_config/test_single_attribute_per_line_option.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing import Any


test_data = [
    pytest.param(
        (
            '<input type="text" name="firstName" id="first-name" '
            'autocomplete="given-name" class="form-input mt-1" '
            'value="{{ user.firstName }}" />\n'
        ),
        (
            "<input\n"
            '  type="text"\n'
            '  name="firstName"\n'
            '  id="first-name"\n'
            '  autocomplete="given-name"\n'
            '  class="form-input mt-1"\n'
            '  value="{{ user.firstName }}"\n'
            "/>\n"
        ),
        {"indent": 2, "max_line_length": 1},
        id="prettier_like",
    ),
    pytest.param(
        (
            '<link rel="apple-touch-icon" sizes="180x180" '
            'href="{% static "img/fav/apple-touch-icon.png" %}" />\n'
        ),
        (
            "<link\n"
            '  rel="apple-touch-icon"\n'
            '  sizes="180x180"\n'
            '  href="{% static "img/fav/apple-touch-icon.png" %}"\n'
            "/>\n"
        ),
        {"indent": 2, "max_attribute_length": 1, "profile": "django"},
        id="issue_1877",
    ),
    pytest.param(
        ('<a href = "http://test.test:3000/testtesttesttesttesttesttesttesttesttest">Test</a>\n'),
        ('<a href="http://test.test:3000/testtesttesttesttesttesttesttesttesttest">Test</a>\n'),
        ({"single_attribute_per_line": True}),
        id="space around equals does not oscillate",
    ),
    pytest.param(
        (
            "<ul>\n"
            '<li><a href="{% url \'post\' post.slug %}" class="post-link" '
            'aria-label="Read {{ post.title }}">{{ post.title }}</a></li>\n'
            "</ul>\n"
        ),
        (
            "<ul>\n"
            "    <li><a\n"
            "        href=\"{% url 'post' post.slug %}\"\n"
            '        class="post-link"\n'
            '        aria-label="Read {{ post.title }}"\n'
            "    >{{ post.title }}</a></li>\n"
            "</ul>\n"
        ),
        {"profile": "django"},
        id="tag after another tag indents from the line",
    ),
    pytest.param(
        (
            "<div>\n"
            '<p>Read the <a href="https://example.com/a/very/long/path/to/an/article" '
            'class="external-link" target="_blank">article</a> first.</p>\n'
            "</div>\n"
        ),
        (
            "<div>\n"
            "    <p>Read the <a\n"
            '        href="https://example.com/a/very/long/path/to/an/article"\n'
            '        class="external-link"\n'
            '        target="_blank"\n'
            "    >article</a> first.</p>\n"
            "</div>\n"
        ),
        {},
        id="tag after text indents from the line",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    args = {**args, "single_attribute_per_line": True}
    config = config_builder(args)
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
    assert expected == formatter(config, output)


def test_default_keeps_hanging_indent() -> None:
    source = (
        '<input type="text" name="firstName" id="first-name" '
        'autocomplete="given-name" class="form-input mt-1" />\n'
    )
    output = formatter(config_builder({"indent": 2, "max_line_length": 1}), source)

    assert output.startswith('<input type="text"\n       name=')


def test_default_aligns_attributes_of_a_tag_after_another_tag() -> None:
    source = (
        "<ul>\n"
        '<li><a href="https://example.com/a/very/long/path/to/an/article" '
        'class="post-link" aria-label="Read the article">Article</a></li>\n'
        "</ul>\n"
    )
    expected = (
        "<ul>\n"
        '    <li><a href="https://example.com/a/very/long/path/to/an/article"\n'
        '           class="post-link"\n'
        '           aria-label="Read the article">Article</a></li>\n'
        "</ul>\n"
    )
    config = config_builder({})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
    assert expected == formatter(config, output)


def test_default_aligns_attributes_of_a_tag_after_a_wrapped_tag() -> None:
    source = (
        "<ul>\n"
        '<li class="item item--featured item--with-a-very-long-modifier-name" '
        'data-id="x"><a href="https://example.com/a/very/long/path/to/an/article" '
        'class="post-link" aria-label="Read the article">Article</a></li>\n'
        "</ul>\n"
    )
    expected = (
        "<ul>\n"
        '    <li class="item item--featured item--with-a-very-long-modifier-name"\n'
        '        data-id="x"><a href="https://example.com/a/very/long/path/to/an/article"\n'
        '                       class="post-link"\n'
        '                       aria-label="Read the article">Article</a></li>\n'
        "</ul>\n"
    )
    config = config_builder({})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
    assert expected == formatter(config, output)
