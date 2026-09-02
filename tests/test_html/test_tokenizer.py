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


def test_unterminated_comment_in_template_comment_keeps_following_tags() -> (
    None
):
    """A stray "<!--" inside a {# #} template comment must not swallow the rest of the document (issue 2266)."""
    source = "<div>\n{# <!-- #}\n</div>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<div>", "</div>"]


def test_unterminated_comment_in_raw_text_element_keeps_following_tags() -> (
    None
):
    source = "<textarea><!--</textarea>\n<p>a</p>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<textarea>", "</textarea>", "<p>", "</p>"]


def test_terminated_comment_still_hides_tags() -> None:
    source = "<div><!-- <span> --></div>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<div>", "</div>"]


def test_less_than_in_mako_expression_in_text_is_not_a_tag() -> None:
    source = "<p>${x<y}</p>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<p>", "</p>"]


def test_less_than_in_variable_expression_in_text_is_not_a_tag() -> None:
    source = "<p>{{a<b}}</p>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<p>", "</p>"]


def test_template_expression_between_tags_does_not_hide_real_tags() -> None:
    source = "{% if a<b %}<div>x</div>{% endif %}"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<div>", "</div>"]


def test_quoted_literal_braces_do_not_escape_attribute() -> None:
    """A quoted literal "{{" must not make the scanner hunt for a "}}" in later content and swallow the tag boundary."""
    source = '<div a="{{">x</div>\n<pre>\n  keep }}  me\n</pre>'

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ['<div a="{{">', "</div>", "<pre>", "</pre>"]


def test_quote_inside_template_tag_does_not_end_attribute() -> None:
    """A template tag nested in an attribute value carries its own quotes; an apostrophe in the translated text must not open a value either."""
    source = (
        '<a href="#" title="{% translate "You don\'t have permission" %}">/</a>'
    )

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == [
        '<a href="#" title="{% translate "You don\'t have permission" %}">',
        "</a>",
    ]


def test_template_expression_with_gt_in_quoted_attribute() -> None:
    source = '<div data-value="{{ value > limit }}" title="a > b">x</div>'

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ['<div data-value="{{ value > limit }}" title="a > b">', "</div>"]


def test_triple_stache_attribute_is_one_tag() -> None:
    source = "<a {{{u}}}></a>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<a {{{u}}}>", "</a>"]


def test_handlebars_raw_block_open_tag_attribute() -> None:
    source = "<a {{{{raw}}}}></a>"

    assert [
        source[token.start : token.end] for token in tokenize_tags(source)
    ] == ["<a {{{{raw}}}}>", "</a>"]


def test_mixed_template_comments_are_compressed(basic_config: Config) -> None:
    source = (
        "{{#unless}}<DIV  id=x></DIV>{{/unless}}{# <DIV  id=x> #}<SPAN></SPAN>"
    )

    assert compress_html(source, basic_config) == (
        '{{#unless}}<div id="x"></div>{{/unless}}{# <DIV  id=x> #}<span></span>'
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


def test_markup_inside_a_raw_text_element_is_text(basic_config: Config) -> None:
    source = (
        "<script>\n"
        '    var s = "<DIV CLASS=x>";\n'
        "</script>\n"
        "<style>\n"
        "    /* <DIV CLASS=x> */\n"
        "</style>\n"
        "<textarea>\n"
        "<DIV CLASS=x>\n"
        "</textarea>\n"
    )

    assert compress_html(source, basic_config) == source
