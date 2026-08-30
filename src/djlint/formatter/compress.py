"""Compress html.

1. flatten attributes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_TAG_NAMES, HTML_VOID_ELEMENTS
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


def _tokenizer_source(html: str, config: Config) -> str:
    """Blank out template comments so the tag tokenizer skips over them.

    Each is replaced by a blank of the same length, so a token's offsets
    still index the original html.
    """
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
        """Flatten multiline attributes back to one line.

        Skip when attribute is ignored.
        Attribute name can be in group one or group 2.
        for now, skipping if they are anywhere

        tags starting ignored blocks can have their attributes formatted,
        for example <textarea class="..." id="..."> can be formatted.
        """
        if child_of_unformatted_block(config, html, token):
            return html[token.start : token.end]

        open_bracket = html[token.start : token.name_start]
        tag = _fix_case(token.name)

        raw_attributes = html[token.name_end : token.attributes_end]
        if raw_attributes:
            raw_attributes = encode_attribute_newlines(raw_attributes, config)

        attributes = (
            (" " if raw_attributes[0].isspace() else "")
            + _normalize_equals(
                " ".join(
                    x.strip() for x in raw_attributes.strip().splitlines()
                ),
                config,
            )
            if raw_attributes
            else ""
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
