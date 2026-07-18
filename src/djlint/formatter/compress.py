"""Compress html.

1. flatten attributes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_TAG_NAMES, HTML_VOID_ELEMENTS
from djlint.formatter.class_attributes import encode_class_attribute_newlines
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import RE_FLAGS_ISX, child_of_unformatted_block

if TYPE_CHECKING:
    from typing import Final

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config

_TEMPLATE_COMMENT_BLOCK_PATTERN: Final = re.compile(
    r"{%[ ]*?comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*?endcomment[ ]*?%})",
    RE_FLAGS_ISX,
    cache_pattern=False,
)


def _blank_match(match: re.Match[str]) -> str:
    return " " * len(match.group())


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
        if raw_attributes and config.preserve_class_newlines:
            raw_attributes = encode_class_attribute_newlines(
                raw_attributes, config
            )

        attributes = (
            (" " if raw_attributes[0].isspace() else "")
            + " ".join(x.strip() for x in raw_attributes.strip().splitlines())
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
    # Keep offsets while hiding template comments from the HTML tokenizer.
    token_source = html
    if config.profile in {"all", "django", "jinja", "nunjucks"}:
        if "{#" in html:
            token_source = config.unformatted_blocks_pattern.sub(
                _blank_match, token_source
            )
        if "comment" in html:
            token_source = _TEMPLATE_COMMENT_BLOCK_PATTERN.sub(
                _blank_match, token_source
            )
    for token in tokenize_tags(token_source):
        output.extend((html[previous_end : token.start], _clean_tag(token)))
        previous_end = token.end
    output.append(html[previous_end:])
    return "".join(output)
