"""Condense HTML.

1. Put short html tags back on one line
2. Put short template tags back on one line
"""

from functools import partial

import regex as re

from ..helpers import (
    inside_ignored_block,
    inside_protected_trans_block,
    is_safe_closing_tag,
)
from ..settings import Config


def clean_whitespace(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line

    def strip_space(config: Config, html: str, match: re.Match) -> str:
        """Trim leading whitespace."""
        # either inside a block, or this is a newline + closing block tag.
        # if it is a newline + closing block we can format it.

        if inside_ignored_block(config, html, match) and not is_safe_closing_tag(
            config, match.group()
        ):
            return match.group()

        # trimmed blocks should not be here.
        # we need to full html to check what type of
        # opening block it was - trimmed or not trimmed
        if inside_protected_trans_block(config, html[: match.end()], match):
            return match.group().rstrip()

        lines = len(
            re.findall(
                r"\n",
                match.group(2),
            )
        )
        blank_lines = "\n" * lines
        if lines > config.max_blank_lines:
            blank_lines = "\n" * max(config.max_blank_lines, 0)
        return match.group(1) + blank_lines

    func = partial(strip_space, config, html)

    line_contents = r"(.*?)"
    trailing_contents = r"\n \t"

    if config.preserve_blank_lines:
        line_contents = r"([^\n]+?)"
        trailing_contents = r" \t"

    if not config.preserve_leading_space:
        # remove any leading/trailing space
        html = re.sub(
            re.compile(rf"^[ \t]*{line_contents}([{trailing_contents}]*)$", re.M),
            func,
            html,
        )

    else:
        # only remove leading space in front of tags
        # <, {%
        html = re.sub(
            re.compile(rf"^[ \t]*((?:<|{{%).*?)([{trailing_contents}]*)$", re.M),
            func,
            html,
        )
        html = re.sub(
            re.compile(rf"^{line_contents}([{trailing_contents}]*)$", re.M), func, html
        )

    def add_blank_line_after(config: Config, html: str, match: re.Match) -> str:
        """Add break after if not in ignored block."""
        if inside_ignored_block(config, html, match):
            return match.group()

        # check that next line is not blank.
        if html[match.end() : match.end() + 1] != "\n":  # noqa:E203
            return match.group() + "\n"

        return match.group()

    func = partial(add_blank_line_after, config, html)

    # should we add blank lines after load tags?
    if config.blank_line_after_tag:
        for tag in [x.strip() for x in config.blank_line_after_tag.split(",")]:
            html = re.sub(
                re.compile(
                    rf"((?:{{%\s*?{tag}\b[^}}]+?%}}\n?)+)",
                    re.IGNORECASE | re.MULTILINE | re.DOTALL,
                ),
                func,
                html,
            )

    def add_blank_line_before(config: Config, html: str, match: re.Match) -> str:
        """Add break before if not in ignored block and not first line in file."""
        if inside_ignored_block(config, html, match) or match.start() == 0:
            return match.group()

        return "\n" + match.group()

    func = partial(add_blank_line_before, config, html)

    # should we add blank lines before load tags?
    if config.blank_line_before_tag:
        for tag in [x.strip() for x in config.blank_line_before_tag.split(",")]:
            html = re.sub(
                re.compile(
                    rf"(?<!^\n)((?:{{%\s*?{tag}\b[^}}]+?%}}\n?)+)",
                    re.IGNORECASE | re.MULTILINE | re.DOTALL,
                ),
                func,
                html,
            )

    # add line after yaml front matter

    def yaml_add_blank_line_after(html: str, match: re.Match) -> str:
        """Add break after if not in ignored block."""
        if match.start() == 0 and not html.startswith("\n\n", match.end()):
            # verify there are not already blank lines
            return match.group() + "\n"

        return match.group()

    if config.no_line_after_yaml is False:
        func = partial(yaml_add_blank_line_after, html)
        html = re.sub(
            re.compile(
                r"(^---.+?---)$",
                re.MULTILINE | re.DOTALL,
            ),
            func,
            html,
        )

    return html


def condense_html(html, config):
    """Put short tags back on a single line."""
    if config.preserve_leading_space:
        # if a user is attempting to reuse any leading
        # space for other purposes, we should not try to remove it.
        return html

    def condense_line(config: Config, html: str, match: re.Match) -> str:
        """Put contents on a single line if below max line length."""
        if config.line_break_after_multiline_tag:
            # always force a break by pretending the line is too long.
            combined_length = config.max_line_length + 1
        else:
            combined_length = len(
                match.group(1).splitlines()[-1] + match.group(3) + match.group(4)
            )

        if (
            not inside_ignored_block(config, html, match)
            and combined_length < config.max_line_length
            and if_blank_line_after_match(config, match.group(3))
            and if_blank_line_before_match(config, match.group(3))
        ):
            return match.group(1) + match.group(3) + match.group(4)

        return match.group()

    def if_blank_line_after_match(config: Config, html: str) -> bool:
        """Check if there should be a blank line after."""
        if config.blank_line_after_tag:
            return not any(
                re.findall(
                    re.compile(
                        rf"((?:{{%\s*?{tag}[^}}]+?%}}\n?)+)",
                        re.IGNORECASE | re.MULTILINE | re.DOTALL,
                    ),
                    html,
                )
                for tag in [x.strip() for x in config.blank_line_after_tag.split(",")]
            )
        return True

    def if_blank_line_before_match(config: Config, html: str) -> bool:
        """Check if there should be a blank line before."""
        if config.blank_line_before_tag:
            return not any(
                re.findall(
                    re.compile(
                        rf"((?:{{%\s*?{tag}[^}}]+?%}}\n?)+)",
                        re.IGNORECASE | re.MULTILINE | re.DOTALL,
                    ),
                    html,
                )
                for tag in [x.strip() for x in config.blank_line_before_tag.split(",")]
            )
        return True

    # add blank lines before tags
    func = partial(condense_line, config, html)

    # put short single line tags on one line
    html = re.sub(
        re.compile(
            rf"(<({config.optional_single_line_html_tags})\b(?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)\s*([^<\n]*?)\s*?(</(\2)>)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE,
        ),
        func,
        html,
    )

    # put short template tags back on one line. must have leading space
    # jinja +%} and {%+ intentionally omitted.
    html = re.sub(
        re.compile(
            rf"((?:\s|^){{%-?[ ]*?({config.optional_single_line_template_tags})\b(?:(?!\n|%}}).)*?%}})\s*([^%\n]*?)\s*?({{%-?[ ]+?end(\2)[ ]*?%}})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        func,
        html,
    )

    return html
