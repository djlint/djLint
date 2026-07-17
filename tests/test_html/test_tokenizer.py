"""HTML tokenizer tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.formatter.compress import compress_html
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


def test_template_comment_text_does_not_change_tokenization() -> None:
    source = "<script>{#</script><div></div>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<script>", "</script>", "<div>", "</div>"]


def test_mixed_template_comments_are_compressed(basic_config: Config) -> None:
    source = (
        "{{#unless}}<DIV  id=x></DIV>{{/unless}}{# <DIV  id=x> #}<SPAN></SPAN>"
    )

    assert compress_html(source, basic_config) == (
        "{{#unless}}<div id=x></div>{{/unless}}{# <DIV  id=x> #}<span></span>"
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


def test_dynamic_tag_name_is_preserved(django_config: Config) -> None:
    source = "<h{{ header_level }}>{{ value }}</h{{ header_level }}>"

    assert formatter(django_config, source) == source + "\n"
