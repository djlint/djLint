"""Compress html.

1. flatten attributes
"""

import regex as re

from ..settings import Config


def compress_html(html: str, config: Config) -> str:
    """Compress html."""

    def _flatten_attributes(match: re.Match) -> str:
        """Flatten multiline attributes back to one line.

        Skip when attribute is ignored.
        Attribute name can be in group one or group 2.
        for now, skipping if they are anywhere

        even ignored blocks attributes can be formatted.
        """
        # pylint: disable=C0209
        return "{} {}{}".format(
            match.group(1),
            " ".join(x.strip() for x in match.group(2).strip().splitlines()),
            match.group(3),
        )

    # put attributes on one line
    html = re.sub(
        re.compile(
            rf"(<(?:{config.indent_html_tags})\b)((?:\"[^\"]*\"|'[^']*'|{{{{(?:(?!}}}}).)*}}}}|{{%(?:(?!%}}).)*%}}|[^'\">{{}}])+)(/?>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _flatten_attributes,
        html,
    )

    return html
