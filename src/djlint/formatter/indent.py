"""djLint add indentation to html."""

from __future__ import annotations

import ast
import io
import tokenize
from functools import cache, partial
from typing import TYPE_CHECKING, cast

import json5 as json
import regex as re
from json5.lib import QuoteStyle

from djlint.const import (
    COLLAPSIBLE_WHITESPACE,
    HTML_RAW_TEXT_ELEMENTS,
    HTML_TAG_NAMES,
    HTML_VOID_ELEMENTS,
    TEMPLATE_TAGS_WITH_QUOTED_ARGUMENTS,
)
from djlint.formatter.attributes import format_attributes
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_IS,
    RE_FLAGS_IX,
    inside_html_attribute,
    inside_ignored_block,
    inside_ignored_linter_block,
    is_ignored_block_closing,
    is_ignored_block_opening,
    is_raw_text_block_closing,
    is_raw_text_block_opening,
    is_safe_closing_tag,
)

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_QUOTE_STYLES: Final = {
    "double": QuoteStyle.ALWAYS_DOUBLE,
    "single": QuoteStyle.ALWAYS_SINGLE,
}
_QUOTE_CHARACTERS: Final = {"double": '"', "single": "'"}

_QUOTED_ARGUMENT_TAG_PATTERN: Final = re.compile(
    rf"\{{%[-+]?[ \t]*(?:{TEMPLATE_TAGS_WITH_QUOTED_ARGUMENTS})\b"
    r"(?:(?!%\}).)*?[-+]?%\}",
    RE_FLAGS_IS,
    cache_pattern=False,
)
_TAG_STRING_PATTERN: Final = re.compile(
    r"\"[^\"]*\"|'[^']*'", cache_pattern=False
)

_TAG_SPACING_PATTERN: Final = re.compile(
    r"({%[-+]?)[ ]*?(\w(?:(?!%}).)*?)[ ]*?([-+]?%})", cache_pattern=False
)
_INTERPOLATION_SPACING_PATTERN: Final = re.compile(
    r"({{)[ ]*?(\w(?:(?!}}).)*?)[ ]*?(\+?-?}})", cache_pattern=False
)
_EXTRA_TAG_WHITESPACE_PATTERN: Final = re.compile(
    r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')|[ \t]{2,}", cache_pattern=False
)
_HANDLEBARS_BLOCK_END_PATTERN: Final = re.compile(
    r"({{#(?:each|if)(?:(?!}}).)+?[^ ])(}})", cache_pattern=False
)
_SET_CLOSE_PATTERN: Final = re.compile(
    r"^(?!.*\{\%).*%\}.*$", RE_FLAGS_IMX, cache_pattern=False
)
_SET_CLOSING_BRACE_PATTERN: Final = re.compile(
    r"^[ ]*}|^[ ]*]", RE_FLAGS_IMX, cache_pattern=False
)
_SINGLE_LINE_TEMPLATE_TAG_PATTERN: Final = re.compile(
    r"^\s*\{%[-+]?(?:(?!%}).)*%}\s*$", RE_FLAGS_IMSX, cache_pattern=False
)
_SET_OPEN_PATTERN: Final = re.compile(
    r"^([ ]*{%[ ]*?set)(?!.*%}).*$", RE_FLAGS_IMX, cache_pattern=False
)
_SET_OPENING_BRACE_PATTERN: Final = re.compile(
    r"(\{(?![^{}]*%[}\s])(?=[^{}]*$)|\[(?=[^\]]*$))",
    RE_FLAGS_IMX,
    cache_pattern=False,
)
_TEMPLATE_TAG_CLOSE_PATTERN: Final = re.compile(
    r"\{%[-+]?\s*end|\{\{/", RE_FLAGS_IMX, cache_pattern=False
)
_MULTILINE_TAG_OPEN_PATTERN: Final = re.compile(
    r"(?:\{\{|\{%)(?:(?!\}\}|%\}).)*$", cache_pattern=False
)
_MULTILINE_TAG_CLOSE_PATTERN: Final = re.compile(
    r"^(?:(?!\{\{|\{%).)*?(?:\}\}|%\})", cache_pattern=False
)
_LEADING_CLOSE_BRACKET_PATTERN: Final = re.compile(
    r"[ ]*[)\]}]", cache_pattern=False
)
_TEXTAREA_CLOSE_PATTERN: Final = re.compile(
    r"^\s*</textarea\b", RE_FLAGS_IX, cache_pattern=False
)
_SET_CONTENT_PATTERN: Final = re.compile(
    r"""
    ([ ]*)                # 1: leading indentation
    ({%[-+]?)                # 2: tag open
    [ ]*(set)[ ]+?        # 3: the set keyword
    ((?:(?!%}).)*?)       # 4: assignment contents
    ([-+]?%})                # 5: tag close
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
_FUNCTION_CONTENT_PATTERN: Final = re.compile(
    r"""
    (?P<indent>[ ]*)
    (?P<open>{{-?\+?)
    [ ]*?
    (?P<name>(?:(?!}}).)*?\w)
    (?P<paren>
      \(
      (?:\"[^\"]*+\"|'[^']*+'|[^()]++|(?&paren))*+
      \)
    )
    (?P<index>(?:\[[^\]]*?\]|\.[^\s]+))?
    (?P<gap>[ ]*)
    (?P<close>(?:(?!}}).)*?-?\+?}})
    """,
    RE_FLAGS_IMSX,
    cache_pattern=False,
)


def _attribute_quote_at(html: str, start: int) -> str | None:
    """Return the surrounding HTML attribute quote at start, if any."""
    tag_start = html.rfind("<", 0, start)
    if tag_start == -1:
        return None

    quote = None

    for index in range(tag_start + 1, start):
        char = html[index]

        if quote is not None:
            if char == quote:
                quote = None
            continue

        if char == ">":
            return None

        if char not in {"'", '"'}:
            continue

        attr_index = index - 1
        while attr_index > tag_start and html[attr_index].isspace():
            attr_index -= 1

        if attr_index > tag_start and html[attr_index] == "=":
            quote = char

    return quote


def _offset(line_offsets: list[int], position: tuple[int, int]) -> int:
    row, column = position
    return line_offsets[row - 1] + column


def _format_string_token(token_value: str, quote_style: QuoteStyle) -> str:
    try:
        value = ast.literal_eval(token_value)
    except (SyntaxError, ValueError):
        return token_value

    if not isinstance(value, str):
        return token_value

    return cast(
        "str", json.dumps(value, ensure_ascii=False, quote_style=quote_style)
    )


def _format_string_tokens(contents: str, quote_style: QuoteStyle) -> str:
    try:
        tokens = tuple(tokenize.generate_tokens(io.StringIO(contents).readline))
    except (IndentationError, tokenize.TokenError):
        return contents

    line_offsets = [0]
    for line in contents.splitlines(keepends=True):
        line_offsets.append(line_offsets[-1] + len(line))

    replacements: list[tuple[int, int, str]] = []

    for token in tokens:
        if token.type != tokenize.STRING:
            continue

        replacements.append((
            _offset(line_offsets, token.start),
            _offset(line_offsets, token.end),
            _format_string_token(token.string, quote_style),
        ))

    if not replacements:
        return contents

    formatted: list[str] = []
    last_offset = 0

    for start, end, value in replacements:
        formatted.extend((contents[last_offset:start], value))
        last_offset = end

    formatted.append(contents[last_offset:])
    return "".join(formatted)


def indent_html(rawcode: str, config: Config) -> str:
    """Indent raw code.

    `template_block_stack` holds, for each open template block, the level at
    its opening tag, the depth delta of its first branch and whether the
    branches agree. Closing a block restores its saved level, so html tags
    left unclosed inside it, such as a conditionally rendered wrapper, do
    not leak indentation to the siblings that follow.

    `open_html_indents` holds one entry per html tag left open by an earlier
    line, saying whether closing it gives an indent level back. A line is
    only indented when it starts with the opening tag, so a tag opened after
    text on its line owes nothing. A close with nothing to pair against,
    from a tag opened before this file or from unbalanced markup, dedents
    all the same.

    A line closing more tags than it opens still owes a dedent, whatever
    whole tag happens to end it, as in "</b><small></small>". A branch tag
    such as `{% else %}` or `{% elif %}` instead aligns with its block,
    whatever html the rest of its line closes.

    Markup written after the end of a verbatim block, as in
    "</pre> <span>x", is real markup: the line was skipped as raw, so what
    it leaves open is tracked once the block ends, or the tags closing it
    later take levels from tags opened before the block.
    """
    if config.profile not in {"handlebars", "golang"}:

        def fix_tag_spacing(html: str, match: re.Match[str]) -> str:
            """Respace a template tag, before line lengths are measured.

            The contents of `{% verbatim %}` and `{% raw %}` render
            literally, so only the tag edges are normalized there. Runs of
            whitespace outside a string literal collapse to one (T032).
            """
            if inside_ignored_block(config, html, match):
                return match.group()

            content = match.group(2)
            if not inside_ignored_linter_block(config, html, match):
                content = _EXTRA_TAG_WHITESPACE_PATTERN.sub(
                    lambda m: m.group(1) or " ", content
                ).strip()
            return f"{match.group(1)} {content} {match.group(3)}"

        rawcode = _TAG_SPACING_PATTERN.sub(
            partial(fix_tag_spacing, rawcode), rawcode
        )

        rawcode = _INTERPOLATION_SPACING_PATTERN.sub(
            partial(fix_tag_spacing, rawcode), rawcode
        )

        def fix_tag_quotes(html: str, match: re.Match[str]) -> str:
            """Rewrite a tag's quoted arguments to the configured quote.

            This is what T002 asks for, so the rule stays fixable by
            running the formatter. A string is left alone when it holds the
            quote it would be rewritten to, and so is a tag written inside
            an html attribute, where the attribute's own quotes decide.
            """
            if inside_ignored_block(config, html, match) or (
                inside_html_attribute(html, match)
            ):
                return match.group()

            wanted = _QUOTE_CHARACTERS[config.quote_style]

            def requote(string: re.Match[str]) -> str:
                text = string.group()
                if text.startswith(wanted) or wanted in text[1:-1]:
                    return text
                return f"{wanted}{text[1:-1]}{wanted}"

            return _TAG_STRING_PATTERN.sub(requote, match.group())

        rawcode = _QUOTED_ARGUMENT_TAG_PATTERN.sub(
            partial(fix_tag_quotes, rawcode), rawcode
        )

    elif config.profile == "handlebars":

        def fix_handlebars_template_tags(
            html: str, match: re.Match[str]
        ) -> str:
            if inside_ignored_block(config, html, match):
                return match.group()

            return f"{match.group(1)} {match.group(2)}"

        rawcode = _HANDLEBARS_BLOCK_END_PATTERN.sub(
            partial(fix_handlebars_template_tags, rawcode), rawcode
        )

    rawcode_flat_list = rawcode.split("\n")

    indent = config.indent

    beautified_lines: list[str] = []
    indent_level = 0
    in_set_tag = False
    in_multiline_tag = False
    multiline_tag_level = 0
    multiline_tag_is_block = False
    is_raw_first_line = False
    in_raw_text_tag = False
    is_block_raw = False

    slt_html = config.indent_html_tags
    always_self_closing_html = config.always_self_closing_html_tags
    slt_template = config.single_line_template_tags

    ignored_level = 0

    template_block_stack: list[tuple[int, int | None, bool]] = []

    open_html_indents: list[bool] = []

    ignored_inline_start_pattern = re.compile(
        rf"^\s*?(?:{config.ignored_inline_blocks})", flags=RE_FLAGS_IMX
    )
    golang_slt = (
        r"(?:\{\{-?[ ]*?(?:if|range|with|block|define)\b(?:(?!\}\}).)*?\}\})"
        r"(?:.*?)(?:\{\{-?[ ]*?end[ ]*?-?\}\})"
        if config.profile == "golang"
        else r"(?!x)x"
    )
    single_line_tag_pattern = re.compile(
        rf"""^(?:[^<\s].*?)? # start of a line, optionally with some text
                    (?:
                        <({slt_html})(?:(?:>|\b[^>]+?>)(?:.*?)(?:</(?:\1)>)|\b(?:[^>"']|"[^"]*"|'[^']*')*?\/>) # <span stuff-or-not>stuff</span> or <img stuff /> >>> match 1
                        |(?:<(?:{always_self_closing_html})\b(?:[^>"']|"[^"]*"|'[^']*')*?/?>) # <img stuff />
                        |(?:{{%[-+]?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%[-+]?[ ]*?end(?:\2)\b(?:(?!%}}).)*?%}}) # >>> match 2
                        |{golang_slt}
                        |{config.ignored_inline_blocks}
                    )[ \t]*?
                    (?:
                    .*? # anything
                    (?: # followed by another slt
                        <({slt_html})(?:(?:>|\b[^>]+?>)(?:.*?)(?:</(?:\3)>)|\b(?:[^>"']|"[^"]*"|'[^']*')*?\/>) # <span stuff-or-not>stuff</span> or <img stuff /> >>> match 3
                       |(?:<(?:{always_self_closing_html})\b(?:[^>"']|"[^"]*"|'[^']*')*?/?>) # <img stuff />
                       |(?:{{%[-+]?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%[-+]?[ ]*?end(?:\4)\b(?:(?!%}}).)*?%}}) # >>> match 4
                       |{golang_slt}
                       |{config.ignored_inline_blocks}
                    )[ \t]*?
                    )*? # optional of course
                    [^<]*?$ # with no other tags following until end of line
                """,
        flags=RE_FLAGS_IMX,
    )
    tag_unindent_pattern = re.compile(config.tag_unindent, RE_FLAGS_IMX)
    inline_slt_no_attrs_end_pattern = re.compile(
        rf"(<({slt_html})>)(.*?)(</(\2)>[^<]*?$)", flags=RE_FLAGS_IMX
    )
    inline_slt_attrs_end_pattern = re.compile(
        rf"(<({slt_html})\\b[^>]+?>)(.*?)(</(\2)>[^<]*?$)", flags=RE_FLAGS_IMX
    )
    inline_slt_no_attrs_pattern = re.compile(
        rf"(^<({slt_html})>)(.*?)(</(\2)>)", flags=RE_FLAGS_IMX
    )
    inline_slt_attrs_pattern = re.compile(
        rf"(^<({slt_html})\b[^>]+?>)(.*?)(</(\2)>)", flags=RE_FLAGS_IMX
    )
    tag_unindent_line_pattern = re.compile(
        r"^" + str(config.tag_unindent_line), flags=RE_FLAGS_IMX
    )
    tag_indent_pattern = re.compile(
        r"^(?:" + str(config.tag_indent) + r")", flags=RE_FLAGS_IMX
    )
    custom_html_pattern = (
        re.compile(rf"^(?:{config.custom_html})$", flags=RE_FLAGS_IX)
        if config.custom_html
        else None
    )
    template_start_pattern = re.compile(
        r"(?:\{\{\#|\{%[-+]?)[ ]*?" + str(config.start_template_tags),
        flags=RE_FLAGS_IMX,
    )
    template_indent_pattern = config.template_indent_imx_pattern
    template_unindent_pattern = config.template_unindent_imx_pattern
    prefixed_template_tag_indent_pattern = re.compile(
        r"^[^\S\n]*[\(\[](?:(?:\{\{\#|\{%[-+]?)[ ]*?"
        + str(config.start_template_tags)
        + r")",
        flags=RE_FLAGS_IMX,
    )

    def is_html_tag(name: str) -> bool:
        return name.lower() in HTML_TAG_NAMES or bool(
            custom_html_pattern and custom_html_pattern.match(name)
        )

    def format_html_attributes(value: str) -> str:
        output: list[str] = []
        previous_end = 0
        for token in tokenize_tags(value):
            if (
                token.closing
                or token.declaration
                or not is_html_tag(token.name)
            ):
                continue
            leading_start = token.start
            while leading_start and value[leading_start - 1] in " \t":
                leading_start -= 1
            replacement = format_attributes(config, value, token)
            replacement_start = (
                token.start
                if replacement == value[token.start : token.end]
                else leading_start
            )
            output.extend((value[previous_end:replacement_start], replacement))
            previous_end = token.end
        output.append(value[previous_end:])
        return "".join(output)

    @cache
    def starts_unclosed_html_tag(item: str) -> bool:
        stripped_item = item.lstrip()
        tokens = tokenize_tags(stripped_item)
        opening = next(tokens, None)
        if (
            opening is None
            or opening.start != 0
            or opening.closing
            or opening.declaration
            or opening.self_closing
            or opening.name.lower() in HTML_VOID_ELEMENTS
        ):
            return False

        tag = opening.name.lower()
        depth = 1
        for token in tokens:
            if token.name.lower() != tag:
                continue
            if token.closing:
                depth -= 1
            elif (
                not token.self_closing
                and token.name.lower() not in HTML_VOID_ELEMENTS
            ):
                depth += 1

        return depth > 0

    def formatted_item(item: str) -> str:
        return item.lstrip() if config.preserve_leading_space else item

    def output_ends_with(suffixes: tuple[str, ...]) -> bool:
        for written in reversed(beautified_lines):
            stripped = written.rstrip()
            if stripped:
                return stripped.endswith(suffixes)
        return False

    def scan_html_tags(text: str) -> tuple[int, int]:
        """Count tags left open, and closes of tags opened before this.

        A raw text element holds text, so a "<" inside it opens no tag and
        only its own end tag leaves the element.
        """
        opened = 0
        unclosed_closes = 0
        raw_text_element = ""
        for token in tokenize_tags(text):
            name = token.name.lower()
            if raw_text_element:
                if not (token.closing and name == raw_text_element):
                    continue
                raw_text_element = ""
            elif (
                not token.closing
                and not token.self_closing
                and name in HTML_RAW_TEXT_ELEMENTS
            ):
                raw_text_element = name
            if token.self_closing:
                continue
            if name in HTML_VOID_ELEMENTS or not is_html_tag(name):
                continue
            if not token.closing:
                opened += 1
            elif opened:
                opened -= 1
            else:
                unclosed_closes += 1
        return opened, unclosed_closes

    for item in rawcode_flat_list:
        is_safe_closing_tag_ = is_safe_closing_tag(config, item)
        is_ignored_block_opening_ = is_ignored_block_opening(config, item)
        dedent_after = 0
        indent_level_before = indent_level
        opened_html = 0
        unclosed_closes = 0
        html_dedent = 0
        indented_closes = 0
        closes_nothing_indented = False

        if not is_block_raw and is_ignored_block_opening_:
            is_raw_first_line = True

        if is_ignored_block_opening_:
            is_block_raw = True
            ignored_level += 1

        if is_raw_text_block_opening(config, item):
            in_raw_text_tag = True

        marker_is_shown_as_text = (
            is_safe_closing_tag_
            and in_raw_text_tag
            and not is_raw_text_block_closing(config, item)
        )
        if marker_is_shown_as_text:
            is_safe_closing_tag_ = False

        if (
            not is_block_raw
            and ("{%" in item or "{{" in item)
            and not template_unindent_pattern.match(item.lstrip())
        ):
            close_count = len(template_unindent_pattern.findall(item))
            if close_count:
                open_count = len(template_start_pattern.findall(item))
                dedent_after = max(close_count - open_count, 0)
                if dedent_after:
                    del template_block_stack[-dedent_after:]

        if not is_block_raw and "<" in item:
            opened_html, unclosed_closes = scan_html_tags(item)

            if unclosed_closes:
                popped = min(unclosed_closes, len(open_html_indents))
                indented_closes = 0
                for _ in range(popped):
                    indented_closes += open_html_indents.pop()
                closes_nothing_indented = bool(popped) and not indented_closes
                html_dedent = max(unclosed_closes - opened_html, 0)

        if is_safe_closing_tag_:
            ignored_level = max(ignored_level - 1, 0)
            if is_block_raw and ignored_level == 0:
                is_block_raw = False

        if (not is_block_raw and ignored_inline_start_pattern.search(item)) or (
            not is_block_raw
            and single_line_tag_pattern.search(item)
            and not starts_unclosed_html_tag(item)
            and not template_unindent_pattern.match(item.lstrip())
            and not tag_unindent_line_pattern.match(item.lstrip())
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_CLOSE_PATTERN.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            in_set_tag = False
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_CLOSING_BRACE_PATTERN.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif (
            not is_block_raw
            and in_multiline_tag
            and _MULTILINE_TAG_CLOSE_PATTERN.search(item)
        ):
            tmp_level = (
                multiline_tag_level
                if _LEADING_CLOSE_BRACKET_PATTERN.match(item)
                else multiline_tag_level + 1
            )
            tmp = (indent * tmp_level) + formatted_item(item) + "\n"
            indent_level = multiline_tag_level + (
                1 if multiline_tag_is_block else 0
            )
            if multiline_tag_is_block:
                template_block_stack.append((multiline_tag_level, None, True))
            closes_an_html_tag_too = bool(
                tag_unindent_pattern.search(item.lstrip())
            )
            if closes_an_html_tag_too:
                indent_level = max(indent_level - 1, 0)
            opens_another_multiline_tag = bool(
                _MULTILINE_TAG_OPEN_PATTERN.search(item)
            )
            if opens_another_multiline_tag:
                multiline_tag_level = indent_level
                multiline_tag_is_block = len(
                    template_start_pattern.findall(item)
                ) > len(template_unindent_pattern.findall(item))
                indent_level += 1
            else:
                in_multiline_tag = False

        elif (
            not is_block_raw
            and in_multiline_tag
            and _SET_CLOSING_BRACE_PATTERN.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif (
            not is_block_raw
            and in_multiline_tag
            and _SET_OPENING_BRACE_PATTERN.search(item)
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            indent_level += 1

        elif (
            not is_block_raw
            and not is_safe_closing_tag_
            and tag_unindent_pattern.search(item.lstrip())
            and (
                unclosed_closes > opened_html
                or not (
                    inline_slt_no_attrs_end_pattern.search(item)
                    or inline_slt_attrs_end_pattern.search(item)
                )
            )
            and not starts_unclosed_html_tag(item)
            and not tag_unindent_line_pattern.match(item.lstrip())
        ):
            if inline_slt_no_attrs_pattern.search(
                item
            ) or inline_slt_attrs_pattern.search(item):
                tmp = (indent * indent_level) + formatted_item(item) + "\n"
                indent_level = max(indent_level - 1, 0)
            elif template_block_stack and template_unindent_pattern.match(
                item.lstrip()
            ):
                saved_level, branch_delta, consistent = (
                    template_block_stack.pop()
                )
                delta = indent_level - saved_level - 1
                target = (
                    saved_level + delta
                    if consistent and branch_delta == delta
                    else saved_level
                )
                indent_level = min(max(indent_level - 1, 0), max(target, 0))
                tmp = (
                    (indent * min(indent_level, saved_level))
                    + formatted_item(item)
                    + "\n"
                )
                if config.profile == "golang":
                    glued_openers = len(
                        template_start_pattern.findall(item)
                    ) - (len(template_unindent_pattern.findall(item)) - 1)
                    for _ in range(max(glued_openers, 0)):
                        template_block_stack.append((indent_level, None, True))
                        indent_level += 1
            elif closes_nothing_indented:
                tmp = (indent * indent_level) + formatted_item(item) + "\n"

            else:
                floor = (
                    template_block_stack[-1][0] + 1
                    if template_block_stack
                    else 0
                )
                floor_held = indent_level - 1 < floor
                if floor_held:
                    html_dedent = 0
                indent_level = max(indent_level - 1, floor)
                tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif not is_block_raw and tag_unindent_line_pattern.search(item):
            if template_block_stack:
                saved_level, branch_delta, consistent = template_block_stack[-1]
                delta = indent_level - saved_level - 1
                if branch_delta is None:
                    branch_delta = delta
                elif branch_delta != delta:
                    consistent = False
                template_block_stack[-1] = (
                    saved_level,
                    branch_delta,
                    consistent,
                )
                tmp = (indent * saved_level) + formatted_item(item) + "\n"
                indent_level = saved_level + 1
            else:
                tmp = (
                    (indent * (indent_level - 1)) + formatted_item(item) + "\n"
                )

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and not in_set_tag
            and _SET_OPEN_PATTERN.search(item)
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            indent_level += 1
            in_set_tag = True

        elif (
            not is_block_raw
            and not config.preserve_leading_space
            and not in_set_tag
            and not in_multiline_tag
            and _MULTILINE_TAG_OPEN_PATTERN.search(item)
            and not starts_unclosed_html_tag(item)
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            in_multiline_tag = True
            multiline_tag_level = indent_level
            multiline_tag_is_block = len(
                template_start_pattern.findall(item)
            ) > len(template_unindent_pattern.findall(item))
            indent_level += 1

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_OPENING_BRACE_PATTERN.search(item)
        ) or (
            not is_block_raw
            and (
                tag_indent_pattern.search(item.lstrip())
                or (
                    prefixed_template_tag_indent_pattern.search(item.lstrip())
                    and not _TEMPLATE_TAG_CLOSE_PATTERN.search(item)
                )
            )
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            if template_indent_pattern.match(item.lstrip()):
                template_block_stack.append((indent_level, None, True))
            indent_level += 1

        elif is_raw_first_line or (is_safe_closing_tag_ and not is_block_raw):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif is_block_raw or not item.strip():
            if (
                config.profile
                in {"jinja", "askama", "tera", "liquid", "nunjucks"}
                and is_block_raw
                and _TEXTAREA_CLOSE_PATTERN.search(item)
                and output_ends_with(("-}}", "-%}"))
            ):
                tmp = (indent * indent_level) + item.lstrip() + "\n"
            else:
                tmp = item + "\n"

        elif (
            config.preserve_leading_space
            and _SINGLE_LINE_TEMPLATE_TAG_PATTERN.search(item)
        ):
            tmp = (indent * indent_level) + item.lstrip() + "\n"

        elif not config.preserve_leading_space:
            tmp = (indent * indent_level) + item + "\n"
        else:
            tmp = item + "\n"

        if html_dedent:
            stripped_item = item.lstrip()
            already_given_back = indent_level < indent_level_before
            took_no_level_of_its_own = (
                indent_level == indent_level_before
                or not (
                    stripped_item.startswith("<")
                    and not stripped_item.startswith("</")
                )
            )
            if already_given_back:
                html_dedent = 0
            elif took_no_level_of_its_own:
                html_dedent = min(html_dedent, indented_closes)
            dedent_after += html_dedent

        if opened_html:
            if indent_level > indent_level_before:
                open_html_indents.append(True)
                opened_html -= 1
            elif indent_level < indent_level_before:
                indent_level += 1
                open_html_indents.append(True)
                opened_html -= 1
            open_html_indents.extend([False] * opened_html)

        if dedent_after:
            indent_level = max(indent_level - dedent_after, 0)

        if is_ignored_block_opening_:
            is_block_raw = True
            is_raw_first_line = False

        elif not is_block_raw:
            tmp = format_html_attributes(tmp)

        if (
            not in_raw_text_tag or is_raw_text_block_closing(config, item)
        ) and is_ignored_block_closing(config, item):
            in_raw_text_tag = False
            if not is_safe_closing_tag_:
                ignored_level = max(ignored_level - 1, 0)
            if ignored_level == 0:
                was_block_raw, is_block_raw = is_block_raw, False
                if was_block_raw and "<" in item:
                    tail = ""
                    for close in config.ignored_block_closing_pattern.finditer(
                        item
                    ):
                        tail = item[close.end() :]
                    opened, closed = scan_html_tags(tail)
                    del open_html_indents[len(open_html_indents) - closed :]
                    open_html_indents.extend([False] * opened)

        beautified_lines.append(tmp)

    beautified_code = "".join(beautified_lines)

    def format_data(
        config: Config,
        contents: str,
        tag_size: int,
        leading_space: str,
        *,
        quote_style: QuoteStyle = QuoteStyle.ALWAYS_DOUBLE,
        normalize_string_quotes: bool = False,
    ) -> str:
        """Lay out the contents of a set assignment or function call.

        json.dumps produces relative indentation, which has to be shifted
        by leading_space. The fallback keeps the absolute indentation the
        indent pass already applied, so its lines are joined unshifted.
        Contents spread over several lines that are neither data nor a
        literal have no layout to give them, so they are left as written.
        """
        joiner = "\n"
        try:
            data = json.loads(contents)
            contents = json.dumps(
                data,
                trailing_commas=False,
                ensure_ascii=False,
                quote_keys=True,
                quote_style=quote_style,
            )

            if tag_size + len(contents) >= config.max_line_length:
                contents = json.dumps(
                    data,
                    indent=config.indent_size,
                    trailing_commas=False,
                    ensure_ascii=False,
                    quote_keys=True,
                    quote_style=quote_style,
                )
                joiner = f"\n{leading_space}"

        except Exception:
            try:
                evaluated = str(ast.literal_eval(contents))
                added_parentheses = contents[:1] != "(" and evaluated[:1] == "("
                contents = evaluated[1:-1] if added_parentheses else evaluated
            except Exception:
                if "\n" in contents:
                    return contents.strip(" \t")
                contents = contents.strip()

            if normalize_string_quotes:
                contents = _format_string_tokens(contents, quote_style)

        return joiner.join(contents.splitlines())

    def format_set(config: Config, html: str, match: re.Match[str]) -> str:
        if inside_ignored_block(config, html, match):
            return match.group()

        leading_space = match.group(1)
        open_bracket = match.group(2)
        tag = match.group(3)
        close_bracket = match.group(5)
        contents = match.group(4).strip()
        contents_split = contents.split("=", 1)

        if len(contents_split) > 1:
            contents = (
                contents_split[0].strip()
                + " = "
                + format_data(
                    config,
                    contents_split[-1],
                    len(f"{open_bracket} {tag}  {close_bracket}"),
                    leading_space,
                    quote_style=_QUOTE_STYLES[config.quote_style],
                )
            )

        return f"{leading_space}{open_bracket} {tag} {contents} {close_bracket}"

    def format_function(config: Config, html: str, match: re.Match[str]) -> str:
        if inside_ignored_block(config, html, match):
            return match.group()

        leading_space = match["indent"]
        open_bracket = match["open"]
        tag = match["name"].strip()
        index = match["index"] or ""
        close_bracket = match["close"]
        quote_style = _QUOTE_STYLES[config.quote_style]
        normalize_string_quotes = False

        if config.profile == "jinja":
            outer_quote = _attribute_quote_at(html, match.start("open"))
            match outer_quote:
                case '"':
                    quote_style = QuoteStyle.ALWAYS_SINGLE
                    normalize_string_quotes = True
                case "'":
                    quote_style = QuoteStyle.ALWAYS_DOUBLE
                    normalize_string_quotes = True
                case _:
                    pass

        contents = format_data(
            config,
            match["paren"][1:-1],
            len(f"{open_bracket} {tag}() {close_bracket}"),
            leading_space,
            quote_style=quote_style,
            normalize_string_quotes=normalize_string_quotes,
        )

        separator = (
            " " if close_bracket.lstrip("-+").startswith("}}") else match["gap"]
        )
        return f"{leading_space}{open_bracket} {tag}({contents}){index}{separator}{close_bracket}"

    if not config.no_set_formatting:
        beautified_code = _SET_CONTENT_PATTERN.sub(
            partial(format_set, config, beautified_code), beautified_code
        )

    if not config.no_function_formatting:
        beautified_code = _FUNCTION_CONTENT_PATTERN.sub(
            partial(format_function, config, beautified_code), beautified_code
        )

    if not config.preserve_blank_lines:
        beautified_code = beautified_code.lstrip(COLLAPSIBLE_WHITESPACE)

    return beautified_code.rstrip(COLLAPSIBLE_WHITESPACE) + "\n"
