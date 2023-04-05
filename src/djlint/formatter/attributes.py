"""Format attributes."""

from functools import partial

import regex as re

from ..helpers import child_of_ignored_block
from ..settings import Config


def format_template_tags(config: Config, attributes: str, spacing: int) -> str:
    """Format template tags in attributes."""
    # find break tags, add breaks + indent
    # find unindent lines and move back
    # put short stuff back on one line

    def add_indentation(config: Config, attributes: str, spacing: int) -> str:
        """Indent template tags.

        |    <form class="this"
        |    ----- attribute name
        |
        |    <form class="this"
        |---^ leading space
        |
        |    <form class="this"
        |    ^----^ base indent
        |
        """
        indent = 0
        indented = ""
        indent_adder = spacing or 0

        for line_number, line in enumerate(attributes.splitlines()):
            # when checking for template tag, use "match" to force start of line check.
            if re.match(
                re.compile(config.template_unindent, re.I | re.X), line.strip()
            ):
                indent = indent - 1
                tmp = (indent * config.indent) + (indent_adder * " ") + line.strip()

            elif re.match(
                re.compile(config.tag_unindent_line, re.I | re.X), line.strip()
            ):
                # if we are leaving an indented group, then remove the indent_adder
                tmp = (
                    max(indent - 1, 0) * config.indent
                    + indent_adder * " "
                    + line.strip()
                )

            elif re.search(
                re.compile(config.template_indent, re.I | re.X), line.strip()
            ) and not re.search(
                re.compile(config.template_unindent, re.I | re.X), line.strip()
            ):
                # for open tags, search, but then check that they are not closed.
                tmp = (indent * config.indent) + (indent_adder * " ") + line.strip()
                indent = indent + 1

            else:
                tmp = (indent * config.indent) + (indent_adder * " ") + line.strip()

            if line_number == 0:
                # don't touch first line
                indented += line.strip()
            elif tmp.strip():
                indented += f"\n{tmp}"

        return indented

    def add_break(pattern: str, match: re.Match) -> str:
        """Make a decision if a break should be added."""
        if pattern == "before":
            return f"\n{match.group()}"

        return f"{match.group(1)}\n{match.group(2).strip()}"

    break_char = config.break_before

    func = partial(add_break, "before")

    attributes = re.sub(
        re.compile(
            break_char
            + r".\K((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        func,
        attributes,
    )

    func = partial(add_break, "after")
    # break after
    attributes = re.sub(
        re.compile(
            r"((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})([^\n]+)$",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        func,
        attributes,
    )
    attributes = add_indentation(config, attributes, spacing)

    return attributes


def format_attributes(config: Config, html: str, match: re.match) -> str:
    """Spread long attributes over multiple lines."""
    # check that we are not inside an ignored block
    if (
        child_of_ignored_block(config, html, match)
        or len(match.group(3).strip()) < config.max_attribute_length
    ):
        return match.group()

    leading_space = match.group(1)

    tag = match.group(2) + " "

    spacing = leading_space + len(tag) * " "

    attributes = []

    # format attributes as groups
    for attr_grp in re.finditer(
        config.attribute_pattern, match.group(3).strip(), re.VERBOSE
    ):
        attrib_name = attr_grp.group(1)
        is_quoted = attr_grp.group(2) and attr_grp.group(2)[0] in ["'", '"']
        quote = attr_grp.group(2)[0] if is_quoted else '"'

        attrib_value = None

        if attr_grp.group(2) and attr_grp.group(2)[0] == attr_grp.group(2)[-1]:
            if attr_grp.group(2)[0] == "'":
                attrib_value = attr_grp.group(2).strip("'")

            elif attr_grp.group(2)[0] == '"':
                attrib_value = attr_grp.group(2).strip('"')

            else:
                attrib_value = attr_grp.group(2)
        else:
            attrib_value = attr_grp.group(2)

        standalone = attr_grp.group(3)

        quote_length = 1

        if attrib_name and attrib_value:
            # for the equals sign
            quote_length += 1

        if config.format_attribute_template_tags:
            join_space = "\n" + spacing
        else:
            join_space = (
                "\n" + spacing + int(quote_length + len(attrib_name or "")) * " "
            )

        # format style attribute
        if attrib_name and attrib_name.lower() == "style":
            attrib_value = (";" + join_space).join(
                [value.strip() for value in attrib_value.split(";") if value.strip()]
            )

        elif attrib_name and attrib_name.lower() in ["srcset", "data-srcset", "sizes"]:
            # vw
            attrib_value = ("w," + join_space).join(
                [value.strip() for value in attrib_value.split("w,") if value.strip()]
            )
            # px
            attrib_value = ("x," + join_space).join(
                [value.strip() for value in attrib_value.split("x,") if value.strip()]
            )

        # format template stuff
        if config.format_attribute_template_tags:
            if attrib_value and attrib_name not in config.ignored_attributes:
                attrib_value = format_template_tags(
                    config,
                    attrib_value,
                    int(len(spacing) + len(attrib_name or "") + quote_length),
                )

            if standalone:
                standalone = format_template_tags(
                    config, standalone, int(len(spacing) + len(attrib_name or ""))
                )

        if attrib_name and attrib_value or is_quoted:
            attrib_value = attrib_value or ""
            attributes.append(f"{attrib_name}={quote}{attrib_value}{quote}")
        else:
            attributes.append(
                (attrib_name or "") + (attrib_value or "") + (standalone or "")
            )
    attribute_string = ("\n" + spacing).join([x for x in attributes if x])

    close = match.group(4)

    attribute_string = f"{leading_space}{tag}{attribute_string}{close}"

    # clean trailing spaces added by breaks
    attribute_string = "\n".join([x.rstrip() for x in attribute_string.splitlines()])

    return f"{attribute_string}"
