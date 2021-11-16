"""Compress html.

1. flatten attributes
"""


from functools import partial

import regex as re

from ..helpers import inside_ignored_block
from ..settings import Config


def compress_html(html: str, config: Config) -> str:
    """Compress html."""

    def _flatten_attributes(config: Config, html: str, match: re.Match) -> str:
        """Flatten multiline attributes back to one line.

        Skip when attribute is ignored.
        Attribute name can be in group one or group 2.
        for now, skipping if they are anywhere
        """
        if inside_ignored_block(config, html, match):
            return match.group()
        # pylint: disable=C0209
        return "{} {}{}".format(
            match.group(1),
            " ".join(x.strip() for x in match.group(2).strip().splitlines()),
            match.group(3),
        )

    func = partial(_flatten_attributes, config, html)

    # put attributes on one line
    html = re.sub(
        re.compile(
            fr"(<(?:{config.indent_html_tags})\b)((?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])+)(/?>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        func,
        html,
    )

    return html
