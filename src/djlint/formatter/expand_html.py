"""djLint expand out html code."""
from functools import partial

import regex as re

from ..settings import Config


def _flatten_attributes(match: re.Match) -> str:
    """Flatten multiline attributes back to one line.

    Skip when attribute is ignored.
    Attribute name can be in group one or group 2.
    for now, skipping if they are anywhere
    """
    # pylint: disable=C0209
    return "{} {}{}".format(
        match.group(1),
        " ".join(x.strip() for x in match.group(2).strip().splitlines()),
        match.group(3),
    )


def _should_ignore(config: Config, html: str, match: re.Match) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        ignored_match.start() < match.start(1) and ignored_match.end() > match.end(1)
        for ignored_match in re.finditer(
            config.ignored_blocks,
            html,
            re.DOTALL | re.IGNORECASE | re.VERBOSE,
        )
    )


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
    html = re.sub(
        re.compile(config.tag_pattern, flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE),
        _flatten_attributes,
        html,
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
        re.compile(
            fr"{break_char}\K(<(?:{html_tags})>)", flags=re.IGNORECASE | re.VERBOSE
        ),
        add_left,
        html,
    )

    # <tag>
    html = re.sub(
        re.compile(fr"(<(?:{html_tags})>)(?=[^\n])", flags=re.IGNORECASE | re.VERBOSE),
        add_right,
        html,
    )

    # \n<tag /> and \n<tag/>
    html = re.sub(
        re.compile(
            fr"{break_char}\K(<(?:{html_tags})[ ]?/>)", flags=re.IGNORECASE | re.VERBOSE
        ),
        add_left,
        html,
    )

    # <tag /> and <tag/>
    html = re.sub(
        re.compile(
            fr"(<(?:{html_tags})[ ]?/>)(?=[^\n])", flags=re.IGNORECASE | re.VERBOSE
        ),
        add_right,
        html,
    )

    # \n<tag attributes/>,  \n<tag attributes>, \n<tag attributes />
    html = re.sub(
        re.compile(
            fr"{break_char}\K(<(?:{html_tags})[ ]+?("
            + config.attribute_pattern
            + r")\s*?>)",
            flags=re.IGNORECASE | re.VERBOSE,
        ),
        add_left,
        html,
    )

    # <tag attributes/>,  <tag attributes>, <tag attributes />
    html = re.sub(
        re.compile(
            fr"(<(?:{html_tags})[ ]+?("
            + config.attribute_pattern
            + r")\s*?>)(?=[^\n])",
            flags=re.IGNORECASE | re.VERBOSE,
        ),
        add_right,
        html,
    )

    html = re.sub(
        re.compile(
            fr"{break_char}\K(<(?:{html_tags})[ ][^>]+?/>)",
            flags=re.IGNORECASE | re.VERBOSE,
        ),
        add_left,
        html,
    )

    html = re.sub(
        re.compile(
            fr"(<(?:{html_tags})[ ][^>]+?/>)(?=[^\n])", flags=re.IGNORECASE | re.VERBOSE
        ),
        add_right,
        html,
    )

    # process closing (break_char, html_tags,)s ######

    html = re.sub(
        re.compile(
            fr"{break_char}\K(</(?:{html_tags})>)", flags=re.IGNORECASE | re.VERBOSE
        ),
        add_left,
        html,
    )
    html = re.sub(
        re.compile(fr"(</(?:{html_tags})>)(?=[^\n])", flags=re.IGNORECASE | re.VERBOSE),
        add_right,
        html,
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
        re.compile(
            break_char
            + r"\K((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        partial(should_i_move_template_tag, "\n%s"),
        html,
    )

    # break after
    html = re.sub(
        re.compile(
            r"((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})(?=[^\n])",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        partial(should_i_move_template_tag, "%s\n"),
        html,
    )

    return html
