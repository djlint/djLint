"""djLint expand out html code."""
import re as old_re
from functools import partial

import regex as re

from ..settings import (
    break_html_tags,
    break_template_tags,
    ignored_attributes,
    ignored_blocks,
    tag_pattern,
)


def _flatten_attributes(match):
    """Flatten multiline attributes back to one line.

    Skip when attribute is ignored.
    Attribute name can be in group one or group 2.
    for now, skipping if they are anywhere
    """
    for attribute in ignored_attributes:
        if attribute in match.group():
            return match.group()

    return "{} {}{}".format(
        match.group(1),
        " ".join(match.group(2).strip().splitlines()),
        match.group(3),
    )


def _should_ignore(html, match):
    """Do not add whitespace if the tag is in a non indent block."""
    for block in ignored_blocks:
        return any(
            ignored_match.start() < match.start(1)
            and ignored_match.end() > match.end(1)
            for ignored_match in re.finditer(
                block % re.escape(match.group(1)), html, re.DOTALL | re.IGNORECASE
            )
        )

    return False


def expand_html(html):
    """Split single line html into many lines based on tags."""

    def add_html_line(out_format, match):
        """Add whitespace.

        Do not add whitespace if the tag is in a non indent block.
        """
        if _should_ignore(html, match):
            return match.group(1)

        return out_format % match.group(1)

    # put attributes on one line
    html = old_re.sub(
        tag_pattern,
        _flatten_attributes,
        html,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    html_tags = "|".join(break_html_tags)

    # process opening tags ############

    # the tag either closes <div>
    # self closes <img />
    # has attributes <div text>
    # or has attributes and self closes <img text/>

    add_left = partial(add_html_line, "\n%s")
    add_right = partial(add_html_line, "%s\n")

    break_char = r"(?<!\n *?)"

    html = re.sub(
        r"%s\K(<(?:%s)>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"(<(?:%s)>)(?=[^\n])" % html_tags, add_right, html, flags=re.IGNORECASE
    )

    html = re.sub(
        r"%s\K(<(?:%s) ?/>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"(<(?:%s) ?/>)(?=[^\n])" % html_tags, add_right, html, flags=re.IGNORECASE
    )

    html = re.sub(
        r"%s\K(<(?:%s) [^>]*?[^/]>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"(<(?:%s) [^>]*?[^/]>)(?=[^\n])" % html_tags,
        add_right,
        html,
        flags=re.IGNORECASE,
    )

    html = re.sub(
        r"%s\K(<(?:%s) [^>]+?/>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"(<(?:%s) [^>]+?/>)(?=[^\n])" % html_tags, add_right, html, flags=re.IGNORECASE
    )

    # process closing (break_char, html_tags,)s ######

    html = re.sub(
        r"%s\K(</(?:%s)>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r"(</(?:%s)>)(?=[^\n])" % html_tags, add_right, html, flags=re.IGNORECASE
    )

    # template tag breaks

    def should_i_move_template_tag(out_format, match):
        # ensure template tag is not inside an html tag
        html_tags = "|".join(break_html_tags)

        if _should_ignore(html, match):
            return match.group(1)

        if not re.findall(
            r"\<(?:"
            + html_tags
            + r") .*? ?\w+=[\"][^\"]*?"
            + re.escape(match.group(1))
            + "$",
            html[: match.end()],
            re.MULTILINE,
        ):

            return out_format % match.group(1)

        return match.group(1)

    for tag in break_template_tags:
        # find all matching tags

        html = re.sub(
            r"%s\K(%s)"
            % (
                break_char,
                tag,
            ),
            partial(should_i_move_template_tag, "\n%s"),
            html,
            re.IGNORECASE | re.MULTILINE,
        )

        html = re.sub(
            r"(%s)(?=[^\n])" % tag,
            partial(should_i_move_template_tag, "%s\n"),
            html,
            re.IGNORECASE | re.MULTILINE,
        )

    return html
