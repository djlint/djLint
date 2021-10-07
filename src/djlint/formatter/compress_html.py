"""djLint Attempt to logically shrink html."""

from functools import partial

import regex as re

from ..helpers import inside_ignored_block
from ..settings import Config


def compress_html(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line

    def trip_space(config: Config, html: str, match: re.Match) -> str:
        """Trim leading whitepsace."""
        if inside_ignored_block(config, html, match):
            return match.group()
        return match.group(1)

    func = partial(trip_space, config, html)

    html = re.sub(re.compile(r"^\s*(.*?)\s*$", re.M), func, html)

    # put short single line tags on one line
    html = re.sub(
        re.compile(
            fr"(<({config.optional_single_line_html_tags})(?:\s(?:(?:{{%[^(?:%}}]*?%}})|(?:{{{{[^(?:}}}})]*?}}}})|[^<>])*)?>)\s*([^<\n]{{,80}})\s*?(</(\2)>)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE,
        ),
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    # put short template tags back on one line
    html = re.sub(
        re.compile(
            rf"({{%-?[ ]*?({config.optional_single_line_template_tags})[^\n(?:%}})]{{,30}}%}})\s*([^%\n]{{,50}})\s*?({{%-?[ ]+?end(\2)[ ]*?%}})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        r"\1\3\4",
        html,
    )

    return html
