"""Format attributes."""

from functools import partial

import regex as re

from ..settings import Config


def format_style(match: re.match) -> str:
    """Format inline styles."""
    tag = match.group(2)

    quote = match.group(3)

    # if the style attrib is following the tag name
    leading_stuff = (
        match.group(1)
        if not bool(re.match(r"^\s+$", match.group(1), re.MULTILINE))
        else len(match.group(1)) * " "
    )

    spacing = "\n" + len(match.group(1)) * " " + len(tag) * " " + len(quote) * " "

    styles = (spacing).join(
        [x.strip() + ";" for x in match.group(4).split(";") if x.strip()]
    )

    return f"{leading_stuff}{tag}{quote}{styles}{quote}"


def format_attributes(config: Config, match: re.match) -> str:
    """Spread long attributes over multiple lines."""
    leading_space = match.group(1)

    tag = match.group(2)

    spacing = "\n" + leading_space + len(tag) * " "

    # format attributes as groups
    attributes = (spacing).join(
        re.findall(config.attribute_pattern, match.group(3).strip(), re.VERBOSE)
    )

    close = match.group(4)

    attributes = f"{leading_space}{tag}{attributes}{close}"

    # format styles
    func = partial(format_style)
    attributes = re.sub(
        re.compile(
            config.attribute_style_pattern,
            re.VERBOSE | re.IGNORECASE,
        ),
        func,
        attributes,
    )

    return f"{attributes}"
