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

from djlint.const import HTML_TAG_NAMES, HTML_VOID_ELEMENTS
from djlint.formatter.attributes import format_attributes
from djlint.formatter.tokenizer import tokenize_tags
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
    from typing import Final

    from djlint.settings import Config


_TAG_SPACING_PATTERN: Final = re.compile(
    r"({%-?\+?)[ ]*?(\w(?:(?!%}).)*?)[ ]*?(\+?-?%})", cache_pattern=False
)
_INTERPOLATION_SPACING_PATTERN: Final = re.compile(
    r"({{)[ ]*?(\w(?:(?!}}).)*?)[ ]*?(\+?-?}})", cache_pattern=False
)
_HANDLEBARS_BLOCK_END_PATTERN: Final = re.compile(
    r"({{#(?:each|if).+?[^ ])(}})", cache_pattern=False
)
_SET_CLOSE_PATTERN: Final = re.compile(
    r"^(?!.*\{\%).*%\}.*$", RE_FLAGS_IMX, cache_pattern=False
)
_SET_CLOSING_BRACE_PATTERN: Final = re.compile(
    r"^[ ]*}|^[ ]*]", RE_FLAGS_IMX, cache_pattern=False
)
_SINGLE_LINE_TEMPLATE_TAG_PATTERN: Final = re.compile(
    r"^\s*\{%-?(?:(?!%}).)*%}\s*$", RE_FLAGS_IMSX, cache_pattern=False
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
    r"\{%-?\s*end|\{\{/", RE_FLAGS_IMX, cache_pattern=False
)
# a line ending inside a template tag or expression that opened on it.
_MULTILINE_TAG_OPEN_PATTERN: Final = re.compile(
    r"(?:\{\{|\{%)(?:(?!\}\}|%\}).)*$", cache_pattern=False
)
# a line closing a template tag or expression opened on an earlier line.
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
    r"([ ]*)({%-?)[ ]*(set)[ ]+?((?:(?!%}).)*?)(-?%})",
    RE_FLAGS_IMSX,
    cache_pattern=False,
)
# possessive quantifiers keep an unbalanced "(" from backtracking
# exponentially across the rest of the file.
_FUNCTION_CONTENT_PATTERN: Final = re.compile(
    r"([ ]*)({{-?\+?)[ ]*?((?:(?!}}).)*?\w)((?P<paren>\((?:\"[^\"]*+\"|'[^']*+'|[^()]++|(?&paren))*+\))[ ]*)((?:\[[^\]]*?\]|\.[^\s]+)[ ]*)?((?:(?!}}).)*?-?\+?}})",
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

        rawcode = _TAG_SPACING_PATTERN.sub(func, rawcode)

        rawcode = _INTERPOLATION_SPACING_PATTERN.sub(func, rawcode)

    elif config.profile == "handlebars":

        def fix_handlebars_template_tags(
            html: str, match: re.Match[str]
        ) -> str:
            if inside_ignored_block(config, html, match):
                return match.group()

            return f"{match.group(1)} {match.group(2)}"

        func = partial(fix_handlebars_template_tags, rawcode)
        # handlebars templates
        rawcode = _HANDLEBARS_BLOCK_END_PATTERN.sub(func, rawcode)

    rawcode_flat_list = rawcode.split("\n")

    indent = config.indent

    beautified_code = ""
    indent_level = 0
    in_set_tag = False
    in_multiline_tag = False
    multiline_tag_level = 0
    multiline_tag_is_block = False
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
                        |(?:<(?:{always_self_closing_html})\b(?:[^>"']|"[^"]*"|'[^']*')*?/?>) # <img stuff />
                        |(?:{{%-?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%-?[ ]*?end(?:\2)\b(?:(?!%}}).)*?%}}) # >>> match 2
                        |{config.ignored_inline_blocks}
                    )[ \t]*?
                    (?:
                    .*? # anything
                    (?: # followed by another slt
                        <({slt_html})(?:(?:>|\b[^>]+?>)(?:.*?)(?:</(?:\3)>)|\b(?:[^>"']|"[^"]*"|'[^']*')*?\/>) # <span stuff-or-not>stuff</span> or <img stuff /> >>> match 3
                       |(?:<(?:{always_self_closing_html})\b(?:[^>"']|"[^"]*"|'[^']*')*?/?>) # <img stuff />
                       |(?:{{%-?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%-?[ ]*?end(?:\4)\b(?:(?!%}}).)*?%}}) # >>> match 4
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
        r"(?:\{\{\#|\{%-?)[ ]*?" + str(config.start_template_tags),
        flags=RE_FLAGS_IMX,
    )
    template_unindent_pattern = re.compile(
        str(config.template_unindent), flags=RE_FLAGS_IMX
    )
    prefixed_template_tag_indent_pattern = re.compile(
        r"^[^\S\n]*[\(\[](?:\{\{\#|\{%-?)[ ]*?"
        + str(config.start_template_tags),
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

    for item in rawcode_flat_list:
        is_safe_closing_tag_ = is_safe_closing_tag(config, item)
        is_ignored_block_opening_ = is_ignored_block_opening(config, item)
        dedent_after = 0

        # if a raw tag first line
        if not is_block_raw and is_ignored_block_opening_:
            is_raw_first_line = True

        # if a raw tag then start ignoring
        if is_ignored_block_opening_:
            is_block_raw = True
            ignored_level += 1

        if is_script_style_block_opening(config, item):
            in_script_style_tag = True

        # Closing tags can trail rendered text; keep the line intact, then
        # close indentation for following siblings.
        if (
            not is_block_raw
            and ("{%" in item or "{{" in item)
            and not template_unindent_pattern.match(item.lstrip())
        ):
            close_count = len(template_unindent_pattern.findall(item))
            if close_count:
                open_count = len(template_start_pattern.findall(item))
                dedent_after = max(close_count - open_count, 0)

        if (
            not is_block_raw
            and "</" in item
            and not tag_unindent_pattern.search(item)
        ):
            html_depth_change = sum(
                -1 if token.closing else 1
                for token in tokenize_tags(item)
                if is_html_tag(token.name)
                and not token.self_closing
                and token.name.lower() not in HTML_VOID_ELEMENTS
            )
            dedent_after += max(-html_depth_change, 0)

        if is_safe_closing_tag_:
            ignored_level -= 1
            ignored_level = max(ignored_level, 0)
            if is_block_raw and ignored_level == 0:
                is_block_raw = False

        if (not is_block_raw and ignored_inline_start_pattern.search(item)) or (
            not is_block_raw
            and single_line_tag_pattern.search(item)
            and not starts_unclosed_html_tag(item)
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        # closing set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_CLOSE_PATTERN.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            in_set_tag = False
            tmp = (indent * indent_level) + item + "\n"

        # closing curly brace inside a set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_CLOSING_BRACE_PATTERN.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + item + "\n"

        # closing line of a template tag or expression spanning multiple lines
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
            tmp = (indent * tmp_level) + item + "\n"
            indent_level = multiline_tag_level + (
                1 if multiline_tag_is_block else 0
            )
            # the line may also close an html tag, e.g. ") }}</span>"
            if tag_unindent_pattern.search(item):
                indent_level = max(indent_level - 1, 0)
            # the same line may open another multi-line tag or expression
            if _MULTILINE_TAG_OPEN_PATTERN.search(item):
                multiline_tag_level = indent_level
                multiline_tag_is_block = len(
                    template_start_pattern.findall(item)
                ) > len(template_unindent_pattern.findall(item))
                indent_level += 1
            else:
                in_multiline_tag = False

        # closing bracket inside a multi-line template tag or expression
        elif (
            not is_block_raw
            and in_multiline_tag
            and _SET_CLOSING_BRACE_PATTERN.search(item)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + item + "\n"

        # opening bracket inside a multi-line template tag or expression
        elif (
            not is_block_raw
            and in_multiline_tag
            and _SET_OPENING_BRACE_PATTERN.search(item)
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level += 1

        # if unindent, move left
        elif (
            not is_block_raw
            and not is_safe_closing_tag_
            and tag_unindent_pattern.search(item)
            # and not ending in a slt like <span><strong></strong>.
            and not inline_slt_no_attrs_end_pattern.search(item)
            and not inline_slt_attrs_end_pattern.search(item)
            and not starts_unclosed_html_tag(item)
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
            and _SET_OPEN_PATTERN.search(item)
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level += 1
            in_set_tag = True

        # opening line of a template tag or expression that continues on the
        # next line; its contents are indented by bracket depth until the
        # closing line.
        elif (
            not is_block_raw
            and not config.preserve_leading_space
            and not in_set_tag
            and not in_multiline_tag
            and _MULTILINE_TAG_OPEN_PATTERN.search(item)
            # a line opening an html tag is indented as html instead.
            and not starts_unclosed_html_tag(item)
        ):
            tmp = (indent * indent_level) + item + "\n"
            in_multiline_tag = True
            multiline_tag_level = indent_level
            multiline_tag_is_block = len(
                template_start_pattern.findall(item)
            ) > len(template_unindent_pattern.findall(item))
            indent_level += 1

        # opening curly brace inside a set tag
        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_OPENING_BRACE_PATTERN.search(item)
        ) or (
            not is_block_raw
            and (
                tag_indent_pattern.search(item)
                or (
                    prefixed_template_tag_indent_pattern.search(item)
                    and not _TEMPLATE_TAG_CLOSE_PATTERN.search(item)
                )
            )
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level += 1

        elif is_raw_first_line or (is_safe_closing_tag_ and not is_block_raw):
            tmp = (indent * indent_level) + item + "\n"

        elif is_block_raw or not item.strip():
            if (
                config.profile in {"jinja", "nunjucks"}
                and is_block_raw
                and _TEXTAREA_CLOSE_PATTERN.search(item)
                and beautified_code.rstrip().endswith(("-}}", "-%}"))
            ):
                tmp = (indent * indent_level) + item.lstrip() + "\n"
            else:
                tmp = item + "\n"

        # otherwise, just leave same level
        elif (
            config.preserve_leading_space
            and _SINGLE_LINE_TEMPLATE_TAG_PATTERN.search(item)
        ):
            tmp = (indent * indent_level) + item.lstrip() + "\n"

        elif not config.preserve_leading_space:
            # if we are not trying to preserve indenting
            # on text, the add it now.
            tmp = (indent * indent_level) + item + "\n"
        else:
            tmp = item + "\n"

        if dedent_after:
            indent_level = max(indent_level - dedent_after, 0)

        # if a opening raw tag then start ignoring.. only if there is no closing tag
        # on the same line
        if is_ignored_block_opening_:
            is_block_raw = True
            is_raw_first_line = False

        # if a normal tag, we can try to expand attributes
        elif not is_block_raw:
            # get leading space, and attributes

            tmp = format_html_attributes(tmp)

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
        # json.dumps produces relative indentation that must be shifted by
        # leading_space; the fallback keeps the absolute indentation already
        # applied by the indent pass, so its lines are joined unshifted.
        joiner = "\n"
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
                joiner = f"\n{leading_space}"

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
                )
            )

        return f"{leading_space}{open_bracket} {tag} {contents} {close_bracket}"

    def format_function(config: Config, html: str, match: re.Match[str]) -> str:
        if inside_ignored_block(config, html, match):
            return match.group()

        leading_space = match.group(1)
        open_bracket = match.group(2)
        tag = match.group(3).strip()
        index = (match.group(6) or "").strip()
        close_bracket = match.group(7)
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

        separator = "" if close_bracket[:1].isspace() else " "
        return f"{leading_space}{open_bracket} {tag}({contents}){index}{separator}{close_bracket}"

    if not config.no_set_formatting:
        func = partial(format_set, config, beautified_code)
        # format set contents
        beautified_code = _SET_CONTENT_PATTERN.sub(func, beautified_code)

    if not config.no_function_formatting:
        func = partial(format_function, config, beautified_code)
        # format function contents
        beautified_code = _FUNCTION_CONTENT_PATTERN.sub(func, beautified_code)

    if not config.preserve_blank_lines:
        beautified_code = beautified_code.lstrip()

    return beautified_code.rstrip() + "\n"
