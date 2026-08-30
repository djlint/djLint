"""Compress html.

1. flatten attributes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_TAG_NAMES, HTML_VOID_ELEMENTS
from djlint.formatter.attributes import normalize_attributes
from djlint.formatter.class_attributes import encode_attribute_newlines
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import RE_FLAGS_IS, RE_FLAGS_ISX, child_of_unformatted_block

if TYPE_CHECKING:
    from typing import Final

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config

_TEMPLATE_COMMENT_BLOCK_PATTERN: Final = re.compile(
    r"{%[ ]*comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*endcomment[ ]*%})",
    RE_FLAGS_ISX,
    cache_pattern=False,
)


_TEMPLATE_COMMENT_PROFILES: Final = frozenset((
    "all",
    "askama",
    "django",
    "jinja",
    "nunjucks",
    "tera",
))


_RAW_TEXT_ELEMENT_PATTERN: Final = re.compile(
    r"""
    (<(script|style|textarea)\b
      (?:\"[^\"]*\"|'[^']*'|\{[^}]*\}|[^'\">{}])*>)
    (.*?)
    (?=</\2)
    """,
    RE_FLAGS_ISX,
    cache_pattern=False,
)

_PADDED_EQUALS_PATTERN: Final = re.compile(
    r"\"[^\"]*\"|'[^']*'|\{\{.*?\}\}|\{%.*?%\}|\{\#.*?\#\}|[ \t]+=[ \t]*|=[ \t]+",
    RE_FLAGS_IS,
    cache_pattern=False,
)


def _tighten_equals(match: re.Match[str]) -> str:
    text = match.group()
    return "=" if text.strip() == "=" else text


def _normalize_equals(attributes: str, config: Config) -> str:
    """Drop the padding around "=" in a tag that will be spread.

    Rebuilding the attributes drops it, so a tag measured with the
    padding is spread and then measures short enough to be put back on
    one line, spreading again on the next run. A tag that stays as
    written keeps its padding: quoted values and template tags are
    matched first, so their own whitespace is left alone either way.
    """
    if len(attributes.strip()) < config.max_attribute_length:
        return attributes
    return _PADDED_EQUALS_PATTERN.sub(_tighten_equals, attributes)


def _same_length_blank(match: re.Match[str]) -> str:
    return " " * len(match.group())


def _blank_raw_text(match: re.Match[str]) -> str:
    return match.group(1) + " " * len(match.group(3))


def _tokenizer_source(html: str, config: Config) -> str:
    """Blank out what the tag tokenizer should not read as markup.

    A raw text element holds text: the "<" of `var s = "<div>"` inside a
    `<script>` opens no tag, and rewriting it would change what the page
    shows. Template comments are skipped for the same reason. Each is
    replaced by a blank of the same length, so a token's offsets still
    index the original html.
    """
    html = _RAW_TEXT_ELEMENT_PATTERN.sub(_blank_raw_text, html)

    if config.profile not in _TEMPLATE_COMMENT_PROFILES:
        return html

    if "{#" in html:
        html = config.unformatted_blocks_pattern.sub(_same_length_blank, html)
    if "comment" in html:
        html = _TEMPLATE_COMMENT_BLOCK_PATTERN.sub(_same_length_blank, html)
    return html


def compress_html(html: str, config: Config) -> str:
    """Compress html."""

    def _fix_case(tag: str) -> str:
        if not config.ignore_case and tag.lower() in HTML_TAG_NAMES:
            return tag.lower()

        if not config.ignore_case and tag.lower() == "doctype":
            return "DOCTYPE"
        return tag

    def _clean_tag(token: TagToken) -> str:
        """Flatten multiline attributes back to one line and quote values.

        A tag opening an ignored block still has its own attributes
        formatted, so `<textarea class="..." id="...">` is tidied while its
        contents are left alone.
        """
        if child_of_unformatted_block(config, html, token):
            return html[token.start : token.end]

        open_bracket = html[token.start : token.name_start]
        tag = _fix_case(token.name)

        raw_attributes = html[token.name_end : token.attributes_end]
        attributes = ""
        if raw_attributes:
            leading = " " if raw_attributes[0].isspace() else ""
            flattened = " ".join(
                x.strip()
                for x in encode_attribute_newlines(raw_attributes, config)
                .strip()
                .splitlines()
            )
            attributes = leading + _normalize_equals(
                normalize_attributes(config, flattened), config
            )
        if config.close_void_tags and tag.lower() in HTML_VOID_ELEMENTS:
            close_bracket = " />"
        else:
            close_bracket = " />" if token.self_closing else ">"

        return f"{open_bracket}{tag}{attributes}{close_bracket}"

    output: list[str] = []
    previous_end = 0
    for token in tokenize_tags(_tokenizer_source(html, config)):
        output.extend((html[previous_end : token.start], _clean_tag(token)))
        previous_end = token.end
    output.append(html[previous_end:])
    return "".join(output)
