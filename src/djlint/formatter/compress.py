"""Compress html.

1. flatten attributes
"""

import regex as re
from HtmlTagNames import html_tag_names

from ..helpers import child_of_ignored_block
from ..settings import Config


def compress_html(html: str, config: Config) -> str:
    """Compress html."""

    def _fix_case(tag):
        if config.ignore_case is False and tag.lower() in html_tag_names:
            return tag.lower()
        return tag

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
        return "<{} {}{}".format(
            _fix_case(match.group(1)),
            " ".join(x.strip() for x in match.group(2).strip().splitlines()),
            close,
        )

    # put attributes on one line
    html = re.sub(
        re.compile(
            rf"<({config.indent_html_tags})\s((?:\s*?(?:\"[^\"]*\"|'[^']*'|{{{{(?:(?!}}}}).)*}}}}|{{%(?:(?!%}}).)*%}}|[^'\">{{}}\/\s]))+)\s*?(/?>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _flatten_attributes,
        html,
    )

    def _closing_clean_space(match):
        return f"</{_fix_case(match.group(1))}>"

    # put closing tags back on one line
    # <a ...
    #     >
    html = re.sub(
        re.compile(
            rf"</({config.indent_html_tags})\s*?>",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _closing_clean_space,
        html,
    )

    def _emtpy_clean_space(match):
        return f"<{_fix_case(match.group(1))}>"

    # remove extra space from empty tags
    # <a >
    #   ^
    html = re.sub(
        re.compile(
            rf"<({config.indent_html_tags})\s*?>",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _emtpy_clean_space,
        html,
    )

    def _void_clean_space(match):
        return f"<{_fix_case(match.group(1))} />"

    # ensure space before closing tag
    # <a />
    #   ^
    html = re.sub(
        re.compile(
            rf"<({config.indent_html_tags})\s*?/>",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _void_clean_space,
        html,
    )

    def _doctype_clean_space(match):
        if config.ignore_case is False:
            return f"<!DOCTYPE {match.group(2)}>"
        return f"<!{match.group(1)} {match.group(2)}>"

    # cleanup whitespace in doctype
    html = re.sub(
        re.compile(
            r"<!(doctype)\s((?:\s*?(?:\"[^\"]*\"|'[^']*'|{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|[^'\">{}\/\s]))+)\s*?>",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        _doctype_clean_space,
        html,
    )

    return html
