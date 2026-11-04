"""Compress html.

1. flatten attributes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint._const import (
    HTML_TAG_NAMES,
    HTML_VOID_ELEMENTS,
    QUOTED_ATTRIBUTE_VALUE,
    TEMPLATE_TAG_WHOLE,
)
from djlint._formatter.attributes import normalize_attributes, sort_attributes
from djlint._formatter.class_attributes import encode_attribute_newlines
from djlint._formatter.tokenizer import tokenize_tags
from djlint._helpers import (
    RE_FLAGS_IS,
    RE_FLAGS_ISX,
    child_of_unformatted_block,
    compile_pattern,
    mask_raw_text_bodies,
)

if TYPE_CHECKING:
    from typing import Final

    import regex as re

    from djlint._formatter.tokenizer import TagToken
    from djlint._settings import Config

_TEMPLATE_COMMENT_BLOCK_PATTERN: Final = compile_pattern(
    r"{%[ ]*comment\b(?:(?!%}).)*?%}(?:(?!djlint:(?:off|on)).)*?(?={%[ ]*endcomment[ ]*%})",
    RE_FLAGS_ISX,
)


_TEMPLATE_COMMENT_PROFILES: Final = frozenset((
    "all",
    "askama",
    "django",
    "jinja",
    "nunjucks",
    "tera",
))


_LOOSE_ATTRIBUTE_SPACING_PATTERN: Final = compile_pattern(
    rf"{QUOTED_ATTRIBUTE_VALUE}|{TEMPLATE_TAG_WHOLE}|[ \t]+=[ \t]*|=[ \t]+|[ \t]{{2,}}", RE_FLAGS_IS
)


def _tighten_spacing(match: re.Match[str]) -> str:
    text = match.group()
    if not text.strip():
        return " "
    return "=" if text.strip() == "=" else text


def _normalize_spacing(attributes: str, config: Config) -> str:
    """Drop the slack around "=" and between the attributes of a tag.

    Rebuilding the attributes drops it, so a tag measured with the
    slack is spread and then measures short enough to be put back on
    one line, spreading again on the next run. A tag that stays as
    written keeps its spacing: quoted values and template tags are
    matched first, so their own whitespace is left alone either way.
    """
    if len(attributes.strip()) < config.max_attribute_length:
        return attributes
    return _LOOSE_ATTRIBUTE_SPACING_PATTERN.sub(_tighten_spacing, attributes)


def _same_length_blank(match: re.Match[str]) -> str:
    return " " * len(match.group())


def _tokenizer_source(html: str, config: Config) -> str:
    """Blank out what the tag tokenizer should not read as markup.

    A raw text element holds text: the "<" of `var s = "<div>"` inside a
    `<script>` opens no tag, and rewriting it would change what the page
    shows. Template comments are skipped for the same reason. Each is
    replaced by a blank of the same length, so a token's offsets still
    index the original html.
    """
    html = mask_raw_text_bodies(html)

    if config.profile not in _TEMPLATE_COMMENT_PROFILES:
        return html

    if "{#" in html:
        html = config.unformatted_blocks_pattern.sub(_same_length_blank, html)
    if "comment" in html:
        html = _TEMPLATE_COMMENT_BLOCK_PATTERN.sub(_same_length_blank, html)
    return html


def compress_html(html: str, config: Config) -> str:
    """Compress html."""
    source = _tokenizer_source(html, config)

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

        # A template comment after the last attribute was blanked for the
        # tokenizer, which ends the attributes before it; it is still part
        # of the tag and is kept where it was written.
        attributes_end = token.attributes_end
        close = source.rfind("/" if token.self_closing else ">", attributes_end, token.end)
        if close > attributes_end:
            attributes_end += len(html[attributes_end:close].rstrip())

        raw_attributes = html[token.name_end : attributes_end]
        attributes = ""
        if raw_attributes:
            leading = " " if raw_attributes[0].isspace() else ""
            flattened = " ".join(
                x.strip()
                for x in encode_attribute_newlines(raw_attributes, config).strip().splitlines()
            )
            normalized = normalize_attributes(config, flattened)
            attributes = leading + _normalize_spacing(sort_attributes(config, normalized), config)
        if config.close_void_tags and tag.lower() in HTML_VOID_ELEMENTS:
            close_bracket = " />"
        else:
            close_bracket = " />" if token.self_closing else ">"

        return f"{open_bracket}{tag}{attributes}{close_bracket}"

    output: list[str] = []
    previous_end = 0
    for token in tokenize_tags(source):
        output.extend((html[previous_end : token.start], _clean_tag(token)))
        previous_end = token.end
    output.append(html[previous_end:])
    return "".join(output)
