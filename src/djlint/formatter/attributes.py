"""Format attributes."""

import regex as re

from ..settings import Config


def format_attributes(config: Config, match: re.match) -> str:
    """Spread long attributes over multiple lines."""
    leading_space = match.group(1)

    tag = match.group(2)

    spacing = "\n" + leading_space + len(tag) * " "

    attributes = (spacing).join(
        re.findall(config.attribute_pattern, match.group(3).strip(), re.VERBOSE)
    )

    close = match.group(4)

    return f"{leading_space}{tag}{attributes}{close}"
