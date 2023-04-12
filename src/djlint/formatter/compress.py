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

        close = match.group(3) if "/" not in match.group(3) else f" {match.group(3)}"

        # pylint: disable=C0209
        return "{} {}{}".format(
            match.group(1),
            " ".join(x.strip() for x in match.group(2).strip().splitlines()),
            close,
        )

    # put attributes on one line
    html = re.sub(
        re.compile(
            rf"(<(?:{config.indent_html_tags}))\s((?:\s*?(?:\"[^\"]*\"|'[^']*'|{{{{(?:(?!}}}}).)*}}}}|{{%(?:(?!%}}).)*%}}|[^'\">{{}}\/\s]))+)\s*?(/?>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _flatten_attributes,
        html,
    )

    # put closing tags back on one line
    # <a ...
    #     >
    html = re.sub(
        re.compile(
            rf"(</(?:{config.indent_html_tags}))\s*?(>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        r"\1\2",
        html,
    )

    # remove extra space from empty tags
    # <a >
    #   ^
    html = re.sub(
        re.compile(
            rf"(<(?:{config.indent_html_tags}))\s*?(>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        r"\1\2",
        html,
    )

    # ensure space before closing tag
    # <a />
    #   ^
    html = re.sub(
        re.compile(
            rf"(<(?:{config.indent_html_tags}))\s*?(/>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        r"\1 \2",
        html,
    )

    # cleanup whitespace in doctype
    html = re.sub(
        re.compile(
            r"(<!(?:doctype))\s((?:\s*?(?:\"[^\"]*\"|'[^']*'|{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|[^'\">{}\/\s]))+)\s*?(>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        r"\1 \2\3",
        html,
    )

    return html
