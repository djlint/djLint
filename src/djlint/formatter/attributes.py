"""Format attributes."""

from functools import partial

import regex as re

from ..settings import Config


def format_template_tags(config: Config, attributes: str) -> str:
    """Format template tags in attributes."""
    # find break tags, add breaks + indent
    # find unindent lines and move back
    # put short stuff back on one line

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

        leading_space = len(attr_name.group()) * " "

        indent = ""

        if re.match(
            re.compile(config.tag_indent, re.I | re.X), match.group()
        ) or re.match(re.compile(config.tag_unindent_line, re.I | re.X), match.group()):
            # if an indent tag, then add leading space
            indent = config.indent
        if pattern == "before":
            # but don't add break if we are the first thing in an attribute.
            if attr_name.end() == match.start():
                return match.group()
            return f"\n{leading_space}{match.group()}"

        # else "after"
        # but don't add a break if the next char closes the attr.
        if re.match(r"\s*?[\"|'|>]", match.group(2)):
            return match.group(1) + match.group(2)

        return f"{match.group(1)}\n{leading_space}{indent}{match.group(2).strip()}"

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

    # format template tags
    attributes = format_template_tags(config, attributes)

    # clean trailing spaces added by breaks
    attributes = "\n".join([x.rstrip() for x in attributes.splitlines()])

    return f"{attributes}"
