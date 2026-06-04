"""Expand html.

1. put html tags on individual lines, if needed.
2. put template tags on individual lines, if needed.
"""

from __future__ import annotations

from functools import lru_cache, partial
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IMX,
    RE_FLAGS_IX,
    RE_FLAGS_MX,
    inside_html_attribute,
    inside_ignored_block,
    inside_template_block,
)

if TYPE_CHECKING:
    from djlint.settings import Config

_EXPAND_PATTERN_CACHE_SIZE = 64
_INLINE_CHILD_HTML_TAGS = frozenset({
    "a",
    "abbr",
    "acronym",
    "b",
    "bdi",
    "bdo",
    "big",
    "cite",
    "code",
    "data",
    "del",
    "dfn",
    "em",
    "font",
    "i",
    "ins",
    "kbd",
    "mark",
    "q",
    "s",
    "samp",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "time",
    "u",
    "var",
})

_TAG_NAME_PATTERN = re.compile(r"^</?\s*([^\s>/]+)", flags=RE_FLAGS_IX)
_BODY_TAG_PATTERN = re.compile(r"</?\s*([^\s>/]+)", flags=RE_FLAGS_IX)
_BODY_HTML_TAG_PATTERN = re.compile(r"<[^>\n]*>", flags=RE_FLAGS_IX)


@lru_cache(maxsize=_EXPAND_PATTERN_CACHE_SIZE)
def _optional_single_line_tag_pattern(
    optional_single_line_html_tags: str,
) -> re.Pattern[str]:
    return re.compile(
        rf"^(?:{optional_single_line_html_tags})$", flags=RE_FLAGS_IX
    )


@lru_cache(maxsize=_EXPAND_PATTERN_CACHE_SIZE)
def _open_close_tag_patterns(
    tag_name: str,
) -> tuple[re.Pattern[str], re.Pattern[str]]:
    tag = re.escape(tag_name)
    return (
        re.compile(
            rf"<{tag}\b(?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>",
            flags=RE_FLAGS_IX,
        ),
        re.compile(rf"</{tag}>", flags=RE_FLAGS_IX),
    )


def expand_html(html: str, config: Config) -> str:
    """Split single line html into many lines based on tags."""
    html_tags = config.break_html_tags
    optional_single_line_tag_pattern = _optional_single_line_tag_pattern(
        config.optional_single_line_html_tags
    )

    def should_preserve_inline_body(
        out_format: str, match: re.Match[str]
    ) -> bool:
        tag = match.group(1)
        tag_name_match = _TAG_NAME_PATTERN.match(tag)
        if not tag_name_match:
            return False

        tag_name = tag_name_match.group(1).lower()
        if not optional_single_line_tag_pattern.match(tag_name):
            return False

        line_start = html.rfind("\n", 0, match.start()) + 1
        line_end = html.find("\n", match.end())
        if line_end == -1:
            line_end = len(html)

        line = html[line_start:line_end]
        if len(line) >= config.max_line_length:
            return False

        match_start = match.start() - line_start
        match_end = match.end() - line_start

        open_tag_pattern, close_tag_pattern = _open_close_tag_patterns(tag_name)

        if tag.startswith("</"):
            if out_format != "\n%s":
                return False
            open_matches = tuple(open_tag_pattern.finditer(line[:match_start]))
            if not open_matches:
                return False
            body = line[open_matches[-1].end() : match_start]
        else:
            if out_format != "%s\n":
                return False
            close_match = close_tag_pattern.search(line, match_end)
            if not close_match:
                return False
            body = line[match_end : close_match.start()]

        body_tags = [
            body_tag.lower() for body_tag in _BODY_TAG_PATTERN.findall(body)
        ]
        if tag_name in body_tags:
            return False

        if not _BODY_HTML_TAG_PATTERN.sub("", body).strip():
            return False

        for body_tag in body_tags:
            if body_tag not in _INLINE_CHILD_HTML_TAGS:
                return False

        return True

    def add_html_line(out_format: str, match: re.Match[str]) -> str:
        """Add whitespace.

        Do not add whitespace if the tag is in a non indent block.

        Do not add whitespace if the tag is a in a template block.

        Do not add whitespace if the tag is in an html attribute string.
        """
        if inside_ignored_block(config, html, match):
            return match.group(1)

        if inside_template_block(config, html, match):
            return match.group(1)

        if inside_html_attribute(config, html, match):
            return match.group(1)

        if should_preserve_inline_body(out_format, match):
            return match.group(1)

        if out_format == "\n%s" and match.start() == 0:
            return match.group(1)

        return out_format % match.group(1)

    add_left = partial(add_html_line, "\n%s")
    add_right = partial(add_html_line, "%s\n")

    break_char = config.break_before

    # html tags - break before
    html = re.sub(
        rf"{break_char}\K(</?(?:{html_tags})\b(\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)",
        add_left,
        html,
        flags=RE_FLAGS_IX,
    )

    # html tags - break after
    html = re.sub(
        rf"(</?(?:{html_tags})\b(\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)(?!\s*?\n)(?=[^\n])",
        add_right,
        html,
        flags=RE_FLAGS_IX,
    )

    # template tag breaks
    def should_i_move_template_tag(
        out_format: str, match: re.Match[str]
    ) -> str:
        # ensure template tag is not inside an html tag and also not the first line of the file
        if inside_ignored_block(config, html, match):
            return match.group(1)
        match_start, match_end = match.span()
        if not re.search(
            r"\<(?:"
            + str(config.indent_html_tags)
            # added > as not allowed inside a "" or '' to prevent invalid wild html matches
            # for issue #640
            + r")\b(?:\"[^\">]*\"|'[^'>]*'|{{[^}]*}}|{%[^%]*%}|{\#[^\#]*\#}|[^>{}])*?"
            + re.escape(match.group(1))
            + "$",
            html[:match_end],
            flags=RE_FLAGS_MX,
        ):
            if out_format == "\n%s" and match_start == 0:
                return match.group(1)
            return out_format % match.group(1)

        return match.group(1)

    # template tags
    # break before
    html = re.sub(
        break_char
        + r"\K((?:{%|{{\#)[ ]*?(?:"
        + config.break_template_tags
        + ")[^}]+?[%}]})",
        partial(should_i_move_template_tag, "\n%s"),
        html,
        flags=RE_FLAGS_IMX,
    )

    # break after
    return re.sub(
        rf"((?:{{%|{{{{\#)[ ]*?(?:{config.break_template_tags})(?>{config.template_tags}|[^}}])+?[%}}]}})(?=[^\n])",
        partial(should_i_move_template_tag, "%s\n"),
        html,
        flags=RE_FLAGS_IMX,
    )
