"""Condense HTML.

1. Put short html tags back on one line
2. Put short template tags back on one line
"""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import regex as re

from djlint.const import HTML_INLINE_ELEMENTS
from djlint.helpers import (
    RE_FLAGS_IMS,
    RE_FLAGS_IMSX,
    RE_FLAGS_IMX,
    RE_FLAGS_MS,
    inside_html_attribute,
    inside_ignored_block,
    inside_protected_trans_block,
    is_safe_closing_tag,
)

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_YAML_FRONT_MATTER_PATTERN: Final = re.compile(
    r"(^---.+?---)$", RE_FLAGS_MS, cache_pattern=False
)

# whitespace that css collapses; other whitespace (e.g. u+2005) is rendered.
_COLLAPSIBLE_WHITESPACE_PATTERN: Final = re.compile(
    r"[ \t\n\r\f]+", cache_pattern=False
)

# a line that closes a block and decreases the indentation.
_CLOSING_LINE_PATTERN: Final = re.compile(
    r"[ \t]*(?:</|\{%-?\s*end|\{\{/)", cache_pattern=False
)

# a whole line holding a single-line comment.
_COMMENT_LINE_PATTERN: Final = re.compile(
    r"[ \t]*(?:\{#[^\n]*?#\}|<!--[^\n]*?-->)[ \t]*", cache_pattern=False
)


def clean_whitespace(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line

    def strip_space(config: Config, html: str, match: re.Match[str]) -> str:
        """Trim leading whitespace."""
        # either inside a block, or this is a newline + closing block tag.
        # if it is a newline + closing block we can format it.

        if inside_ignored_block(
            config, html, match
        ) and not is_safe_closing_tag(config, match.group()):
            return match.group()

        # trimmed blocks should not be here.
        # we need to full html to check what type of
        # opening block it was - trimmed or not trimmed
        if inside_protected_trans_block(config, html[: match.end()], match):
            return match.group().rstrip()

        lines = match.group(2).count("\n")
        blank_lines = "\n" * lines
        if lines > config.max_blank_lines:
            blank_lines = "\n" * max(config.max_blank_lines, 0)
        return match.group(1) + blank_lines

    func = partial(strip_space, config, html)

    line_contents = r"(.*?)"
    trailing_contents = r"\n \t"

    if config.preserve_blank_lines:
        line_contents = r"([^\n]*?)"
        trailing_contents = r" \t"

    if not config.preserve_leading_space:
        # remove any leading/trailing space
        html = re.sub(
            rf"^[ \t]*{line_contents}([{trailing_contents}]*)$",
            func,
            html,
            flags=re.M,
        )

    else:
        # only remove leading space in front of tags
        # <, {%
        html = re.sub(
            rf"^[ \t]*((?:<|{{%).*?)([{trailing_contents}]*)$",
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

        # no blank line when the next line closes a block (decreased indent).
        next_line = match.string[match_end:].split("\n", 1)[0]
        if _CLOSING_LINE_PATTERN.match(next_line):
            return match.group()

        return match.group() + "\n"

    func = partial(add_blank_line_after, config, html)

    # should we add blank lines after load tags?
    if config.blank_line_after_tag:
        for tag in config.blank_line_after_tag.split(","):
            html = re.sub(
                rf"((?:{{%-?\s*?{tag.strip()}\b[^}}]+?-?%}}\n?)+)",
                func,
                html,
                flags=RE_FLAGS_IMS,
            )

    def add_blank_line_before(
        config: Config,
        html: str,
        attach_comments: bool,  # noqa: FBT001
        match: re.Match[str],
    ) -> str:
        """Add break before if not in ignored block and not first line in file."""
        if match.start() == 0 or inside_ignored_block(config, html, match):
            return match.group()

        # a comment line directly above belongs to this tag. if it was not
        # swallowed into the match, there is already a blank line above it.
        start = match.start()
        if attach_comments and match.string[start - 1] == "\n":
            prev_start = match.string.rfind("\n", 0, start - 1) + 1
            if _COMMENT_LINE_PATTERN.fullmatch(
                match.string, prev_start, start - 1
            ):
                return match.group()

        return "\n" + match.group()

    # should we add blank lines before load tags?
    if config.blank_line_before_tag:
        # keep comments attached to the tag they document: the blank line
        # goes above any comment lines directly preceding the tag. a comment
        # above an end tag is block content, not the end tag's comment.
        comment_lines = r"(?:^[ \t]*(?:\{#[^\n]*?#\}|<!--[^\n]*?-->)[ \t]*\n)*"
        for raw_tag in config.blank_line_before_tag.split(","):
            tag = raw_tag.strip()
            attach_comments = not tag.startswith("end")
            func = partial(add_blank_line_before, config, html, attach_comments)
            html = re.sub(
                rf"(?<!^\n)({comment_lines if attach_comments else ''}(?:{{%-?\s*?{tag}\b[^}}]+?-?%}}\n?)+)",
                func,
                html,
                flags=RE_FLAGS_IMS,
            )

    # add line after yaml front matter

    def yaml_add_blank_line_after(html: str, match: re.Match[str]) -> str:
        """Add break after if not in ignored block."""
        match_start, match_end = match.span()
        if match_start == 0 and not html.startswith("\n\n", match_end):
            # verify there are not already blank lines
            return match.group() + "\n"

        return match.group()

    if not config.no_line_after_yaml:
        func = partial(yaml_add_blank_line_after, html)
        html = _YAML_FRONT_MATTER_PATTERN.sub(func, html)

    return html


def _multiline_template_block_states(
    source: str | None, config: Config
) -> list[bool]:
    """Track simple template blocks that were authored across lines."""
    if source is None:
        return []

    source = "\n".join(source.splitlines())
    if "{%" not in source or "\n" not in source:
        return []

    return [
        "\n" in match.group(2) and bool(match.group(2).strip())
        for match in re.finditer(
            rf"""
            (?:\s|^)
            {{%-?[ ]*?({config.optional_single_line_template_tags})\b(?:(?!\n|%}}).)*?%}}
            ([^%]*?)
            {{%-?[ ]+?end\1[ ]*?%}}
            """,
            source,
            flags=RE_FLAGS_IMX,
        )
    ]


def condense_html(html: str, config: Config, source: str | None = None) -> str:
    """Put short tags back on a single line."""
    if config.preserve_leading_space:
        # if a user is attempting to reuse any leading
        # space for other purposes, we should not try to remove it.
        return html

    blank_line_after_patterns = (
        tuple(
            re.compile(
                rf"((?:{{%-?\s*?{tag.strip()}[^}}]+?-?%}}\n?)+)", RE_FLAGS_IMS
            )
            for tag in config.blank_line_after_tag.split(",")
        )
        if config.blank_line_after_tag
        else ()
    )
    blank_line_before_patterns = (
        tuple(
            re.compile(
                rf"((?:{{%-?\s*?{tag.strip()}[^}}]+?-?%}}\n?)+)", RE_FLAGS_IMS
            )
            for tag in config.blank_line_before_tag.split(",")
        )
        if config.blank_line_before_tag
        else ()
    )

    def condense_line(config: Config, html: str, match: re.Match[str]) -> str:
        """Put contents on a single line if below max line length."""
        # whitespace-only content of an inline element is rendered; collapse
        # it to one space instead of dropping it. template tag names never
        # match the inline element set, so the template path is unaffected.
        whitespace = ""
        if (
            not match.group(3)
            and match.start(4) > match.end(1)
            and match.group(2).lower() in HTML_INLINE_ELEMENTS
        ):
            whitespace = _COLLAPSIBLE_WHITESPACE_PATTERN.sub(
                " ", match.string[match.end(1) : match.start(4)]
            )

        if config.line_break_after_multiline_tag:
            # always force a break by pretending the line is too long.
            combined_length = config.max_line_length + 1
        else:
            combined_length = len(
                match.group(1).splitlines()[-1]
                + whitespace
                + match.group(3)
                + match.group(4)
            )

        if (
            combined_length < config.max_line_length
            and not inside_ignored_block(config, html, match)
            and if_blank_line_after_match(match.group(3))
            and if_blank_line_before_match(match.group(3))
        ):
            return match.group(1) + whitespace + match.group(3) + match.group(4)

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

    # add blank lines before tags
    func = partial(condense_line, config, html)

    # put short single line tags on one line
    html = re.sub(
        rf"(<({config.optional_single_line_html_tags})\b(?:\"[^\"]*\"|'[^']*'|{{{{[^}}]*}}}}|{{[^}}]*}}|[^'\">{{}}])*>)\s*([^<\n]*?)\s*?(</(\2)>)",
        func,
        html,
        flags=RE_FLAGS_IMSX,
    )

    template_block_states = iter(
        _multiline_template_block_states(source, config)
    )

    def condense_template_line(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        try:
            was_authored_multiline = next(template_block_states)
        except StopIteration:
            was_authored_multiline = False

        if was_authored_multiline or inside_html_attribute(html, match):
            return match.group()

        return condense_line(config, html, match)

    # put short template tags back on one line. must have leading space
    # jinja +%} and {%+ intentionally omitted.
    func = partial(condense_template_line, config, html)
    return re.sub(
        rf"((?:\s|^){{%-?[ ]*?({config.optional_single_line_template_tags})\b(?:(?!\n|%}}).)*?%}})\s*([^%\n]*?)\s*?({{%-?[ ]+?end(\2)[ ]*?%}})",
        func,
        html,
        flags=RE_FLAGS_IMX,
    )
