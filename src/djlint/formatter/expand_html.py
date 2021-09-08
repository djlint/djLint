"""djLint expand out html code."""
import re as old_re
from functools import partial

import regex as re

from ..settings import Config


def _flatten_attributes(config: Config, match: re.Match) -> str:
    """Flatten multiline attributes back to one line.

    Skip when attribute is ignored.
    Attribute name can be in group one or group 2.
    for now, skipping if they are anywhere
    """
    for attribute in config.ignored_attributes:
        if attribute in match.group():
            return match.group()

    return "{} {}{}".format(
        match.group(1),
        " ".join(x.strip() for x in match.group(2).strip().splitlines()),
        match.group(3),
    )


def _should_ignore(config: Config, html: str, match: re.Match) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    for block in config.ignored_blocks:
        return any(
            ignored_match.start() < match.start(1)
            and ignored_match.end() > match.end(1)
            for ignored_match in re.finditer(
                block % re.escape(match.group(1)),
                html,
                re.DOTALL | re.IGNORECASE | re.VERBOSE,
            )
        )

    return False


def expand_html(html: str, config: Config) -> str:
    """Split single line html into many lines based on tags."""

    def add_html_line(out_format: str, match: re.Match) -> str:
        """Add whitespace.

        Do not add whitespace if the tag is in a non indent block.
        """
        if _should_ignore(config, html, match):
            return match.group(1)

        return out_format % match.group(1)

    # put attributes on one line
    func = partial(_flatten_attributes, config)
    html = old_re.sub(
        config.tag_pattern,
        func,
        html,
        flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
    )

    html_tags = config.break_html_tags

    # process opening tags ############

    # the tag either opens <div>
    # self closes <img />
    # has attributes <div text>
    # or has attributes and self closes <img text/>

    add_left = partial(add_html_line, "\n%s")
    add_right = partial(add_html_line, "%s\n")

    break_char = r"(?<!\n[ ]*?)"

    html = re.sub(
        r"%s\K(<(?:%s)>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    # <tag>
    html = re.sub(
        r"(<(?:%s)>)(?=[^\n])" % html_tags,
        add_right,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    # \n<tag /> and \n<tag/>
    html = re.sub(
        r"%s\K(<(?:%s)[ ]?/>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    # <tag /> and <tag/>
    html = re.sub(
        r"(<(?:%s)[ ]?/>)(?=[^\n])" % html_tags,
        add_right,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    # \n<tag stuff/>,  \n<tag stuff>, \n<tag stuff />
    html = re.sub(
        r"%s\K(<(?:%s)[ ][^>]*?[^/]>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    # <tag stuff/>,  <tag stuff>, <tag stuff />
    html = re.sub(
        r"(<(?:%s)[ ][^>]*?[^/]>)(?=[^\n])" % html_tags,
        add_right,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    html = re.sub(
        r"%s\K(<(?:%s)[ ][^>]+?/>)"
        % (
            break_char,
            html_tags,
        ),
        add_left,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    html = re.sub(
        r"(<(?:%s)[ ][^>]+?/>)(?=[^\n])" % html_tags,
        add_right,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
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
        flags=re.IGNORECASE | re.VERBOSE,
    )
    html = re.sub(
        r"(</(?:%s)>)(?=[^\n])" % html_tags,
        add_right,
        html,
        flags=re.IGNORECASE | re.VERBOSE,
    )

    # template tag breaks

    def should_i_move_template_tag(out_format: str, match: re.Match) -> str:
        # ensure template tag is not inside an html tag

        if _should_ignore(config, html, match):
            return match.group(1)

        if not re.findall(
            r"\<(?:"
            + str(config.break_html_tags)
            + r")[ ][^>]*?"
            + re.escape(match.group(1))
            + "$",
            html[: match.end()],
            re.MULTILINE | re.VERBOSE,
        ):

            return out_format % match.group(1)

        return match.group(1)

    # template tags
    # break before
    html = re.sub(
        break_char
        + r"\K((?:{%|{{\#)[ ]*?(?:"
        + re.sub(r"\s", "", config.break_template_tags)
        + ")[^}]+?[%|}]})",
        partial(should_i_move_template_tag, "\n%s"),
        html,
        re.IGNORECASE | re.MULTILINE,
    )

    # break after
    html = re.sub(
        r"((?:{%|{{\#)[ ]*?(?:"
        + re.sub(r"\s", "", config.break_template_tags)
        + ")[^}]+?[%|}]})(?=[^\n])",
        partial(should_i_move_template_tag, "%s\n"),
        html,
        re.IGNORECASE | re.MULTILINE,
    )

    return html
