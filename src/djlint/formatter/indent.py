"""djLint add indentation to html."""

from __future__ import annotations

import ast
import io
import tokenize
from functools import partial
from typing import TYPE_CHECKING, cast

import json5 as json
import regex as re
from json5.lib import QuoteStyle

from djlint.formatter.attributes import format_attributes
from djlint.helpers import (
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_IX,
    inside_ignored_block,
    is_ignored_block_closing,
    is_ignored_block_opening,
    is_safe_closing_tag,
    is_script_style_block_closing,
    is_script_style_block_opening,
)

if TYPE_CHECKING:
    from djlint.settings import Config


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
    """Indent raw code."""
    if config.profile not in {"handlebars", "golang"}:
        # we can try to fix template tags. ignore handlebars
        # this should be done before indenting to line length
        # calc is preserved.

        def fix_tag_spacing(html: str, match: re.Match[str]) -> str:
            if inside_ignored_block(config, html, match):
                return match.group()

            return f"{match.group(1)} {match.group(2)} {match.group(3)}"

        """
        We should have tags like this:
        {{ tag }}
        {%- tag atrib -%}
        """
        func = partial(fix_tag_spacing, rawcode)

        rawcode = re.sub(
            r"({%-?\+?)[ ]*?(\w(?:(?!%}).)*?)[ ]*?(\+?-?%})", func, rawcode
        )

        rawcode = re.sub(
            r"({{)[ ]*?(\w(?:(?!}}).)*?)[ ]*?(\+?-?}})", func, rawcode
        )

    elif config.profile == "handlebars":

        def fix_handlebars_template_tags(
            html: str, match: re.Match[str]
        ) -> str:
            if inside_ignored_block(config, html, match):
                return match.group()

            return f"{match.group(1)} {match.group(2)}"

        func = partial(fix_handlebars_template_tags, rawcode)
        # handlebars templates
        rawcode = re.sub(r"({{#(?:each|if).+?[^ ])(}})", func, rawcode)

    rawcode_flat_list = re.split(r"\n", rawcode)

    indent = config.indent

    beautified_code = ""
    indent_level = 0
    in_set_tag = False
    is_raw_first_line = False
    in_script_style_tag = False
    is_block_raw = False

    slt_html = config.indent_html_tags

    # here using all tags cause we allow empty tags on one line
    always_self_closing_html = config.always_self_closing_html_tags

    # here using all tags cause we allow empty tags on one line
    slt_template = config.optional_single_line_template_tags

    # nested ignored blocks..
    ignored_level = 0

    ignored_inline_start_pattern = re.compile(
        rf"^\s*?(?:{config.ignored_inline_blocks})", flags=RE_FLAGS_IMX
    )
    single_line_tag_pattern = re.compile(
        rf"""^(?:[^<\s].*?)? # start of a line, optionally with some text
                    (?:
                        <({slt_html})(?:(?:>|\b[^>]+?>)(?:.*?)(?:</(?:\1)>)|\b(?:[^>"']|"[^"]*"|'[^']*')*?\/>) # <span stuff-or-not>stuff</span> or <img stuff /> >>> match 1
                        |(?:<(?:{always_self_closing_html})\b[^>]*?/?>) # <img stuff />
                        |(?:{{%-?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%-?[ ]*?end(?:\2)\b(?:(?!%}}).)*?%}}) # >>> match 2
                        |{config.ignored_inline_blocks}
                    )[ \t]*?
                    (?:
                    .*? # anything
                    (?: # followed by another slt
                        <({slt_html})(?:(?:>|\b[^>]+?>)(?:.*?)(?:</(?:\3)>)|\b(?:[^>"']|"[^"]*"|'[^']*')*?\/>) # <span stuff-or-not>stuff</span> or <img stuff /> >>> match 3
                       |(?:<(?:{always_self_closing_html})\b[^>]*?/?>) # <img stuff />
                       |(?:{{%-?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%-?[ ]*?end(?:\4)\b(?:(?!%}}).)*?%}}) # >>> match 4
                       |{config.ignored_inline_blocks}
                    )[ \t]*?
                    )*? # optional of course
                    [^<]*?$ # with no other tags following until end of line
                """,
        flags=RE_FLAGS_IMX,
    )
    set_close_pattern = re.compile(r"^(?!.*\{\%).*%\}.*$", flags=RE_FLAGS_IMX)
    set_closing_brace_pattern = re.compile(r"^[ ]*}|^[ ]*]", flags=RE_FLAGS_IMX)
    tag_unindent_pattern = re.compile(config.tag_unindent, flags=RE_FLAGS_IMX)
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
    set_open_pattern = re.compile(
        r"^([ ]*{%[ ]*?set)(?!.*%}).*$", flags=RE_FLAGS_IMX
    )
    set_opening_brace_pattern = re.compile(
        r"(\{(?![^{}]*%[}\s])(?=[^{}]*$)|\[(?=[^\]]*$))", flags=RE_FLAGS_IMX
    )
    tag_indent_pattern = re.compile(
        r"^(?:" + str(config.tag_indent) + r")", flags=RE_FLAGS_IMX
    )
    indent_html_tags_pattern = re.compile(
        config.indent_html_tags_regex, flags=RE_FLAGS_IX
    )

    for item in rawcode_flat_list:
        is_safe_closing_tag_ = is_safe_closing_tag(config, item)
        is_ignored_block_opening_ = is_ignored_block_opening(config, item)

        # if a raw tag first line
        if not is_block_raw and is_ignored_block_opening_:
            is_raw_first_line = True

        # if a raw tag then start ignoring
        if is_ignored_block_opening_:
            is_block_raw = True
            ignored_level += 1

        if is_script_style_block_opening(config, item):
            in_script_style_tag = True

        if is_safe_closing_tag_:
            ignored_level -= 1
            ignored_level = max(ignored_level, 0)
            if is_block_raw and ignored_level == 0:
                is_block_raw = False

        if (not is_block_raw and ignored_inline_start_pattern.search(item)) or (
            not is_block_raw and single_line_tag_pattern.search(item)
        ):
            tmp = (indent * indent_level) + item + "\n"

        # closing set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and set_close_pattern.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            in_set_tag = False
            tmp = (indent * indent_level) + item + "\n"

        # closing curly brace inside a set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and set_closing_brace_pattern.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + item + "\n"

        # if unindent, move left
        elif (
            not is_block_raw
            and not is_safe_closing_tag_
            and tag_unindent_pattern.search(item)
            # and not ending in a slt like <span><strong></strong>.
            and not inline_slt_no_attrs_end_pattern.search(item)
            and not inline_slt_attrs_end_pattern.search(item)
        ):
            # block to catch inline block followed by a non-break tag
            if inline_slt_no_attrs_pattern.search(
                item
            ) or inline_slt_attrs_pattern.search(item):
                # unindent after instead of before
                tmp = (indent * indent_level) + item + "\n"
                indent_level = max(indent_level - 1, 0)
            else:
                indent_level = max(indent_level - 1, 0)
                tmp = (indent * indent_level) + item + "\n"

        elif not is_block_raw and tag_unindent_line_pattern.search(item):
            tmp = (indent * (indent_level - 1)) + item + "\n"

        # if indent, move right

        # opening set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and not in_set_tag
            and set_open_pattern.search(item)
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level += 1
            in_set_tag = True

        # opening curly brace inside a set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and set_opening_brace_pattern.search(item)
        ) or (tag_indent_pattern.search(item) and not is_block_raw):
            tmp = (indent * indent_level) + item + "\n"
            indent_level += 1

        elif is_raw_first_line or (is_safe_closing_tag_ and not is_block_raw):
            tmp = (indent * indent_level) + item + "\n"

        elif is_block_raw or not item.strip():
            tmp = item + "\n"

        # otherwise, just leave same level
        elif not config.preserve_leading_space:
            # if we are not trying to preserve indenting
            # on text, the add it now.
            tmp = (indent * indent_level) + item + "\n"
        else:
            tmp = item + "\n"

        # if a opening raw tag then start ignoring.. only if there is no closing tag
        # on the same line
        if is_ignored_block_opening_:
            is_block_raw = True
            is_raw_first_line = False

        # if a normal tag, we can try to expand attributes
        elif not is_block_raw:
            # get leading space, and attributes

            func = partial(format_attributes, config, item)

            tmp = indent_html_tags_pattern.sub(func, tmp)

        # turn off raw block if we hit end - for one line raw blocks, but not an inline raw
        if (
            not in_script_style_tag
            or is_script_style_block_closing(config, item)
        ) and is_ignored_block_closing(config, item):
            in_script_style_tag = False
            if not is_safe_closing_tag_:
                ignored_level -= 1
                ignored_level = max(ignored_level, 0)
            if ignored_level == 0:
                is_block_raw = False

        beautified_code += tmp

    # try to fix internal formatting of set tag
    def format_data(
        config: Config,
        contents: str,
        tag_size: int,
        leading_space: str,
        *,
        quote_style: QuoteStyle = QuoteStyle.ALWAYS_DOUBLE,
        normalize_string_quotes: bool = False,
    ) -> str:
        try:
            # try to format the contents as json
            data = json.loads(contents)
            contents = json.dumps(
                data,
                trailing_commas=False,
                ensure_ascii=False,
                quote_keys=True,
                quote_style=quote_style,
            )

            if tag_size + len(contents) >= config.max_line_length:
                # if the line is too long we can indent the json
                contents = json.dumps(
                    data,
                    indent=config.indent_size,
                    trailing_commas=False,
                    ensure_ascii=False,
                    quote_keys=True,
                    quote_style=quote_style,
                )

        except Exception:
            # was not json.. try to format as a Python literal.
            try:
                evaluated = str(ast.literal_eval(contents))
                # need to unwrap the eval
                contents = (
                    evaluated[1:-1]
                    if contents[:1] != "(" and evaluated[:1] == "("
                    else evaluated
                )
            except Exception:
                contents = contents.strip()

            if normalize_string_quotes:
                contents = _format_string_tokens(contents, quote_style)

        return (f"\n{leading_space}").join(contents.splitlines())

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
                )
            )

        return f"{leading_space}{open_bracket} {tag} {contents} {close_bracket}"

    def format_function(config: Config, html: str, match: re.Match[str]) -> str:
        if inside_ignored_block(config, html, match):
            return match.group()

        leading_space = match.group(1)
        open_bracket = match.group(2)
        tag = match.group(3).strip()
        index = (match.group(5) or "").strip()
        close_bracket = match.group(6)
        quote_style = QuoteStyle.ALWAYS_DOUBLE
        normalize_string_quotes = False

        if config.profile == "jinja":
            outer_quote = _attribute_quote_at(html, match.start(2))
            if outer_quote == '"':
                quote_style = QuoteStyle.ALWAYS_SINGLE
                normalize_string_quotes = True
            elif outer_quote == "'":
                normalize_string_quotes = True

        contents = format_data(
            config,
            match.group(4).strip()[1:-1],
            len(f"{open_bracket} {tag}() {close_bracket}"),
            leading_space,
            quote_style=quote_style,
            normalize_string_quotes=normalize_string_quotes,
        )

        return f"{leading_space}{open_bracket} {tag}({contents}){index} {close_bracket}"

    if not config.no_set_formatting:
        func = partial(format_set, config, beautified_code)
        # format set contents
        beautified_code = re.sub(
            r"([ ]*)({%-?)[ ]*(set)[ ]+?((?:(?!%}).)*?)(-?%})",
            func,
            beautified_code,
            flags=RE_FLAGS_IMSX,
        )

    if not config.no_function_formatting:
        func = partial(format_function, config, beautified_code)
        # format function contents
        beautified_code = re.sub(
            r"([ ]*)({{-?\+?)[ ]*?((?:(?!}}).)*?\w)(\((?:\"[^\"]*\"|'[^']*'|[^\)])*?\)[ ]*)((?:\[[^\]]*?\]|\.[^\s]+)[ ]*)?((?:(?!}}).)*?-?\+?}})",
            func,
            beautified_code,
            flags=RE_FLAGS_IMSX,
        )

    if not config.preserve_blank_lines:
        beautified_code = beautified_code.lstrip()

    return beautified_code.rstrip() + "\n"
