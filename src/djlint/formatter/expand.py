"""Expand html.

1. put html tags on individual lines, if needed.
2. put template tags on individual lines, if needed.
"""

from __future__ import annotations

from functools import cache, partial
from types import MappingProxyType
from typing import TYPE_CHECKING

import regex as re

from djlint.const import (
    COLLAPSIBLE_WHITESPACE,
    HTML_ATOMIC_INLINE_ELEMENTS,
    HTML_INLINE_ELEMENTS,
    HTML_INLINE_LEVEL_ELEMENTS,
    HTML_VOID_ELEMENTS,
)
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    RE_FLAGS_IMX,
    RE_FLAGS_IX,
    RE_FLAGS_MX,
    breaks_an_ignored_block,
    inside_html_attribute,
    inside_ignored_block,
    inside_template_block,
    mask_raw_text_bodies,
)

if TYPE_CHECKING:
    from typing import Final

    from djlint.formatter.tokenizer import TagToken
    from djlint.settings import Config

_HTML_TAG_NAME_PATTERN: Final = re.compile(
    r"^</?\s*([a-zA-Z][-\w:.]*)", cache_pattern=False
)
_TRANSPARENT_ELEMENTS: Final = (
    (HTML_INLINE_LEVEL_ELEMENTS | HTML_VOID_ELEMENTS)
    - HTML_ATOMIC_INLINE_ELEMENTS
    - {"br", "hr"}
)
_BREAK_BEFORE_TAG: Final = "\n%s"
_BREAK_AFTER_TAG: Final = "%s\n"
_TEMPLATE_TAG_NAME_PATTERN: Final = re.compile(
    r"^\{%[-+]?\s*([^\s%]+)", flags=RE_FLAGS_IX, cache_pattern=False
)
_BODY_TEMPLATE_TAG_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*[^\s%]+(?:(?!%}).)*?%}", flags=RE_FLAGS_IX, cache_pattern=False
)
_COMMENT_TEMPLATE_BLOCK_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*comment\b(?:(?!%}).)*?%\}.*?\{%[-+]?\s*endcomment\s*[-+]?%}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_NON_RENDERING_TEMPLATE_TAG_PATTERN: Final = re.compile(
    r"\{\#.*?\#\}|\{%[-+]?.*?%\}|\{\{\s*(?:\#|/|else\b).*?\}\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TRIMMED_TRANSLATION_BLOCK_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*blocktrans(?:late)?\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%\}"
    r".*?"
    r"\{%[-+]?\s*endblocktrans(?:late)?\s*[-+]?%}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TRIMMED_TRANSLATION_OPEN_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*blocktrans(?:late)?\b(?:(?!%}).)*?\btrimmed\b(?:(?!%}).)*?%\}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TRIMMED_TRANSLATION_CLOSE_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*endblocktrans(?:late)?\s*[-+]?%}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_VERBATIM_SET_BLOCK_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*set\b(?!(?:(?!%\}).)*=)(?:(?!%\}).)*?%\}"
    r".*?"
    r"\{%[-+]?\s*endset\s*[-+]?%}",
    flags=RE_FLAGS_IX,
    cache_pattern=False,
)
_TEMPLATE_END_TAG_NAMES: Final = MappingProxyType({
    "endall": "asyncall",
    "endeach": "asynceach",
})
_TEMPLATE_START_TAG_END_NAMES: Final = MappingProxyType({
    "asyncall": "endall",
    "asynceach": "endeach",
})


def _open_close_template_tag_patterns(
    tag_name: str,
) -> tuple[re.Pattern[str], re.Pattern[str]]:
    tag = re.escape(tag_name)
    end_tag = re.escape(
        _TEMPLATE_START_TAG_END_NAMES.get(tag_name, f"end{tag_name}")
    )
    return (
        re.compile(rf"{{%[-+]?\s*{tag}\b(?:(?!%}}).)*?%}}", RE_FLAGS_IX),
        re.compile(rf"{{%[-+]?\s*{end_tag}\b(?:(?!%}}).)*?%}}", RE_FLAGS_IX),
    )


def _tag_name(tag: str) -> str:
    """The lowercased name of an html tag, or "" if this is not one."""
    match = _HTML_TAG_NAME_PATTERN.match(tag)
    return match.group(1).lower() if match else ""


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


_ELEMENTS_THAT_RENDER_NOTHING: Final = frozenset(("script", "style"))


def _past_raw_text_element(
    html: str, index: int, name: str, *, back: bool
) -> int:
    """The position on the far side of a script or style element.

    Its body renders nothing and is not markup, so text on either side of
    the element is adjacent and the body itself never counts as content.
    """
    if back:
        opening = f"<{name}"
        while index > 0:
            index = html.rfind("<", 0, index)
            if index < 0:
                return -1
            if html[index : index + len(opening)].lower() == opening:
                return index
        return -1

    closing = f"</{name}"
    while True:
        found = html.find("<", index)
        if found < 0:
            return -1
        if html[found : found + len(closing)].lower() == closing:
            end = html.find(">", found)
            return len(html) if end < 0 else end + 1
        index = found + 1


def expand_html(html: str, config: Config) -> str:
    """Split single line html into many lines based on tags."""

    @cache
    def html_tokens(value: str) -> tuple[TagToken, ...]:
        return tuple(tokenize_tags(value))

    def without_html_tags(value: str) -> str:
        output: list[str] = []
        previous_end = 0
        for token in html_tokens(value):
            output.append(value[previous_end : token.start])
            previous_end = token.end
        output.append(value[previous_end:])
        return "".join(output)

    marker_prefix = "__DJLINT_WS_LINE_"
    while marker_prefix in html:
        marker_prefix = f"_{marker_prefix}"

    protected_lines: list[str] = []

    def has_rendered_text(value: str) -> bool:
        value = _COMMENT_TEMPLATE_BLOCK_PATTERN.sub("", value)
        value = _TRIMMED_TRANSLATION_BLOCK_PATTERN.sub("", value)
        value = without_html_tags(value)
        value = _NON_RENDERING_TEMPLATE_TAG_PATTERN.sub("", value)
        return bool(value.strip(COLLAPSIBLE_WHITESPACE))

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

    def protect_line(
        line: str, scanned: str, *, inside_trimmed_translation: bool
    ) -> str:
        stripped = scanned.strip()
        if (
            not has_template_block_tag(scanned)
            or (
                stripped.startswith("<")
                and stripped.endswith(">")
                and "</" not in stripped
                and not has_rendered_text(scanned)
            )
            or is_trimmed_translation_content(
                scanned, inside_trimmed_translation=inside_trimmed_translation
            )
            or not (
                has_rendered_text(scanned)
                or _VERBATIM_SET_BLOCK_PATTERN.search(scanned)
            )
        ):
            return line

        marker = f"{marker_prefix}{len(protected_lines)}__"
        protected_lines.append(line)
        return marker

    lines: list[str] = []
    inside_trimmed_translation = False
    for line, scanned in zip(
        html.split("\n"), mask_raw_text_bodies(html).split("\n"), strict=True
    ):
        lines.append(
            protect_line(
                line,
                scanned,
                inside_trimmed_translation=inside_trimmed_translation,
            )
        )
        if _TRIMMED_TRANSLATION_OPEN_PATTERN.search(
            scanned
        ) and not _TRIMMED_TRANSLATION_CLOSE_PATTERN.search(scanned):
            inside_trimmed_translation = True
        if _TRIMMED_TRANSLATION_CLOSE_PATTERN.search(scanned):
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
        tag_tokens = html_tokens(tag)
        if not tag_tokens:
            return False

        tag_token = tag_tokens[0]
        tag_name = tag_token.name.lower()
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

        line_tokens = html_tokens(line)

        if tag_token.closing:
            if out_format != _BREAK_BEFORE_TAG:
                return False
            opening_tokens = tuple(
                token
                for token in line_tokens
                if token.start < match_start
                and not token.closing
                and token.name.lower() == tag_name
            )
            if not opening_tokens:
                return False
            opening_token = opening_tokens[-1]
            opening_tag = line[opening_token.start : opening_token.end]
            if should_break_multiline_opening_tag(opening_tag):
                return False
            body = line[opening_token.end : match_start]
        else:
            if out_format != _BREAK_AFTER_TAG:
                return False
            closing_token = next(
                (
                    token
                    for token in line_tokens
                    if token.start >= match_end
                    and token.closing
                    and token.name.lower() == tag_name
                ),
                None,
            )
            if closing_token is None:
                return False
            body = line[match_end : closing_token.start]

        body_tags = [token.name.lower() for token in html_tokens(body)]
        if tag_name in body_tags:
            return False

        if not without_html_tags(body).strip(COLLAPSIBLE_WHITESPACE):
            return False

        for body_tag in body_tags:
            if body_tag not in HTML_INLINE_ELEMENTS:
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
            if out_format != _BREAK_BEFORE_TAG:
                return False
            open_matches = tuple(open_tag_pattern.finditer(line[:match_start]))
            if not open_matches:
                return False
            body = line[open_matches[-1].end() : match_start]
        else:
            if out_format != _BREAK_AFTER_TAG:
                return False
            close_match = close_tag_pattern.search(line, match_end)
            if not close_match:
                return False
            body = line[match_end : close_match.start()]

        body_without_html = without_html_tags(body)
        if _BODY_TEMPLATE_TAG_PATTERN.search(body_without_html):
            return False

        body_tags = [token.name.lower() for token in html_tokens(body)]
        if not body_without_html.strip(COLLAPSIBLE_WHITESPACE):
            return False

        for body_tag in body_tags:
            if body_tag not in HTML_INLINE_ELEMENTS:
                return False
        return True

    def touches_rendered_content(index: int, *, back: bool) -> bool:
        """Whether rendered content runs right up to this position.

        Looks through tags that lay out nothing of their own, and through
        the inside edge of a box, where whitespace is the edge of that box's
        own content, so what lies beyond it is what would be parted.

        Comments and template statements lay out nothing and are looked
        past; an interpolation renders a value and counts. Where template
        statements break is the template's own business, not this check's.
        """
        while True:
            char = html[index - 1 : index] if back else html[index : index + 1]
            if not char or char in COLLAPSIBLE_WHITESPACE:
                return False
            if char == ("}" if back else "{"):
                pair = (
                    html[index - 2 : index] if back else html[index : index + 2]
                )
                if pair == ("#}" if back else "{#"):
                    found = (
                        html.rfind("{#", 0, index)
                        if back
                        else html.find("#}", index)
                    )
                    if found < 0:
                        return True
                    index = found if back else found + 2
                    continue
                return pair == ("}}" if back else "{{")
            if char != (">" if back else "<"):
                return True
            if back:
                start = html.rfind("<", 0, index)
                if start < 0:
                    return True
                tag, index = html[start:index], start
            else:
                end = html.find(">", index)
                if end < 0:
                    return True
                tag, index = html[index : end + 1], end + 1
            if tag.startswith("<!--"):
                continue
            name = _tag_name(tag)
            if name in _ELEMENTS_THAT_RENDER_NOTHING:
                beyond = _past_raw_text_element(html, index, name, back=back)
                if beyond < 0:
                    return False
                index = beyond
                continue
            if name in HTML_ATOMIC_INLINE_ELEMENTS:
                at_outside_edge = back == tag.startswith("</")
                return name in HTML_VOID_ELEMENTS or at_outside_edge
            if name not in _TRANSPARENT_ELEMENTS:
                return False

    def splits_inline_boxes(out_format: str, match: re.Match[str]) -> bool:
        """Whether a break here would part rendered content that touches.

        A line break between two inline boxes renders as a space, so
        writing one would change the page: "x<img>y" is not "x <img> y".
        Against a block edge, or whitespace already there, css drops it
        either way, and there the break is only this formatter's layout.
        """
        index = match.start(1) if out_format == "\n%s" else match.end(1)
        return touches_rendered_content(
            index, back=True
        ) and touches_rendered_content(index, back=False)

    def add_html_line(out_format: str, match: re.Match[str]) -> str:
        """Add whitespace.

        Do not add whitespace if the tag is in a non indent block.

        Do not add whitespace if the tag is a in a template block.

        Do not add whitespace if the tag is in an html attribute string.
        """
        if out_format == _BREAK_AFTER_TAG:
            if breaks_an_ignored_block(config, html, match.end(1)):
                return match.group(1)
        elif inside_ignored_block(config, html, match):
            return match.group(1)

        if inside_template_block(config, html, match):
            return match.group(1)

        if inside_html_attribute(html, match):
            return match.group(1)

        if config.keep_br_inline and _tag_name(match.group(1)) == "br":
            return match.group(1)

        if should_preserve_inline_body(out_format, match):
            return match.group(1)

        if splits_inline_boxes(out_format, match):
            return match.group(1)

        if out_format == "\n%s" and match.start() == 0:
            return match.group(1)

        return out_format % match.group(1)

    break_before_html_tag = partial(add_html_line, "\n%s")
    break_after_html_tag = partial(add_html_line, "%s\n")

    break_char = config.break_before

    html = re.sub(
        rf"{break_char}\K(</?(?:{html_tags})\b(\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)",
        break_before_html_tag,
        html,
        flags=RE_FLAGS_IX,
    )

    html = re.sub(
        rf"(</?(?:{html_tags})\b(\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)(?!\s*?\n)(?=[^\n])",
        break_after_html_tag,
        html,
        flags=RE_FLAGS_IX,
    )

    def should_i_move_template_tag(
        out_format: str, match: re.Match[str]
    ) -> str:
        """Break against a template tag unless it belongs where it is.

        A tag inside an html tag or an ignored block stays put, and so does
        one already at the start of the file. The enclosing-tag search
        excludes ">" from quoted values so a wild match cannot run past the
        end of a tag (issue #640).
        """
        if inside_ignored_block(config, html, match):
            return match.group(1)

        if inside_html_attribute(html, match):
            return match.group(1)

        if should_preserve_template_body(out_format, match):
            return match.group(1)

        match_start, match_end = match.span()
        if not re.search(
            r"\<(?:"
            + str(config.indent_html_tags)
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

    break_before_template_tag = partial(should_i_move_template_tag, "\n%s")
    break_after_template_tag = partial(should_i_move_template_tag, "%s\n")

    html = re.sub(
        break_char
        + r"\K((?:{%|{{\#)[ ]*?(?:"
        + config.break_template_tags
        + ")[^}]+?[%}]})",
        break_before_template_tag,
        html,
        flags=RE_FLAGS_IMX,
    )

    html = re.sub(
        rf"((?:{{%|{{{{\#)[ ]*?(?:{config.break_template_tags})(?>{config.template_tags}|[^}}])+?[%}}]}})(?=[^\n])",
        break_after_template_tag,
        html,
        flags=RE_FLAGS_IMX,
    )

    if protected_lines:
        html = re.sub(
            rf"{re.escape(marker_prefix)}(\d+)__",
            lambda match: protected_lines[int(match.group(1))],
            html,
        )

    return html
