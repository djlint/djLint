"""Expand html.

1. put html tags on individual lines, if needed.
2. put template tags on individual lines, if needed.
"""

from functools import partial

import regex as re

from ..helpers import inside_ignored_block, inside_template_block
from ..settings import Config


def expand_html(html: str, config: Config) -> str:
    """Split single line html into many lines based on tags."""

    def add_html_line(out_format: str, match: re.Match) -> str:
        """Add whitespace.

        Do not add whitespace if the tag is in a non indent block.

        Do not add whiatespace if the tag is a in a template block
        """
        if inside_ignored_block(config, html, match):
            return match.group(1)

        if inside_template_block(config, html, match):
            return match.group(1)

        if out_format == "\n%s" and match.start() == 0:
            return match.group(1)

        return out_format % match.group(1)

    html_tags = config.break_html_tags

    add_left = partial(add_html_line, "\n%s")
    add_right = partial(add_html_line, "%s\n")

    break_char = config.break_before

    # html tags - break before
    html = re.sub(
        re.compile(
            rf"{break_char}\K(</?(?:{html_tags})\b(\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)",
            flags=re.IGNORECASE | re.VERBOSE,
        ),
        add_left,
        html,
    )

    # html tags - break after
    html = re.sub(
        re.compile(
            rf"(</?(?:{html_tags})\b(\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)(?!\s*?\n)(?=[^\n])",
            flags=re.IGNORECASE | re.VERBOSE,
        ),
        add_right,
        html,
    )

    # template tag breaks
    def should_i_move_template_tag(out_format: str, match: re.Match) -> str:
        # ensure template tag is not inside an html tag and also not the first line of the file

        if inside_ignored_block(config, html, match):
            return match.group(1)
        if not re.findall(
            r"\<(?:"
            + str(config.indent_html_tags)
            + r")\b(?:\"[^\"]*\"|'[^']*'|{{[^}]*}}|{%[^%]*%}|{\#[^\#]*\#}|[^>{}])*?"
            # original
            # + r")\b(?:[^>]|{%[^(?:%}]*?%}|{{[^(?:}}]*?}})*?"
            + re.escape(match.group(1)) + "$",
            html[: match.end()],
            re.MULTILINE | re.VERBOSE,
        ):
            if out_format == "\n%s" and match.start() == 0:
                return match.group(1)
            return out_format % match.group(1)

        return match.group(1)

    # template tags
    # break before
    html = re.sub(
        re.compile(
            break_char
            + r"\K((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        partial(should_i_move_template_tag, "\n%s"),
        html,
    )

    # break after
    html = re.sub(
        re.compile(
            r"((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})(?=[^\n])",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        partial(should_i_move_template_tag, "%s\n"),
        html,
    )

    return html
