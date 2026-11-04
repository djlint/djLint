"""HTML tokenizer tests."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pytest

from djlint._formatter.compress import compress_html
from djlint._formatter.tokenizer import tokenize_tags
from djlint._reformat import formatter

if TYPE_CHECKING:
    from djlint._settings import Config


FAR = " " * 2000000


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

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<script>",
        "</script>",
        "<div>",
        "</div>",
    ]


def test_unterminated_comment_in_template_comment_keeps_following_tags() -> None:
    """A stray "<!--" inside a {# #} template comment must not swallow the rest of the document (issue 2266)."""
    source = "<div>\n{# <!-- #}\n</div>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<div>",
        "</div>",
    ]


def test_unterminated_comment_in_raw_text_element_keeps_following_tags() -> None:
    source = "<textarea><!--</textarea>\n<p>a</p>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<textarea>",
        "</textarea>",
        "<p>",
        "</p>",
    ]


def test_terminated_comment_still_hides_tags() -> None:
    source = "<div><!-- <span> --></div>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<div>",
        "</div>",
    ]


def test_less_than_in_mako_expression_in_text_is_not_a_tag() -> None:
    source = "<p>${x<y}</p>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == ["<p>", "</p>"]


def test_less_than_in_variable_expression_in_text_is_not_a_tag() -> None:
    source = "<p>{{a<b}}</p>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == ["<p>", "</p>"]


def test_template_expression_between_tags_does_not_hide_real_tags() -> None:
    source = "{% if a<b %}<div>x</div>{% endif %}"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<div>",
        "</div>",
    ]


def test_quoted_literal_braces_do_not_escape_attribute() -> None:
    """A quoted literal "{{" must not make the scanner hunt for a "}}" in later content and swallow the tag boundary."""
    source = '<div a="{{">x</div>\n<pre>\n  keep }}  me\n</pre>'

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        '<div a="{{">',
        "</div>",
        "<pre>",
        "</pre>",
    ]


def test_later_quote_does_not_close_quoted_literal_braces() -> None:
    source = '<div a="{{">text }} "> <SPAN>next</SPAN></div>'

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        '<div a="{{">',
        "<SPAN>",
        "</SPAN>",
        "</div>",
    ]


def test_gt_in_template_string_in_quoted_attribute() -> None:
    """The template string reuses the attribute's quote, so its ">" is data."""
    tag = "<div class=\"{{ classes|default:\" [&>a]:flex\" }} block\" class='{% firstof a '>' %}'>"
    source = f"{tag}x</div>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [tag, "</div>"]


def test_a_run_of_unclosed_braces_is_read_once() -> None:
    """Twenty thousand "{{" in a value took forty seconds.

    Each brace counted the rest of the run and searched the rest of the
    file for a closing one.
    """
    source = '<a title="' + "{{" * 20000 + '">x</a>'

    started = time.perf_counter()
    tokens = [source[token.start : token.end] for token in tokenize_tags(source)]

    assert tokens == [source[: source.index(">") + 1], "</a>"]
    assert time.perf_counter() - started < 1


@pytest.mark.parametrize(
    "run", [pytest.param("${ x ", id="side by side"), pytest.param("${ {", id="nested")]
)
def test_a_run_of_unclosed_mako_expressions_is_read_once(run: str) -> None:
    """Six thousand "${ x " in a paragraph took three seconds to read.

    The formatter reads a template some twenty times. Each expression was
    read to the end of the file, and so was each one opening inside it,
    again from each.
    """
    source = "<p>" + run * 6000 + "</p><a b='${x}}'>y</a>"

    started = time.perf_counter()
    tokens = [source[token.start : token.end] for token in tokenize_tags(source)]

    assert tokens == ["<p>", "</p>", "<a b='${x}}'>", "</a>"]
    assert time.perf_counter() - started < 1


def test_an_expression_inside_an_unclosed_one_can_close() -> None:
    source = "<p>${ a ${b<c} <i>x</i></p>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<p>",
        "<i>",
        "</i>",
        "</p>",
    ]


def test_a_value_that_never_closes_ends_the_scan() -> None:
    source = '<p>x</p><a b="c>y</a><i>'

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == ["<p>", "</p>"]


def test_a_template_past_the_closing_quote_keeps_the_value_open() -> None:
    """The first '"' after the opening one lies inside the template."""
    tag = """<a b="{{ c|default:"d" }}e" f='{% g 'h' %}' i="$" j="${k["l"]}">"""
    source = f"{tag}x</a>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [tag, "</a>"]


@pytest.mark.parametrize(
    ("source", "tags"),
    [
        pytest.param(
            '<b c="d" "="" e="f"><i title="h">',
            ['<b c="d" "="" e="f">', '<i title="h">'],
            id="a stray quote is part of an attribute name",
        ),
        pytest.param(
            "<p title=a'b>x</p><i>",
            ["<p title=a'b>", "</p>", "<i>"],
            id="a quote in a bare value is part of the value",
        ),
    ],
)
def test_only_a_quote_after_equals_opens_a_value(source: str, tags: list[str]) -> None:
    assert [source[token.start : token.end] for token in tokenize_tags(source)] == tags


def test_a_tag_quoted_in_an_abandoned_tag_is_read() -> None:
    """A brace abandons the outer tag, so the scan goes back to the next "<"."""
    source = '<a x="<b c>" }'

    assert [token.name for token in tokenize_tags(source)] == ["b"]


@pytest.mark.parametrize(
    ("source", "names"),
    [
        pytest.param("<div {x}> " * 20000 + FAR, [], id="brace-in-tag"),
        pytest.param("<b }" * 20000 + FAR, [], id="closing-brace"),
        pytest.param("$ " * 400000 + "{<a>", ["a"], id="dollars-in-text"),
        pytest.param('<a b="' + "$" * 40000 + '">' + FAR + "{", ["a"], id="dollars-in-value"),
        pytest.param(
            '<p>$5</p><a b="' + "{ " * 40000 + '">' + FAR, ["p", "p", "a"], id="braces-in-value"
        ),
    ],
)
def test_a_stop_in_a_tag_reads_no_further_than_the_next(source: str, names: list[str]) -> None:
    """Each stop must cost its own distance, not a search of the whole file.

    The run of spaces is what a search for a character the page doesn't
    use would read from every stop.
    """
    started = time.perf_counter()
    tokens = [token.name for token in tokenize_tags(source)]

    assert tokens == names
    assert time.perf_counter() - started < 1


def test_quote_inside_template_tag_does_not_end_attribute() -> None:
    """A template tag nested in an attribute value carries its own quotes; an apostrophe in the translated text must not open a value either."""
    source = '<a href="#" title="{% translate "You don\'t have permission" %}">/</a>'

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        '<a href="#" title="{% translate "You don\'t have permission" %}">',
        "</a>",
    ]


def test_template_expression_with_gt_in_quoted_attribute() -> None:
    source = '<div data-value="{{ value > limit }}" title="a > b">x</div>'

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        '<div data-value="{{ value > limit }}" title="a > b">',
        "</div>",
    ]


def test_triple_stache_attribute_is_one_tag() -> None:
    source = "<a {{{u}}}></a>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<a {{{u}}}>",
        "</a>",
    ]


def test_handlebars_raw_block_open_tag_attribute() -> None:
    source = "<a {{{{raw}}}}></a>"

    assert [source[token.start : token.end] for token in tokenize_tags(source)] == [
        "<a {{{{raw}}}}>",
        "</a>",
    ]


def test_mixed_template_comments_are_compressed(basic_config: Config) -> None:
    source = "{{#unless}}<DIV  id=x></DIV>{{/unless}}{# <DIV  id=x> #}<SPAN></SPAN>"

    assert compress_html(source, basic_config) == (
        '{{#unless}}<div id="x"></div>{{/unless}}{# <DIV  id=x> #}<span></span>'
    )


def test_mako_attribute_is_preserved(basic_config: Config) -> None:
    source = "<input aria-describedby=\"heading\" ${'checked=\"yes\"' if enabled else ''}>"

    assert formatter(basic_config, source) == source + "\n"


def test_nested_mako_attribute_is_preserved(basic_config: Config) -> None:
    source = '<input aria-describedby="heading" ${{"label": ">", "nested": {"ok": True}}}>'

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


@pytest.mark.parametrize(
    ("source", "tags"),
    [
        pytest.param(
            r'<input value="${ "a\"}" }"><p>',
            [r'<input value="${ "a\"}" }">', "<p>"],
            id="an escaped quote in a mako string",
        ),
        pytest.param(
            r'<a title={{ "x\">" }}><p>',
            [r'<a title={{ "x\">" }}>', "<p>"],
            id="an escaped quote in a template string",
        ),
        pytest.param(
            r'<a title="{{ "x\">" }}"><p>',
            [r'<a title="{{ "x\">" }}">', "<p>"],
            id="an escaped quote in a template string in a quoted value",
        ),
        pytest.param("<p>${ x <b>", ["<p>", "<b>"], id="a mako expression that never closes"),
        pytest.param("<p>{{<b>x</b>", ["<p>", "<b>", "</b>"], id="braces opening on a tag"),
        pytest.param("<![CDATA[ <p>", ["<p>"], id="a cdata section that never closes"),
    ],
)
def test_escaped_quotes_and_openers_left_open(source: str, tags: list[str]) -> None:
    assert [source[token.start : token.end] for token in tokenize_tags(source)] == tags
