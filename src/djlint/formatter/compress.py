"""Compress html.

1. flatten attributes
"""

import regex as re

from ..helpers import child_of_ignored_block
from ..settings import Config


def compress_html(html: str, config: Config) -> str:
    """Compress html."""

    def _flatten_attributes(match: re.Match) -> str:
        """Flatten multiline attributes back to one line.

        Skip when attribute is ignored.
        Attribute name can be in group one or group 2.
        for now, skipping if they are anywhere

        tags starting ignored blocks can have their attributes formatted,
        for example <textarea class="..." id="..."> can be formatted.
        """
        if child_of_ignored_block(config, html, match):
            return match.group()

        # pylint: disable=C0209
        return "{} {}{}".format(
            match.group(1),
            " ".join(x.strip() for x in match.group(2).strip().splitlines()),
            match.group(3),
        )

    # put attributes on one line
    html = re.sub(
        re.compile(
            rf"(<(?:{config.indent_html_tags}))\s((?:\"[^\"]*\"|'[^']*'|{{{{(?:(?!}}}}).)*}}}}|{{%(?:(?!%}}).)*%}}|[^'\">{{}}])+)(/?>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _flatten_attributes,
        html,
    )

    return html
