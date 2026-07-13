"""HTML tokenizer tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.formatter.tokenizer import tokenize_tags
from djlint.reformat import formatter

if TYPE_CHECKING:
    from djlint.settings import Config


def test_tokenize_tags_preserves_source_positions() -> None:
    source = (
        '<div\n data-value="{{ value > limit }}" title="a > b">text</div>'
        "<script><Component data={state.data}/></script>"
        '<li{% if active %} class="active">item</li>'
        '<textarea placeholder="${_("Email Addresses/Usernames")}"></textarea>'
        '<input data-options="${{"label": ">", "nested": {"ok": True}}}">'
        "<!-- <fake> --><![CDATA[<fake>]]>"
    )

    tokens = list(tokenize_tags(source))

    assert [source[token.start : token.end] for token in tokens] == [
        '<div\n data-value="{{ value > limit }}" title="a > b">',
        "</div>",
        "<script>",
        "</script>",
        '<li{% if active %} class="active">',
        "</li>",
        '<textarea placeholder="${_("Email Addresses/Usernames")}">',
        "</textarea>",
        '<input data-options="${{"label": ">", "nested": {"ok": True}}}">',
    ]
    assert source[tokens[0].name_end : tokens[0].attributes_end] == (
        '\n data-value="{{ value > limit }}" title="a > b"'
    )


def test_mako_attribute_is_preserved(basic_config: Config) -> None:
    source = (
        '<input aria-describedby="heading" '
        "${'checked=\"yes\"' if enabled else ''}>"
    )

    assert formatter(basic_config, source) == source + "\n"


def test_nested_mako_attribute_is_preserved(basic_config: Config) -> None:
    source = (
        '<input aria-describedby="heading" '
        '${{"label": ">", "nested": {"ok": True}}}>'
    )

    assert formatter(basic_config, source) == source + "\n"
