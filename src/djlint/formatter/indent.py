"""djLint add indentation to html."""

from __future__ import annotations

import ast
import io
import sys
import tokenize
from bisect import bisect_right
from functools import cache, lru_cache, partial
from typing import TYPE_CHECKING, cast, final

import json5 as json
import regex as re
from json5.lib import QuoteStyle

from djlint.const import (
    COLLAPSIBLE_WHITESPACE,
    HTML_RAW_TEXT_ELEMENTS,
    HTML_TAG_NAMES,
    HTML_VOID_ELEMENTS,
    TEMPLATE_TAG_NAME,
    TEMPLATE_TAGS_WITH_QUOTED_ARGUMENTS,
    TEMPLATE_TAGS_WITH_QUOTED_CONDITIONS,
)
from djlint.formatter.attributes import format_attributes
from djlint.formatter.class_attributes import (
    VERBATIM_ATTRIBUTE_NEWLINE,
    multiline_template_tag_spans,
    restore_template_string_newlines,
)
from djlint.formatter.tokenizer import tokenize_tags
from djlint.helpers import (
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_IS,
    RE_FLAGS_IX,
    compile_pattern,
    ignored_block_opening_start,
    inside_html_attribute,
    inside_ignored_block,
    inside_ignored_linter_block,
    is_ignored_block_closing,
    is_raw_text_block_closing,
    is_raw_text_block_opening,
    is_safe_closing_tag,
)

if sys.version_info >= (3, 13):
    from typing import NamedTuple
else:
    from typing_extensions import NamedTuple

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_QUOTE_STYLES: Final = {"double": QuoteStyle.PREFER_DOUBLE, "single": QuoteStyle.PREFER_SINGLE}
_QUOTE_CHARACTERS: Final = {"double": '"', "single": "'"}
_ESCAPE: Final = "\\"
# The raw text elements whose bodies --format-js and --format-css lay out.
_RAW_TEXT_OPENINGS_SPREAD: Final = frozenset(("script", "style"))

# A tag left open ends at the next opener, as for the multiline patterns below,
# so a run of unclosed ones is read once rather than each to the end of the
# file; a pattern starting with indentation reads each run of it from its
# start only.
_QUOTED_ARGUMENT_TAG_PATTERN: Final = compile_pattern(
    rf"\{{%[-+]?[ \t]*(?:{TEMPLATE_TAGS_WITH_QUOTED_ARGUMENTS}"
    rf"|{TEMPLATE_TAGS_WITH_QUOTED_CONDITIONS})\b"
    r"(?:(?![-+]?%\}|\{%).)*+[-+]?%\}",
    RE_FLAGS_IS,
)
_TAG_STRING_PATTERN: Final = compile_pattern(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'")

_TAG_SPACING_PATTERN: Final = compile_pattern(r"({%[-+]?)[ ]*?(\w(?:(?!%}).)*?)[ ]*?([-+]?%})")
_INTERPOLATION_SPACING_PATTERN: Final = compile_pattern(r"({{)[ ]*?(\w(?:(?!}}).)*?)[ ]*?(\+?-?}})")
# Indentation after a preserved attribute line break is the author's layout,
# not padding inside the tag, so it is held whole rather than collapsed.
_EXTRA_TAG_WHITESPACE_PATTERN: Final = compile_pattern(
    r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'"
    rf"|{re.escape(VERBATIM_ATTRIBUTE_NEWLINE)}[ \t]*)|[ \t]{{2,}}"
)
_HANDLEBARS_BLOCK_END_PATTERN: Final = compile_pattern(r"({{#(?:each|if)(?:(?!}}).)+?[^ ])(}})")
_SET_CLOSE_PATTERN: Final = compile_pattern(r"^(?!.*\{\%).*%\}.*$", RE_FLAGS_IMX)
_SET_CLOSING_BRACE_PATTERN: Final = compile_pattern(r"^[ ]*}|^[ ]*]", RE_FLAGS_IMX)
_TAG_CLOSE_START_PATTERN: Final = compile_pattern(r"[ \t]*[-+]?%}")
_SINGLE_LINE_TEMPLATE_TAG_PATTERN: Final = compile_pattern(
    r"^\s*\{%[-+]?(?:(?!%}).)*%}\s*$", RE_FLAGS_IMSX
)
_SET_OPEN_PATTERN: Final = compile_pattern(r"^([ ]*{%[ ]*?set)(?!.*%}).*$", RE_FLAGS_IMX)
_SET_OPENING_BRACE_PATTERN: Final = compile_pattern(
    r"(\{(?![^{}]*%[}\s])(?=[^{}]*$)|\[(?=[^\]]*$))", RE_FLAGS_IMX
)
_TEMPLATE_TAG_CLOSE_PATTERN: Final = compile_pattern(r"\{%[-+]?\s*end|\{\{/", RE_FLAGS_IMX)
# Some opener is left unclosed exactly when the last one is, so each is only
# read up to the next, which keeps a line of unclosed ones to one pass.
_MULTILINE_TAG_OPEN_PATTERN: Final = compile_pattern(r"(?:\{\{|\{%)(?:(?!\}\}|%\}|\{\{|\{%).)*$")
_MULTILINE_TAG_CLOSE_PATTERN: Final = compile_pattern(r"^(?:(?!\{\{|\{%).)*?(?:\}\}|%\})")
_LEADING_CLOSE_BRACKET_PATTERN: Final = compile_pattern(r"[ ]*[)\]}]")
_MULTILINE_TAG_OPEN_PAREN_PATTERN: Final = compile_pattern(r"\((?=[^()]*$)")
_MULTILINE_TAG_CLOSE_PAREN_PATTERN: Final = compile_pattern(r"^[ ]*\)")
_TEXTAREA_CLOSE_PATTERN: Final = compile_pattern(r"^\s*</textarea\b", RE_FLAGS_IX)
_LINE_TEMPLATE_TAG_PATTERN: Final = compile_pattern(
    r"\{\{(?:(?!\}\}|\{\{).)*\}\}|\{%(?:(?!%\}|\{%).)*%\}|\$\{[^{}]*\}"
)
_TRIMMED_TRANS_OPEN_PATTERN: Final = compile_pattern(
    r"\{%[-+]?\s*blocktrans(?:late)?\b(?:(?!%\}).)*?\btrimmed\b(?:(?!%\}).)*?%\}", RE_FLAGS_IS
)
_TRANS_CLOSE_PATTERN: Final = compile_pattern(
    r"\{%[-+]?\s*endblocktrans(?:late)?\b(?:(?!%\}).)*?%\}", RE_FLAGS_IS
)
_SET_CONTENT_PATTERN: Final = compile_pattern(
    r"""
    (?<![ ])([ ]*+)       # 1: leading indentation, read from its start
    ({%[-+]?)                # 2: tag open
    [ ]*(set)[ ]+?        # 3: the set keyword
    ((?:(?![-+]?%}|{%).)*+)  # 4: assignment contents
    ([-+]?%})                # 5: tag close
    """,
    RE_FLAGS_IMSX,
)
_FUNCTION_CONTENT_PATTERN: Final = compile_pattern(
    r"""
    (?<![ ])(?P<indent>[ ]*+)
    (?P<open>{{-?\+?)
    [ ]*?
    (?P<name>(?:(?!}}|{{).)*?\w)
    (?P<paren>
      \(
      (?:\"(?:(?!{{)[^\"])*+\"|'(?:(?!{{)[^'])*+'|(?:(?!{{)[^()])++|(?&paren))*+
      \)
    )
    (?P<index>(?:\[[^\]]*?\]|\.[^\s]+))?
    (?P<gap>[ ]*)
    (?P<close>(?:(?!}}|{{).)*?-?\+?}})
    """,
    RE_FLAGS_IMSX,
)


def _blank_quotes(match: re.Match[str]) -> str:
    return match.group().replace('"', "_").replace("'", "_")


def _without_template_quotes(line: str) -> str:
    """The line with the quotes inside its template tags blanked out.

    The pattern for a tag on one line reads an attribute value as quote to
    quote, so the value of `value="{{ _("it's") }}"` ended at the quote
    inside the tag, and the apostrophe opened another that never closed.
    """
    if ("{{" not in line and "{%" not in line and "${" not in line) or (
        '"' not in line and "'" not in line
    ):
        return line
    return _LINE_TEMPLATE_TAG_PATTERN.sub(_blank_quotes, line)


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


def _set_line_brackets(line: str, quote: str) -> tuple[int, int, str]:
    """Read the brackets of one line of a set tag's value.

    Returns how many closing brackets the line starts with, how much it changes
    the bracket depth, and the quote still open at its end. A bracket inside a
    quoted string counts for nothing, also when the string began on an earlier
    line, whose open quote is passed in.
    """
    leading = depth = 0
    at_start = not quote
    escaped = False
    for char in line:
        if quote:
            if escaped:
                escaped = False
            elif char == _ESCAPE:
                escaped = True
            elif char == quote:
                quote = ""
        elif char in "\"'":
            quote = char
            at_start = False
        elif char in "([{":
            depth += 1
            at_start = False
        elif char in ")]}":
            depth -= 1
            if at_start:
                leading += 1
        elif not char.isspace():
            at_start = False
    return leading, depth, quote


def _format_string_token(token_value: str, quote_style: QuoteStyle) -> str:
    try:
        value = ast.literal_eval(token_value)
    except (SyntaxError, ValueError):
        return token_value

    if not isinstance(value, str):
        return token_value

    return cast("str", json.dumps(value, ensure_ascii=False, quote_style=quote_style))


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


@final
class _IndentPatterns(NamedTuple):
    """The patterns indenting builds out of the configuration."""

    ignored_inline_start: re.Pattern[str]
    single_line_tag: re.Pattern[str]
    tag_unindent: re.Pattern[str]
    inline_slt_no_attrs_end: re.Pattern[str]
    inline_slt_no_attrs: re.Pattern[str]
    inline_slt_attrs: re.Pattern[str]
    tag_unindent_line: re.Pattern[str]
    tag_indent: re.Pattern[str]
    custom_html: re.Pattern[str] | None
    template_start: re.Pattern[str]
    prefixed_template_tag_indent: re.Pattern[str]


@lru_cache(maxsize=4)
def _indent_patterns(config: Config) -> _IndentPatterns:
    """Build the indenting patterns a configuration calls for.

    Every one of them is settled by the configuration alone, so building
    and looking them up once per file only asked the regex cache the same
    long questions over again.
    """
    slt_html = config.indent_html_tags
    always_self_closing_html = config.always_self_closing_html_tags
    slt_template = config.single_line_template_tags
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
                        |(?:<(?:{TEMPLATE_TAG_NAME})(?:>|(?:[^>"']|"[^"]*"|'[^']*')*?>)(?:.*?)</(?:{TEMPLATE_TAG_NAME})>) # <{{ tag }}>stuff</{{ tag }}>
                        |(?:{{%[-+]?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%[-+]?[ ]*?end(?:\2)\b(?:(?!%}}).)*?%}}) # >>> match 2
                        |{golang_slt}
                        |{config.ignored_inline_blocks}
                    )[ \t]*?
                    (?:
                    .* # anything, holding any number of tags
                    (?: # followed by another slt, the last of the line
                        <({slt_html})(?:(?:>|\b[^>]+?>)(?:.*?)(?:</(?:\3)>)|\b(?:[^>"']|"[^"]*"|'[^']*')*?\/>) # <span stuff-or-not>stuff</span> or <img stuff /> >>> match 3
                       |(?:<(?:{always_self_closing_html})\b(?:[^>"']|"[^"]*"|'[^']*')*?/?>) # <img stuff />
                       |(?:{{%[-+]?[ ]*?({slt_template})\b(?:(?!%}}).)*?%}})(?:.*?)(?:{{%[-+]?[ ]*?end(?:\4)\b(?:(?!%}}).)*?%}}) # >>> match 4
                       |{golang_slt}
                       |{config.ignored_inline_blocks}
                    )[ \t]*?
                    )? # optional of course. Repeated, it would match no more lines,
                    # but try every way to split one that fails.
                    [^<]*?$ # with no other tags following until end of line
                """,
        flags=RE_FLAGS_IMX,
    )
    tag_unindent_pattern = re.compile(config.tag_unindent, RE_FLAGS_IMX)
    inline_slt_no_attrs_end_pattern = re.compile(
        rf"(<({slt_html})>)(.*?)(</(\2)>[^<]*?$)", flags=RE_FLAGS_IMX
    )
    inline_slt_no_attrs_pattern = re.compile(
        rf"(^<({slt_html})>)(.*?)(</(\2)>)", flags=RE_FLAGS_IMX
    )
    inline_slt_attrs_pattern = re.compile(
        rf"(^<({slt_html})\b[^>]+?>)(.*?)(</(\2)>)", flags=RE_FLAGS_IMX
    )
    tag_unindent_line_pattern = re.compile(r"^" + str(config.tag_unindent_line), flags=RE_FLAGS_IMX)
    tag_indent_pattern = re.compile(r"^(?:" + str(config.tag_indent) + r")", flags=RE_FLAGS_IMX)
    custom_html_pattern = (
        re.compile(rf"^(?:{config.custom_html})$", flags=RE_FLAGS_IX)
        if config.custom_html
        else None
    )
    template_start_pattern = re.compile(
        r"(?:\{\{\#|\{%[-+]?)[ ]*?" + str(config.start_template_tags), flags=RE_FLAGS_IMX
    )
    prefixed_template_tag_indent_pattern = re.compile(
        r"^[^\S\n]*[\(\[](?:(?:\{\{\#|\{%[-+]?)[ ]*?" + str(config.start_template_tags) + r")",
        flags=RE_FLAGS_IMX,
    )

    return _IndentPatterns(
        ignored_inline_start=ignored_inline_start_pattern,
        single_line_tag=single_line_tag_pattern,
        tag_unindent=tag_unindent_pattern,
        inline_slt_no_attrs_end=inline_slt_no_attrs_end_pattern,
        inline_slt_no_attrs=inline_slt_no_attrs_pattern,
        inline_slt_attrs=inline_slt_attrs_pattern,
        tag_unindent_line=tag_unindent_line_pattern,
        tag_indent=tag_indent_pattern,
        custom_html=custom_html_pattern,
        template_start=template_start_pattern,
        prefixed_template_tag_indent=prefixed_template_tag_indent_pattern,
    )


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

    A line starting with a template block it leaves open indents what
    follows, even when the rest of it looks like a single-line tag, as in
    `{% call modal("<b>" ~ n ~ "</b>") %}` or `{% if a %}<b>x</b>`.

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
            # The indentation of a line the tag closes on, after a preserved
            # line break, is held whole like that of any other such line.
            closing_gap = " "
            if content.endswith(VERBATIM_ATTRIBUTE_NEWLINE):
                closing_gap = html[match.end(2) : match.start(3)]
            return f"{match.group(1)} {content}{closing_gap}{match.group(3)}"

        rawcode = _TAG_SPACING_PATTERN.sub(partial(fix_tag_spacing, rawcode), rawcode)

        rawcode = _INTERPOLATION_SPACING_PATTERN.sub(partial(fix_tag_spacing, rawcode), rawcode)

        def fix_tag_quotes(html: str, match: re.Match[str]) -> str:
            """Rewrite a tag's quoted arguments to the configured quote.

            This is what T002 asks for, so the rule stays fixable by
            running the formatter, and a condition is covered too, so one
            file does not spell the same string both ways. A string is
            left alone when it holds the quote it would be rewritten to,
            and so is a tag written inside an html attribute, where the
            attribute's own quotes decide. A quote escaped inside the
            string loses its backslash, the delimiter it hid from having
            gone.

            The contents of `{% verbatim %}` and `{% raw %}` are shown as
            they are written, so a tag quoted inside one is text on the
            page rather than a tag to normalize.
            """
            if (
                inside_ignored_block(config, html, match)
                or inside_ignored_linter_block(config, html, match)
                or inside_html_attribute(html, match)
            ):
                return match.group()

            wanted = _QUOTE_CHARACTERS[config.quote_style]

            def requote(string: re.Match[str]) -> str:
                text = string.group()
                quote, body = text[0], text[1:-1]
                if quote == wanted or wanted in body:
                    return text
                unescaped = body.replace(_ESCAPE + quote, quote)
                return f"{wanted}{unescaped}{wanted}"

            return _TAG_STRING_PATTERN.sub(requote, match.group())

        rawcode = _QUOTED_ARGUMENT_TAG_PATTERN.sub(partial(fix_tag_quotes, rawcode), rawcode)

    elif config.profile == "handlebars":

        def fix_handlebars_template_tags(html: str, match: re.Match[str]) -> str:
            if inside_ignored_block(config, html, match):
                return match.group()

            return f"{match.group(1)} {match.group(2)}"

        rawcode = _HANDLEBARS_BLOCK_END_PATTERN.sub(
            partial(fix_handlebars_template_tags, rawcode), rawcode
        )

    rawcode_flat_list = rawcode.split("\n")

    # A line inside a template tag written across lines holds template code,
    # where `"<a href='x'>"` is a string: spreading its attributes put line
    # breaks into the string, a syntax error in mako. The markup may still
    # render, as with `{{ "<b>"|safe }}` or mako's `HTML()`, so its tags are
    # still counted for indentation. Each such line maps to where markup may
    # start on it, -1 for none, as on a line the tag covers.
    markup_starts: dict[int, int] = {}
    tag_spans = multiline_template_tag_spans(rawcode)
    if tag_spans:
        line_starts = [0]
        for line in rawcode_flat_list[:-1]:
            line_starts.append(line_starts[-1] + len(line) + 1)
        for span_start, span_end in tag_spans:
            first = bisect_right(line_starts, span_start) - 1
            last = bisect_right(line_starts, span_end - 1) - 1
            for line_index in range(first + 1, last):
                markup_starts[line_index] = -1
            markup_starts[last] = span_end - line_starts[last]

    indent = config.indent

    beautified_lines: list[str] = []
    indent_level = 0
    in_set_tag = False
    # The level of the line that opened the set tag, which its closing line returns to
    # however many brackets the lines between left open.
    set_tag_level = 0
    # The quote of a string in the set tag's value that a line left open.
    set_quote = ""
    in_multiline_tag = False
    multiline_tag_level = 0
    multiline_tag_is_block = False
    is_raw_first_line = False
    in_raw_text_tag = False
    is_block_raw = False

    ignored_level = 0
    # Trimmed blocktrans blocks opened inside the current ignored block.
    open_trimmed_trans = 0

    template_block_stack: list[tuple[int, int | None, bool]] = []
    # How many template blocks are open. The tags inside an ignored block
    # are not counted, but the ones that open and close it are, as a pair.
    # At zero an end tag closes nothing.
    open_template_blocks = 0

    open_html_indents: list[bool] = []

    patterns = _indent_patterns(config)
    ignored_inline_start_pattern = patterns.ignored_inline_start
    single_line_tag_pattern = patterns.single_line_tag
    tag_unindent_pattern = patterns.tag_unindent
    inline_slt_no_attrs_end_pattern = patterns.inline_slt_no_attrs_end
    inline_slt_no_attrs_pattern = patterns.inline_slt_no_attrs
    inline_slt_attrs_pattern = patterns.inline_slt_attrs
    tag_unindent_line_pattern = patterns.tag_unindent_line
    tag_indent_pattern = patterns.tag_indent
    custom_html_pattern = patterns.custom_html
    template_start_pattern = patterns.template_start
    prefixed_template_tag_indent_pattern = patterns.prefixed_template_tag_indent
    template_indent_pattern = config.template_indent_imx_pattern
    template_unindent_pattern = config.template_unindent_imx_pattern

    def is_html_tag(name: str) -> bool:
        return name.lower() in HTML_TAG_NAMES or bool(
            custom_html_pattern and custom_html_pattern.match(name)
        )

    def format_html_attributes(value: str) -> str:
        output: list[str] = []
        previous_end = 0
        for token in tokenize_tags(value):
            if token.closing or token.declaration or not is_html_tag(token.name):
                continue
            leading_start = token.start
            while leading_start and value[leading_start - 1] in " \t":
                leading_start -= 1
            written = "".join(output) + value[previous_end : token.start]
            replacement = format_attributes(
                config, value, token, written[written.rfind("\n") + 1 :]
            )
            replacement_start = (
                token.start if replacement == value[token.start : token.end] else leading_start
            )
            output.extend((value[previous_end:replacement_start], replacement))
            previous_end = token.end
        output.append(value[previous_end:])
        return "".join(output)

    def format_raw_text_opening(line: str, start: int) -> str:
        """Spread the attributes of a raw text element opening at start.

        Its body is left as written, but its opening tag is markup like any
        other. Left alone, a long one stayed on one line while its body was
        written on lines of its own, and was spread once the body was
        joined to it, so formatting the script a second time changed it.
        """
        for token in tokenize_tags(line):
            if token.start >= start:
                break
        else:
            return line
        if (
            token.start != start
            or token.closing
            or token.name.lower() not in _RAW_TEXT_OPENINGS_SPREAD
        ):
            return line
        return format_html_attributes(line[: token.end]) + line[token.end :]

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
            elif not token.self_closing and token.name.lower() not in HTML_VOID_ELEMENTS:
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
            elif not token.closing and not token.self_closing and name in HTML_RAW_TEXT_ELEMENTS:
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

    for line_index, item in enumerate(rawcode_flat_list):
        markup_start = markup_starts.get(line_index, 0)
        no_template_block_open = open_template_blocks == 0
        is_safe_closing_tag_ = is_safe_closing_tag(config, item)
        ignored_block_opening_start_ = ignored_block_opening_start(config, item)
        is_ignored_block_opening_ = ignored_block_opening_start_ >= 0
        was_block_raw = is_block_raw
        dedent_after = 0
        indent_level_before = indent_level
        opened_html = 0
        unclosed_closes = 0
        html_dedent = 0
        indented_closes = 0
        closes_nothing_indented = False
        closed_a_template_block = False

        if not is_block_raw and is_ignored_block_opening_:
            is_raw_first_line = True

        if is_ignored_block_opening_:
            is_block_raw = True
            ignored_level += 1

        if is_raw_text_block_opening(config, item):
            in_raw_text_tag = True

        marker_is_shown_as_text = (
            is_safe_closing_tag_ and in_raw_text_tag and not is_raw_text_block_closing(config, item)
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

        set_leading_closes = set_depth_change = 0
        starts_in_set_string = False
        if in_set_tag:
            starts_in_set_string = bool(set_quote)
            set_leading_closes, set_depth_change, set_quote = _set_line_brackets(item, set_quote)

        if (not is_block_raw and ignored_inline_start_pattern.search(item)) or (
            not is_block_raw
            and single_line_tag_pattern.search(_without_template_quotes(item.lstrip()))
            and not starts_unclosed_html_tag(item)
            and not template_unindent_pattern.match(item.lstrip())
            and not tag_unindent_line_pattern.match(item.lstrip())
            and not (
                template_indent_pattern.match(item.lstrip())
                and not template_unindent_pattern.search(item)
            )
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and _SET_CLOSE_PATTERN.search(item)
        ):
            in_set_tag = False
            # A line that starts with a closing bracket lines up with what that bracket
            # closes, the bare tag close with the tag; anything else is one more line of
            # the value. A line that goes on with a string gets no indentation, which
            # would become part of the string.
            if starts_in_set_string:
                line_level = 0
            elif set_leading_closes:
                line_level = max(indent_level - 1, set_tag_level)
            elif _TAG_CLOSE_START_PATTERN.match(item):
                line_level = set_tag_level
            else:
                line_level = indent_level
            tmp = (indent * line_level) + formatted_item(item) + "\n"
            indent_level = set_tag_level
            set_quote = ""

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and in_set_tag
            and (set_leading_closes or set_depth_change or starts_in_set_string)
        ):
            # A line that starts with a closing bracket lines up with what that bracket
            # closes; the next line follows every bracket this one opens or closes, and
            # stays a level inside the tag, as the rest of the value.
            line_level = max(indent_level - (1 if set_leading_closes else 0), set_tag_level)
            if starts_in_set_string:
                line_level = 0
            tmp = (indent * line_level) + formatted_item(item) + "\n"
            indent_level = max(indent_level + set_depth_change, set_tag_level + 1)

        elif not is_block_raw and in_multiline_tag and _MULTILINE_TAG_CLOSE_PATTERN.search(item):
            tmp_level = (
                multiline_tag_level
                if _LEADING_CLOSE_BRACKET_PATTERN.match(item)
                else multiline_tag_level + 1
            )
            tmp = (indent * tmp_level) + formatted_item(item) + "\n"
            indent_level = multiline_tag_level + (1 if multiline_tag_is_block else 0)
            if multiline_tag_is_block:
                template_block_stack.append((multiline_tag_level, None, True))
            closes_an_html_tag_too = bool(tag_unindent_pattern.search(item.lstrip()))
            if closes_an_html_tag_too:
                indent_level = max(indent_level - 1, 0)
            opens_another_multiline_tag = bool(_MULTILINE_TAG_OPEN_PATTERN.search(item))
            if opens_another_multiline_tag:
                multiline_tag_level = indent_level
                multiline_tag_is_block = len(template_start_pattern.findall(item)) > len(
                    template_unindent_pattern.findall(item)
                )
                indent_level += 1
            else:
                in_multiline_tag = False

        elif (
            not is_block_raw
            and in_multiline_tag
            and (
                _SET_CLOSING_BRACE_PATTERN.search(item)
                or _MULTILINE_TAG_CLOSE_PAREN_PATTERN.search(item)
            )
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif (
            not is_block_raw
            and in_multiline_tag
            and (
                _SET_OPENING_BRACE_PATTERN.search(item)
                or _MULTILINE_TAG_OPEN_PAREN_PATTERN.search(item)
            )
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            indent_level += 1

        elif (
            not is_block_raw
            and not is_safe_closing_tag_
            and tag_unindent_pattern.search(item.lstrip())
            and (unclosed_closes > opened_html or not inline_slt_no_attrs_end_pattern.search(item))
            and not starts_unclosed_html_tag(item)
            and not tag_unindent_line_pattern.match(item.lstrip())
        ):
            if inline_slt_no_attrs_pattern.search(item) or inline_slt_attrs_pattern.search(item):
                tmp = (indent * indent_level) + formatted_item(item) + "\n"
                indent_level = max(indent_level - 1, 0)
            elif template_block_stack and template_unindent_pattern.match(item.lstrip()):
                saved_level, branch_delta, consistent = template_block_stack.pop()
                closed_a_template_block = True
                delta = indent_level - saved_level - 1
                target = (
                    saved_level + delta if consistent and branch_delta == delta else saved_level
                )
                indent_level = min(max(indent_level - 1, 0), max(target, 0))
                tmp = (indent * min(indent_level, saved_level)) + formatted_item(item) + "\n"
                if config.profile == "golang":
                    glued_openers = len(template_start_pattern.findall(item)) - (
                        len(template_unindent_pattern.findall(item)) - 1
                    )
                    for _ in range(max(glued_openers, 0)):
                        template_block_stack.append((indent_level, None, True))
                        indent_level += 1
            elif closes_nothing_indented or (
                no_template_block_open
                and not unclosed_closes
                and template_unindent_pattern.match(item.lstrip())
            ):
                # An end tag with no block open to close, as an unknown
                # `{% endtoc %}` or a stray `{% endif %}`, closes nothing, so
                # it stays at the level of what it is written in.
                tmp = (indent * indent_level) + formatted_item(item) + "\n"

            else:
                floor = template_block_stack[-1][0] + 1 if template_block_stack else 0
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
                template_block_stack[-1] = (saved_level, branch_delta, consistent)
                tmp = (indent * saved_level) + formatted_item(item) + "\n"
                indent_level = saved_level + 1
            else:
                tmp = (indent * (indent_level - 1)) + formatted_item(item) + "\n"

        elif (
            not config.no_set_formatting
            and not is_block_raw
            and not in_set_tag
            and (set_open := _SET_OPEN_PATTERN.search(item))
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            set_tag_level = indent_level
            # The value starts a level in, or one per bracket it leaves open, as in
            # `outer(inner(`.
            _, opened, set_quote = _set_line_brackets(item[set_open.end(1) :], "")
            indent_level += max(opened, 1)
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
            multiline_tag_is_block = len(template_start_pattern.findall(item)) > len(
                template_unindent_pattern.findall(item)
            )
            indent_level += 1

        elif not is_block_raw and (
            tag_indent_pattern.search(item.lstrip())
            or (
                prefixed_template_tag_indent_pattern.search(item.lstrip())
                and not _TEMPLATE_TAG_CLOSE_PATTERN.search(item)
            )
        ):
            tmp = (indent * indent_level) + formatted_item(item) + "\n"
            if template_indent_pattern.match(item.lstrip()) and len(
                template_indent_pattern.findall(item)
            ) > len(template_unindent_pattern.findall(item)):
                template_block_stack.append((indent_level, None, True))
            indent_level += 1

        elif is_raw_first_line or (is_safe_closing_tag_ and not is_block_raw):
            if is_raw_first_line and "<" in item:
                # A tag closed before the block opens, as in
                # `</noscript><script>`, closes what it closes as on any other
                # line. Left open, it indented the rest of the file a level
                # deeper once the script was written over several lines.
                _, closes = scan_html_tags(item[:ignored_block_opening_start_])
                popped = min(closes, len(open_html_indents))
                indented_closes = sum(open_html_indents.pop() for _ in range(popped))
                floor = template_block_stack[-1][0] + 1 if template_block_stack else 0
                indent_level = max(indent_level - indented_closes, min(floor, indent_level))
            tmp = (indent * indent_level) + formatted_item(item) + "\n"

        elif is_block_raw or not item.strip():
            if (
                config.profile in {"jinja", "askama", "tera", "liquid", "nunjucks"}
                and is_block_raw
                and _TEXTAREA_CLOSE_PATTERN.search(item)
                and output_ends_with(("-}}", "-%}"))
            ):
                tmp = (indent * indent_level) + item.lstrip() + "\n"
            else:
                tmp = item + "\n"

        elif config.preserve_leading_space and _SINGLE_LINE_TEMPLATE_TAG_PATTERN.search(item):
            tmp = (indent * indent_level) + item.lstrip() + "\n"

        elif not config.preserve_leading_space:
            tmp = (indent * indent_level) + item + "\n"
        else:
            tmp = item + "\n"

        if html_dedent:
            stripped_item = item.lstrip()
            already_given_back = indent_level < indent_level_before
            took_no_level_of_its_own = indent_level == indent_level_before or not (
                stripped_item.startswith("<") and not stripped_item.startswith("</")
            )
            if already_given_back and not closed_a_template_block:
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
            opening_tail = item[ignored_block_opening_start_:] + "\n"
            # As for any other tag, one inside a template tag written across
            # lines is part of its text, and spreading it would change that.
            in_template_text = markup_start < 0 or "<" in item[:markup_start]
            if is_raw_first_line and not in_template_text and tmp.endswith(opening_tail):
                tmp = format_raw_text_opening(tmp, len(tmp) - len(opening_tail))
            is_block_raw = True
            is_raw_first_line = False
            if "<" in item:
                opened, _ = scan_html_tags(item[:ignored_block_opening_start_])
                if opened:
                    indent_level += 1
                    open_html_indents.append(True)
                    open_html_indents.extend([False] * (opened - 1))

        elif not is_block_raw and (
            markup_start == 0 or (markup_start > 0 and "<" not in item[:markup_start])
        ):
            tmp = format_html_attributes(tmp)

        # A trimmed blocktrans is formatted rather than left alone, so it
        # opens no ignored block, but its endblocktrans looks like the close
        # of one: inside a `{% filter %}` it ended the filter early. Each one
        # opened in an ignored block claims the next endblocktrans there.
        closing_item = item
        if is_block_raw:
            trimmed_trans_opens = len(_TRIMMED_TRANS_OPEN_PATTERN.findall(item))
            trans_closes = len(_TRANS_CLOSE_PATTERN.findall(item))
            claimed = min(trans_closes, open_trimmed_trans + trimmed_trans_opens)
            open_trimmed_trans += trimmed_trans_opens - claimed
            if claimed:
                closing_item = _TRANS_CLOSE_PATTERN.sub("", item, count=claimed)

        if (
            not in_raw_text_tag or is_raw_text_block_closing(config, item)
        ) and is_ignored_block_closing(config, closing_item):
            in_raw_text_tag = False
            if not is_safe_closing_tag_:
                ignored_level = max(ignored_level - 1, 0)
            if ignored_level == 0:
                is_block_raw = False
                open_trimmed_trans = 0
                if was_block_raw and "<" in item:
                    tail = ""
                    for close in config.ignored_block_closing_pattern.finditer(item):
                        tail = item[close.end() :]
                    opened, closed = scan_html_tags(tail)
                    if closed:
                        kept = max(len(open_html_indents) - closed, 0)
                        indent_level = max(indent_level - sum(open_html_indents[kept:]), 0)
                        del open_html_indents[kept:]
                    open_html_indents.extend([False] * opened)

        if "{" in item and not (was_block_raw and is_block_raw):
            opened = 0 if was_block_raw else len(template_indent_pattern.findall(item))
            closed = len(template_unindent_pattern.findall(item))
            open_template_blocks = max(open_template_blocks + opened - closed, 0)

        beautified_lines.append(tmp)

    # The strings are whole again before sets and calls are laid out, which
    # read their values as data.
    beautified_code = restore_template_string_newlines("".join(beautified_lines))

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

        indent = leading_space = match["indent"]
        open_bracket = match["open"]
        name = match["name"]
        tag = name.strip()
        # A call written on a line of its own after the "{{" stays there, as
        # the closing "}}" does: its lines were indented for that layout, and
        # lifting the call onto the "{{" line left them a level too deep
        # until the next run. They are laid out from the call's own line.
        opening_gap = " "
        name_gap = name[: len(name) - len(name.lstrip())]
        if "\n" in name_gap:
            opening_gap = name_gap[name_gap.find("\n") :]
            leading_space = opening_gap[opening_gap.rfind("\n") + 1 :]
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

        separator = " " if close_bracket.lstrip("-+").startswith("}}") else match["gap"]
        closing_space = leading_space if contents.endswith("\n") else ""
        return (
            f"{indent}{open_bracket}{opening_gap}{tag}({contents}{closing_space})"
            f"{index}{separator}{close_bracket}"
        )

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
