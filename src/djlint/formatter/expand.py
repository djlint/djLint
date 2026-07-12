"""Expand html.

1. put html tags on individual lines, if needed.
2. put template tags on individual lines, if needed.
"""

from __future__ import annotations

from functools import partial
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

_TAG_NAME_PATTERN = re.compile(
    r"^</?\s*([^\s>/]+)", RE_FLAGS_IX, cache_pattern=False
)
_TEMPLATE_TAG_NAME_PATTERN = re.compile(
    r"^\{%-?\s*([^\s%]+)", flags=RE_FLAGS_IX, cache_pattern=False
)
_BODY_TAG_PATTERN = re.compile(
    r"</?\s*([^\s>/]+)", RE_FLAGS_IX, cache_pattern=False
)
_BODY_HTML_TAG_PATTERN = re.compile(
    r"<[^>\n]*>", RE_FLAGS_IX, cache_pattern=False
)
_BODY_TEMPLATE_TAG_PATTERN = re.compile(
    r"\{%-?\s*[^\s%]+(?:(?!%}).)*?%}", flags=RE_FLAGS_IX, cache_pattern=False
)
_COMMENT_TEMPLATE_BLOCK_PATTERN = re.compile(
    r"\{%-?\s*comment\b(?:(?!%}).)*?%\}.*?\{%-?\s*endcomment\s*-?%\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_NON_RENDERING_TEMPLATE_TAG_PATTERN = re.compile(
    r"\{\#.*?\#\}|\{%-?.*?%\}|\{\{\s*(?:\#|/|else\b).*?\}\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TRIMMED_TRANSLATION_BLOCK_PATTERN = re.compile(
    r"\{%-?\s*blocktrans(?:late)?\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%\}"
    r".*?"
    r"\{%-?\s*endblocktrans(?:late)?\s*-?%\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TRIMMED_TRANSLATION_OPEN_PATTERN = re.compile(
    r"\{%-?\s*blocktrans(?:late)?\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TRIMMED_TRANSLATION_CLOSE_PATTERN = re.compile(
    r"\{%-?\s*endblocktrans(?:late)?\s*-?%\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TEMPLATE_END_TAG_NAMES = {"endall": "asyncall", "endeach": "asynceach"}
_TEMPLATE_START_TAG_END_NAMES = {"asyncall": "endall", "asynceach": "endeach"}


def _open_close_tag_patterns(
    tag_name: str,
) -> tuple[re.Pattern[str], re.Pattern[str]]:
    tag = re.escape(tag_name)
    return (
        re.compile(
            rf"<{tag}\b(?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>",
            RE_FLAGS_IX,
        ),
        re.compile(rf"</{tag}>", RE_FLAGS_IX),
    )


def _open_close_template_tag_patterns(
    tag_name: str,
) -> tuple[re.Pattern[str], re.Pattern[str]]:
    tag = re.escape(tag_name)
    end_tag = re.escape(
        _TEMPLATE_START_TAG_END_NAMES.get(tag_name, f"end{tag_name}")
    )
    return (
        re.compile(rf"{{%-?\s*{tag}\b(?:(?!%}}).)*?%}}", RE_FLAGS_IX),
        re.compile(rf"{{%-?\s*{end_tag}\b(?:(?!%}}).)*?%}}", RE_FLAGS_IX),
    )


def _template_start_tag_name(tag: str) -> str | None:
    tag_name_match = _TEMPLATE_TAG_NAME_PATTERN.match(tag)
    if not tag_name_match:
        return None

    tag_name = tag_name_match.group(1).lower()
    if tag_name in _TEMPLATE_END_TAG_NAMES:
        return _TEMPLATE_END_TAG_NAMES[tag_name]
    if tag_name.startswith("end"):
        return tag_name[3:]
    return tag_name


def _is_closing_template_tag(tag: str) -> bool:
    tag_name_match = _TEMPLATE_TAG_NAME_PATTERN.match(tag)
    return bool(
        tag_name_match and tag_name_match.group(1).lower().startswith("end")
    )


def expand_html(html: str, config: Config) -> str:
    """Split single line html into many lines based on tags."""
    marker_prefix = "__DJLINT_WS_LINE_"
    while marker_prefix in html:
        marker_prefix = f"_{marker_prefix}"

    protected_lines: list[str] = []

    def has_rendered_text(value: str) -> bool:
        value = _COMMENT_TEMPLATE_BLOCK_PATTERN.sub("", value)
        value = _TRIMMED_TRANSLATION_BLOCK_PATTERN.sub("", value)
        value = _BODY_HTML_TAG_PATTERN.sub("", value)
        value = _NON_RENDERING_TEMPLATE_TAG_PATTERN.sub("", value)
        return bool(value.strip())

    def has_template_block_tag(line: str) -> bool:
        return ("{%" in line and "%}" in line) or (
            "{{#" in line and "}}" in line
        )

    def is_trimmed_translation_content(
        line: str, *, inside_trimmed_translation: bool
    ) -> bool:
        open_match = _TRIMMED_TRANSLATION_OPEN_PATTERN.search(line)
        if open_match and has_rendered_text(line[: open_match.start()]):
            return False

        close_match = _TRIMMED_TRANSLATION_CLOSE_PATTERN.search(line)
        if close_match and has_rendered_text(line[close_match.end() :]):
            return False
        if close_match:
            return inside_trimmed_translation

        return inside_trimmed_translation or bool(open_match)

    def protect_line(line: str, *, inside_trimmed_translation: bool) -> str:
        stripped = line.strip()
        if (
            not has_template_block_tag(line)
            or (
                stripped.startswith("<")
                and stripped.endswith(">")
                and "</" not in stripped
            )
            or is_trimmed_translation_content(
                line, inside_trimmed_translation=inside_trimmed_translation
            )
            or not has_rendered_text(line)
        ):
            return line

        marker = f"{marker_prefix}{len(protected_lines)}__"
        protected_lines.append(line)
        return marker

    lines: list[str] = []
    inside_trimmed_translation = False
    for line in html.split("\n"):
        lines.append(
            protect_line(
                line, inside_trimmed_translation=inside_trimmed_translation
            )
        )
        if _TRIMMED_TRANSLATION_OPEN_PATTERN.search(
            line
        ) and not _TRIMMED_TRANSLATION_CLOSE_PATTERN.search(line):
            inside_trimmed_translation = True
        if _TRIMMED_TRANSLATION_CLOSE_PATTERN.search(line):
            inside_trimmed_translation = False
    html = "\n".join(lines)

    html_tags = config.break_html_tags
    optional_single_line_tag_pattern = config.optional_single_line_html_pattern
    optional_single_line_template_tag_pattern = (
        config.optional_single_line_template_pattern
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

        def should_break_multiline_opening_tag(opening_tag: str) -> bool:
            return (
                config.line_break_after_multiline_tag
                and len(opening_tag) >= config.max_attribute_length
            )

        if should_break_multiline_opening_tag(tag):
            return False

        line_start = html.rfind("\n", 0, match.start()) + 1
        line_end = html.find("\n", match.end())
        if line_end == -1:
            line_end = len(html)

        line = html[line_start:line_end]

        match_start = match.start() - line_start
        match_end = match.end() - line_start

        open_tag_pattern, close_tag_pattern = _open_close_tag_patterns(tag_name)

        if tag.startswith("</"):
            if out_format != "\n%s":
                return False
            open_matches = tuple(open_tag_pattern.finditer(line[:match_start]))
            if not open_matches:
                return False
            if should_break_multiline_opening_tag(open_matches[-1].group()):
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

    def should_preserve_template_body(
        out_format: str, match: re.Match[str]
    ) -> bool:
        tag = match.group(1)
        tag_name = _template_start_tag_name(tag)
        if not tag_name or not optional_single_line_template_tag_pattern.match(
            tag_name
        ):
            return False

        line_start = html.rfind("\n", 0, match.start()) + 1
        line_end = html.find("\n", match.end())
        if line_end == -1:
            line_end = len(html)

        line = html[line_start:line_end]

        match_start = match.start() - line_start
        match_end = match.end() - line_start

        open_tag_pattern, close_tag_pattern = _open_close_template_tag_patterns(
            tag_name
        )

        if _is_closing_template_tag(tag):
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

        body_without_html = _BODY_HTML_TAG_PATTERN.sub("", body)
        if _BODY_TEMPLATE_TAG_PATTERN.search(body_without_html):
            return False

        body_tags = [
            body_tag.lower() for body_tag in _BODY_TAG_PATTERN.findall(body)
        ]
        if not body_without_html.strip():
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

        if inside_html_attribute(config, html, match):
            return match.group(1)

        if should_preserve_template_body(out_format, match):
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
    html = re.sub(
        rf"((?:{{%|{{{{\#)[ ]*?(?:{config.break_template_tags})(?>{config.template_tags}|[^}}])+?[%}}]}})(?=[^\n])",
        partial(should_i_move_template_tag, "%s\n"),
        html,
        flags=RE_FLAGS_IMX,
    )

    for index, line in enumerate(protected_lines):
        html = html.replace(f"{marker_prefix}{index}__", line)

    return html
