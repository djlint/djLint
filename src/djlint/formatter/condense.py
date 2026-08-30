"""Condense HTML.

1. Put short html tags back on one line
2. Put short template tags back on one line
"""

from __future__ import annotations

from collections import Counter
from functools import partial
from typing import TYPE_CHECKING

import regex as re

from djlint.const import COLLAPSIBLE_WHITESPACE, HTML_INLINE_ELEMENTS
from djlint.helpers import (
    RE_FLAGS_IMS,
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_IX,
    RE_FLAGS_MSX,
    YAML_FRONT_MATTER,
    inside_html_attribute,
    inside_ignored_block,
    inside_ignored_block_span,
    inside_protected_trans_block,
    is_ignored_block_opening,
    is_safe_closing_tag,
    split_option_list,
)

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_YAML_FRONT_MATTER_PATTERN: Final = re.compile(
    YAML_FRONT_MATTER, RE_FLAGS_MSX, cache_pattern=False
)

_COLLAPSIBLE_WHITESPACE_CHARS: Final = frozenset(COLLAPSIBLE_WHITESPACE)
_COLLAPSIBLE_WHITESPACE_PATTERN: Final = re.compile(
    f"[{re.escape(COLLAPSIBLE_WHITESPACE)}]+", cache_pattern=False
)

_CLOSING_LINE_PATTERN: Final = re.compile(
    r"[ \t]*(?:</|\{%[-+]?\s*end|\{\{/)", cache_pattern=False
)

_COMMENT_LINE_PATTERN: Final = re.compile(
    r"[ \t]*(?:\{#[^\n]*?#\}|<!--[^\n]*?-->)[ \t]*", cache_pattern=False
)


def _opening_line_pattern(config: Config) -> re.Pattern[str]:
    """Build the mirror of the pattern for a line that closes a block.

    A line that opens a block and increases the indentation: a template
    block tag, or an html tag that is neither void nor self closed, with
    nothing else on the line.
    """
    return re.compile(
        rf"""
        [ \t]*
        (?:
            (?:{config.template_indent})
            (?:(?!%\}}|\}}\}}).)*(?:%\}}|\}}\}})
          | <(?!(?:{config.always_self_closing_html_tags})\b)
            (?:{config.indent_html_tags})\b
            (?:"[^"]*"|'[^']*'|[^>"'])*(?<!/)>
        )
        [ \t]*
        """,
        RE_FLAGS_IX,
    )


def clean_whitespace(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""

    def strip_space(config: Config, html: str, match: re.Match[str]) -> str:
        """Trim the whitespace on a line that is layout rather than content.

        A line inside an ignored block keeps everything, unless it is a
        closing tag safe to indent. One that starts inside a verbatim block
        but runs past its end, as in "  x  </pre> tail", opens with the
        block's own content rather than with indentation, so that
        whitespace stays; a block whose closing tag is safe to indent
        (script, style) holds none to keep. One that opens a multi-line
        ignored block, as in "<textarea>x", has verbatim content after the
        opening tag, so only its leading indentation goes and the line can
        still be re-indented.
        """
        if inside_ignored_block(
            config, html, match
        ) and not is_safe_closing_tag(config, match.group()):
            return match.group()

        leading = ""
        if not is_safe_closing_tag(
            config, match.group()
        ) and inside_ignored_block_span(
            config, html, match.start(), match.start(1)
        ):
            leading = match.string[match.start() : match.start(1)]

        if is_ignored_block_opening(config, match.group()):
            return leading + match.group(1) + match.group(2)

        if inside_protected_trans_block(config, html[: match.end()], match):
            return match.group().rstrip()

        lines = match.group(2).count("\n")
        blank_lines = "\n" * lines
        if lines > config.max_blank_lines:
            blank_lines = "\n" * max(config.max_blank_lines, 0)
        return leading + match.group(1) + blank_lines

    func = partial(strip_space, config, html)

    line_contents = r"(.*?)"
    trailing_contents = r"\n \t"

    if config.preserve_blank_lines:
        line_contents = r"([^\n]*?)"
        trailing_contents = r" \t"

    if not config.preserve_leading_space:
        html = re.sub(
            rf"^[ \t]*{line_contents}([{trailing_contents}]*)$",
            func,
            html,
            flags=re.M,
        )

    else:
        leading_tag = r"(?:<|{%)"
        html = re.sub(
            rf"^[ \t]*({leading_tag}.*?)([{trailing_contents}]*)$",
            func,
            html,
            flags=re.M,
        )
        html = re.sub(
            rf"^{line_contents}([{trailing_contents}]*)$",
            func,
            html,
            flags=re.M,
        )

    def add_blank_line_after(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        """Add break after if not in ignored block."""
        match_end = match.end()
        if html[match_end : match_end + 1] == "\n":
            return match.group()

        if inside_ignored_block(config, html, match):
            return match.group()

        if inside_html_attribute(html, match):
            return match.group()

        next_line = match.string[match_end:].split("\n", 1)[0]
        if _CLOSING_LINE_PATTERN.match(next_line):
            return match.group()

        return match.group() + "\n"

    func = partial(add_blank_line_after, config, html)

    if config.blank_line_after_tag:
        for tag in split_option_list(config.blank_line_after_tag):
            html = re.sub(
                rf"((?:{{%[-+]?\s*?{tag}\b[^}}]+?[-+]?%}}\n?)+)",
                func,
                html,
                flags=RE_FLAGS_IMS,
            )

    def add_blank_line_before(
        config: Config,
        html: str,
        opening_line: re.Pattern[str],
        attach_comments: bool,  # noqa: FBT001
        match: re.Match[str],
    ) -> str:
        """Add a break before the tag, unless the line above rules it out.

        The first line of the file gets none, nor does a line inside an
        ignored block. A comment line directly above belongs to this tag,
        and if it was not swallowed into the match there is already a blank
        line above it. A previous line that opens a block gets none either,
        since that increases the indent.
        """
        start = match.start()
        if start == 0 or inside_ignored_block(config, html, match):
            return match.group()

        if inside_html_attribute(html, match):
            return match.group()

        line_start = match.string.rfind("\n", 0, start) + 1
        if match.string[line_start:start].strip():
            return match.group()

        if match.string[start - 1] == "\n":
            prev_start = match.string.rfind("\n", 0, start - 1) + 1

            if attach_comments and _COMMENT_LINE_PATTERN.fullmatch(
                match.string, prev_start, start - 1
            ):
                return match.group()

            if opening_line.fullmatch(match.string, prev_start, start - 1):
                return match.group()

        return "\n" + match.group()

    if config.blank_line_before_tag:
        comment_lines = r"(?:^[ \t]*(?:\{#[^\n]*?#\}|<!--[^\n]*?-->)[ \t]*\n)*"
        opening_line = _opening_line_pattern(config)
        for tag in split_option_list(config.blank_line_before_tag):
            attach_comments = not tag.startswith("end")
            func = partial(
                add_blank_line_before,
                config,
                html,
                opening_line,
                attach_comments,
            )
            html = re.sub(
                rf"(?<!^\n)({comment_lines if attach_comments else ''}(?:{{%[-+]?\s*?{tag}\b[^}}]+?[-+]?%}}\n?)+)",
                func,
                html,
                flags=RE_FLAGS_IMS,
            )

    def yaml_add_blank_line_after(html: str, match: re.Match[str]) -> str:
        """Add a blank line after yaml front matter that has none."""
        if html.startswith("\n\n", match.end()):
            return match.group()

        return match.group() + "\n"

    if not config.no_line_after_yaml:
        func = partial(yaml_add_blank_line_after, html)
        html = _YAML_FRONT_MATTER_PATTERN.sub(func, html)

    return html


def _template_block_key(tag: str, contents: str) -> tuple[str, str]:
    """Identify a template block by what it is, not by where it is.

    All whitespace is dropped: the two sides being compared differ in line
    breaks and indentation, and indenting also respaces template tags
    ("{{x}}" -> "{{ x }}").
    """
    return tag.lower(), "".join(contents.split())


def _multiline_template_blocks(
    authored_html: str | None, config: Config
) -> Counter[tuple[str, str]]:
    """Count simple template blocks that were authored across lines.

    The condensing pass runs over the expanded html, whose blocks do not
    line up one for one with the authored ones: expanding splits some lines
    and joins others, and a block inside an attribute is matched in one and
    not the other. Key the blocks by tag and contents so each is looked up
    rather than paired off by position.
    """
    if authored_html is None:
        return Counter()

    authored_html = "\n".join(authored_html.splitlines())
    if "{%" not in authored_html or "\n" not in authored_html:
        return Counter()

    return Counter(
        _template_block_key(match.group(1), match.group(2))
        for match in re.finditer(
            rf"""
            {{%[-+]?[ ]*?({config.optional_single_line_template_tags})\b(?:(?!\n|%}}).)*?%}}
            ([^%]*?)
            {{%[-+]?[ ]+?end\1[ ]*?%}}
            """,
            authored_html,
            flags=RE_FLAGS_IMX,
        )
        if "\n" in match.group(2) and match.group(2).strip()
    )


def _rendered_whitespace(text: str, left: str, right: str) -> str:
    """Whitespace at the edge of an element's content, as it renders.

    Css collapses each run of space, tab and line break to one space, then
    drops that space where it falls against a line edge or against other
    collapsible whitespace, since the neighbour renders it instead. Whatever
    is left over is layout this formatter owns rather than content, so it
    goes. Other whitespace (e.g. u+2005) is never collapsed or dropped.

    `left` and `right` are the single characters the whitespace sits
    between, each empty at the edge of the document.
    """
    text = _COLLAPSIBLE_WHITESPACE_PATTERN.sub(" ", text)
    if text.startswith(" ") and (
        not left or left in _COLLAPSIBLE_WHITESPACE_CHARS
    ):
        text = text[1:]
    if text.endswith(" ") and (
        not right or right in _COLLAPSIBLE_WHITESPACE_CHARS
    ):
        text = text[:-1]
    return text


def condense_html(
    html: str, config: Config, authored_html: str | None = None
) -> str:
    """Put short tags back on a single line."""
    if config.preserve_leading_space:
        return html

    blank_line_after_patterns = (
        tuple(
            re.compile(
                rf"((?:{{%[-+]?\s*?{tag.strip()}[^}}]+?[-+]?%}}\n?)+)",
                RE_FLAGS_IMS,
            )
            for tag in config.blank_line_after_tag.split(",")
        )
        if config.blank_line_after_tag
        else ()
    )
    blank_line_before_patterns = (
        tuple(
            re.compile(
                rf"((?:{{%[-+]?\s*?{tag.strip()}[^}}]+?[-+]?%}}\n?)+)",
                RE_FLAGS_IMS,
            )
            for tag in config.blank_line_before_tag.split(",")
        )
        if config.blank_line_before_tag
        else ()
    )

    def condense_line(
        config: Config, html: str, match: re.Match[str], *, inline: bool
    ) -> str:
        """Put contents on a single line if below max line length.

        `inline` says whether the element shares a line box with what sits
        either side of it, so that whitespace at its edges can render. A
        block starts and ends one of its own, where css drops it.

        With content present, each side is bounded by that content, which
        never starts or ends with whitespace, so only the outer neighbour
        can render the space. With none, the tags enclose a single run and
        both neighbours are outside it.
        """
        leading = trailing = ""
        if match.start(4) > match.end(1):
            opening_tag_start = match.end(1) - len(match.group(1).lstrip())
            end = match.end()
            before = (
                match.string[opening_tag_start - 1 : opening_tag_start]
                if inline and opening_tag_start
                else ""
            )
            after = match.string[end : end + 1] if inline else ""
            content = match.group(3)
            if content:
                leading = _rendered_whitespace(
                    match.string[match.end(1) : match.start(3)],
                    before,
                    content[0],
                )
                trailing = _rendered_whitespace(
                    match.string[match.end(3) : match.start(4)],
                    content[-1],
                    after,
                )
            else:
                leading = _rendered_whitespace(
                    match.string[match.end(1) : match.start(4)], before, after
                )

        holds_back_multiline_content = (
            config.line_break_after_multiline_tag
            and bool(match.group(3))
            and "\n" in match.group(1).strip()
        )
        if holds_back_multiline_content:
            combined_length = config.max_line_length + 1
        else:
            combined_length = len(
                match.group(1).splitlines()[-1]
                + leading
                + match.group(3)
                + trailing
                + match.group(4)
            )

        if (
            combined_length < config.max_line_length
            and not inside_ignored_block(config, html, match)
            and if_blank_line_after_match(match.group(3))
            and if_blank_line_before_match(match.group(3))
        ):
            return (
                match.group(1)
                + leading
                + match.group(3)
                + trailing
                + match.group(4)
            )

        return match.group()

    def if_blank_line_after_match(html: str) -> bool:
        """Check if there should be a blank line after."""
        for pattern in blank_line_after_patterns:
            if pattern.search(html):
                return False
        return True

    def if_blank_line_before_match(html: str) -> bool:
        """Check if there should be a blank line before."""
        for pattern in blank_line_before_patterns:
            if pattern.search(html):
                return False
        return True

    def condense_html_line(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        return condense_line(
            config,
            html,
            match,
            inline=match.group(2).lower() in HTML_INLINE_ELEMENTS,
        )

    func = partial(condense_html_line, config, html)

    html = re.sub(
        rf"(<({config.optional_single_line_html_tags})\b(?:\"[^\"]*\"|'[^']*'|{{{{[^}}]*}}}}|{{[^}}]*}}|[^'\">{{}}])*>)\s*([^<\n]*?)\s*?(</(\2)>)",
        func,
        html,
        flags=RE_FLAGS_IMSX,
    )

    multiline_blocks = _multiline_template_blocks(authored_html, config)

    def condense_template_line(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        """Put a short template block back on one line.

        One block of a kind stays spread for each one the author wrote that
        way. A template block lays out no box of its own, so its body runs
        on with the text either side and whitespace at its edges renders.
        """
        if inside_html_attribute(html, match):
            return match.group()

        key = _template_block_key(match.group(2), match.group(3))
        if multiline_blocks[key]:
            multiline_blocks[key] -= 1
            return match.group()

        return condense_line(config, html, match, inline=True)

    func = partial(condense_template_line, config, html)
    return re.sub(
        rf"((?:\s|^){{%[-+]?[ ]*?({config.optional_single_line_template_tags})\b(?:(?!\n|%}}).)*?%}})\s*([^%\n]*?)\s*?({{%[-+]?[ ]+?end(\2)[ ]*?%}})",
        func,
        html,
        flags=RE_FLAGS_IMX,
    )
