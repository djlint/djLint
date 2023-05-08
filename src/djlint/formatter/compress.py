"""Compress html.

1. flatten attributes
"""

import regex as re
from HtmlTagNames import html_tag_names
from HtmlVoidElements import html_void_elements

from ..helpers import child_of_unformatted_block
from ..settings import Config


def compress_html(html: str, config: Config) -> str:
    """Compress html."""

    def _fix_case(tag):
        if config.ignore_case is False and tag.lower() in html_tag_names:
            return tag.lower()

        if config.ignore_case is False and tag.lower() == "doctype":
            return "DOCTYPE"
        return tag

    def _clean_tag(match: re.Match) -> str:
        """Flatten multiline attributes back to one line.

        Skip when attribute is ignored.
        Attribute name can be in group one or group 2.
        for now, skipping if they are anywhere

        tags starting ignored blocks can have their attributes formatted,
        for example <textarea class="..." id="..."> can be formatted.
        """
        if child_of_unformatted_block(config, html, match):
            return match.group()

        open_braket = match.group(1)
        tag = _fix_case(match.group(2))

        attributes = (
            (" " + " ".join(x.strip() for x in match.group(3).strip().splitlines()))
            if match.group(3)
            else ""
        )
        if tag.lower() in html_void_elements and config.close_void_tags:
            close_braket = " />"
        else:
            close_braket = (
                match.group(4) if "/" not in match.group(4) else f" {match.group(4)}"
            )

        return f"{open_braket}{tag}{attributes}{close_braket}"

    html = re.sub(
        re.compile(
            config.html_tag_regex,
            flags=re.MULTILINE | re.VERBOSE | re.IGNORECASE,
        ),
        _clean_tag,
        html,
    )

    return html
