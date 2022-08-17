"""Format attributes."""

from functools import partial

import regex as re

from ..helpers import inside_ignored_block
from ..settings import Config


def format_template_tags(config: Config, attributes: str) -> str:
    """Format template tags in attributes."""
    # find break tags, add breaks + indent
    # find unindent lines and move back
    # put short stuff back on one line
    leading_space = ""

    if re.search(r"^[ ]+", attributes.splitlines()[0], re.MULTILINE):
        leading_space = re.search(
            r"^[ ]+", attributes.splitlines()[0], re.MULTILINE
        ).group()

    def add_indentation(config: Config, attributes: str) -> str:
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
        attr_name = (
            list(
                re.finditer(
                    re.compile(r"^<\w+\b\s*", re.M), attributes.splitlines()[0].strip()
                )
            )
        )[-1]

        start_test_list = list(
            re.finditer(
                re.compile(
                    r"^.*?(?=" + config.template_indent + r")", re.I | re.X | re.M
                ),
                attributes.splitlines()[0].strip(),
            )
        ) + list(
            re.finditer(
                re.compile(r"^<\w+\b\s*[^\"']+?[\"']", re.M),
                attributes.splitlines()[0].strip(),
            )
        )

        start_test = start_test_list[-1] if start_test_list else None

        base_indent = len(attr_name.group())

        indent = 0
        indented = ""
        indent_adder = 0

        # if the "start test" open is actually closed, then ignore the indent.
        if not re.findall(
            re.compile(r"[\"']$", re.M), attributes.splitlines()[0].strip()
        ):
            indent_adder = len(start_test.group()) - base_indent if start_test else 0

        for line_number, line in enumerate(attributes.splitlines()):
            # when checking for template tag, use "match" to force start of line check.
            if re.match(
                re.compile(config.template_unindent, re.I | re.X), line.strip()
            ):

                indent = indent - 1
                tmp = (indent * config.indent) + (indent_adder * " ") + line.strip()

                # if we are leaving an indented group, then remove the indent_adder
            elif re.match(
                re.compile(config.tag_unindent_line, re.I | re.X), line.strip()
            ):
                tmp = (
                    max(indent - 1, 0) * config.indent
                    + indent_adder * " "
                    + line.strip()
                )

            # for open tags, search, but then check that they are not closed.
            elif re.search(
                re.compile(config.template_indent, re.I | re.X), line.strip()
            ) and not re.search(
                re.compile(config.template_unindent, re.I | re.X), line.strip()
            ):
                tmp = (indent * config.indent) + (indent_adder * " ") + line.strip()
                indent = indent + 1

            else:
                tmp = (indent * config.indent) + (indent_adder * " ") + line.strip()

            if line_number == 0:
                # don't touch first line
                indented += f"{leading_space}{line.strip()}"
            else:
                # if changing indent level and not the first item on the line, then
                # check if base indent is changed.
                # match must start at first of string
                start_test = list(
                    re.finditer(re.compile(r"^(\w+?=[\"'])", re.M), line.strip())
                ) + list(
                    re.finditer(
                        re.compile(
                            r"^(.+?)" + config.template_indent, re.I | re.X | re.M
                        ),
                        line.strip(),
                    )
                )

                if start_test:
                    indent_adder = len(start_test[-1].group(1)) - (
                        base_indent if line_number == 0 else 0
                    )

                base_indent_space = base_indent * " "

                if tmp.strip() != "":
                    indented += f"\n{leading_space}{base_indent_space}{tmp}"

            end_text = re.findall(re.compile(r"[\"']$", re.M), line.strip())

            if end_text:
                indent_adder = 0

        return indented

    def add_break(
        config: Config, attributes: str, pattern: str, match: re.Match
    ) -> str:
        """Make a decision if a break should be added."""
        # check if we are inside an attribute.
        inside_attribute = any(
            x.start() <= match.start() and match.end() <= x.end()
            for x in re.finditer(
                re.compile(
                    r"[a-zA-Z-_]+[ ]*?=[ ]*?([\"'])([^\1]*?"
                    + config.template_if_for_pattern
                    + r"[^\1]*?)\1",
                    re.I | re.M | re.X | re.DOTALL,
                ),
                attributes,
            )
        )

        if inside_attribute:
            attr_name = list(
                re.finditer(
                    re.compile(r"^.+?\w+[ ]*?=[ ]*?[\"|']", re.M),
                    attributes[: match.start()],
                )
            )[-1]
        else:
            # if we don't know where we are, then return what we started with.
            if not re.findall(
                re.compile(r"^<\w+[^=\"']\s*", re.M), attributes[: match.start()]
            ):
                return match.group()

            attr_name = list(
                re.finditer(
                    re.compile(r"^<\w+[^=\"']\s*", re.M), attributes[: match.start()]
                )
            )[-1]

        if pattern == "before":
            # but don't add break if we are the first thing in an attribute.
            if attr_name.end() == match.start():
                return match.group()

            return f"\n{match.group()}"

        # but don't add a break if the next char closes the attr.
        if re.match(r"\s*?[\"|'|>]", match.group(2)):
            return match.group(1) + match.group(2)

        return f"{match.group(1)}\n{match.group(2).strip()}"

    break_char = config.break_before

    func = partial(add_break, config, attributes, "before")
    attributes = re.sub(
        re.compile(
            break_char
            + r"\K((?:{%|{{\#)[ ]*?(?:"
            + config.break_template_tags
            + ")[^}]+?[%|}]})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        func,
        attributes,
    )

    func = partial(add_break, config, attributes, "after")
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

    attributes = add_indentation(config, attributes)

    return attributes


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


def format_attributes(config: Config, html: str, match: re.match) -> str:
    """Spread long attributes over multiple lines."""
    # check that we are not inside an ignored block
    if (
        inside_ignored_block(config, html, match)
        or len(match.group(3).strip()) < config.max_attribute_length
    ):
        return match.group()

    leading_space = match.group(1)

    tag = match.group(2) + " "

    spacing = "\n" + leading_space + len(tag) * " "

    # format attributes as groups
    attributes = (spacing).join(
        re.findall(config.attribute_pattern, match.group(3).strip(), re.VERBOSE)
    )

    close = match.group(4)

    attributes = f"{leading_space}{tag}{attributes}{close}"

    # format template tags
    if config.format_attribute_template_tags:
        attributes = format_template_tags(config, attributes)

    # format styles
    func = partial(format_style)
    attributes = re.sub(
        re.compile(
            config.attribute_style_pattern,
            re.VERBOSE | re.IGNORECASE | re.M,
        ),
        func,
        attributes,
    )

    # clean trailing spaces added by breaks
    attributes = "\n".join([x.rstrip() for x in attributes.splitlines()])

    return f"{attributes}"
