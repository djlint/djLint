"""Condense HTML.

1. Put short html tags back on one line
2. Put short templage tags back on one line
"""

from functools import partial

import regex as re

from ..helpers import inside_ignored_block
from ..settings import Config


def condense_html(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line

    def strip_space(config: Config, html: str, match: re.Match) -> str:
        """Trim leading whitepsace."""
        if inside_ignored_block(config, html, match):
            return match.group()

        return match.group(1)

    func = partial(strip_space, config, html)

    html = re.sub(re.compile(r"^[ \t]*(.*?)[\n \t]*$", re.M), func, html)

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

    def condense_line(config: Config, match: re.Match) -> str:
        """Put contents on a single line if below max line length."""
        if (
            len(match.group(1) + match.group(3) + match.group(4))
            < config.max_line_length
        ) and if_blank_line_after_match(config, match.group(3)):
            return match.group(1) + match.group(3) + match.group(4)

        return match.group()

    def add_blank_line(config: Config, html: str, match: re.Match) -> str:
        """Add break after if not in ignored block."""
        if inside_ignored_block(config, html, match):
            return match.group()

        return match.group() + "\n"

    func = partial(add_blank_line, config, html)

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

    func = partial(condense_line, config)

    # put short single line tags on one line
    html = re.sub(
        re.compile(
            rf"(<({config.optional_single_line_html_tags})\b(?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)\s*([^<\n]*?)\s*?(</(\2)>)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE,
        ),
        func,
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    # put short template tags back on one line
    html = re.sub(
        re.compile(
            rf"({{%-?[ ]*?({config.optional_single_line_template_tags})[^\n(?:%}})]*?%}})\s*?([ ]*?[^%\n]*?[ ]*?)\s*?({{%-?[ ]+?end(\2)[ ]*?%}})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        func,
        html,
    )

    return html
