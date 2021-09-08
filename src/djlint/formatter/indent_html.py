"""djLint add indentation to html."""

from functools import partial

import regex as re

from ..settings import Config


def _format_attributes(config: Config, match: re.match) -> str:
    """Spread long attributes over multiple lines."""
    leading_space = match.group(1)

    tag = match.group(2)

    spacing = "\n" + leading_space + len(tag) * " "

    attributes = (spacing).join(
        re.findall(str(config.attribute_pattern), match.group(3).strip(), re.VERBOSE)
    )

    close = match.group(4)

    return "{}{}{}{}".format(
        leading_space,
        tag,
        attributes,
        close,
    )


def indent_html(rawcode: str, config: Config) -> str:
    """Indent raw code."""
    rawcode_flat_list = re.split("\n", rawcode)

    indent = config.indent

    beautified_code = ""
    indent_level = 0
    is_block_raw = False

    slt_html = config.break_html_tags

    # here using all tags cause we allow empty tags on one line
    always_slt_html = config.always_single_line_html_tags

    # here using all tags cause we allow empty tags on one line
    slt_template = config.single_line_template_tags

    for item in rawcode_flat_list:
        # if a raw tag then start ignoring
        if re.search(config.ignored_group_opening, item, re.IGNORECASE | re.VERBOSE):
            is_block_raw = True

        if re.findall(
            config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
        ):
            tmp = (indent * indent_level) + item + "\n"

        # if a one-line, inline tag, just process it, only if line starts w/ it
        elif (
            re.findall(
                r"(<(%s)>)(.*?)(</(\2)>)" % slt_html, item, re.IGNORECASE | re.VERBOSE
            )
            or re.findall(
                r"(<(%s)[ ].+?>)(.*?)(</(\2)>)" % slt_html,
                item,
                re.IGNORECASE | re.VERBOSE,
            )
            or re.findall(
                r"^({%[ ]*?("
                + str(slt_template)
                + r")[ ]+?.+?%})(.*?)({%[ ]+?end(\2)[ ]+?.*?%})",
                item,
                re.IGNORECASE | re.MULTILINE | re.VERBOSE,
            )
            or re.findall(
                r"(<(%s)[ ].*?/>)" % slt_html, item, flags=re.IGNORECASE | re.VERBOSE
            )
            or re.findall(
                r"(<(%s)[ ].*?/?>)" % always_slt_html,
                item,
                flags=re.IGNORECASE | re.VERBOSE,
            )
        ) and is_block_raw is False:
            tmp = (indent * indent_level) + item + "\n"

        # if unindent, move left
        elif (
            re.search(
                config.tag_unindent,
                item,
                re.IGNORECASE | re.MULTILINE | re.VERBOSE,
            )
            and is_block_raw is False
            or re.search(config.ignored_block_closing, item, re.IGNORECASE | re.VERBOSE)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + item + "\n"

        elif (
            re.search(
                r"^" + str(config.tag_unindent_line),
                item,
                re.IGNORECASE | re.MULTILINE | re.VERBOSE,
            )
            and is_block_raw is False
        ):
            tmp = (indent * (indent_level - 1)) + item + "\n"

        # if indent, move right
        elif (
            re.search(
                r"^(?:" + str(config.tag_indent) + r")",
                item,
                re.IGNORECASE | re.MULTILINE | re.VERBOSE,
            )
            and is_block_raw is False
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level = indent_level + 1

        elif is_block_raw is True:
            tmp = item + "\n"

        # if just a blank line
        elif item.strip() == "":
            tmp = item.strip()

        # otherwise, just leave same level
        else:
            tmp = (indent * indent_level) + item + "\n"

        # we can try to fix template tags
        tmp = re.sub(r"({[{|%]\-?)(\w[^}].+?)([}|%]})", r"\1 \2\3", tmp)
        tmp = re.sub(r"({[{|%])([^}].+?[^(?:\ |\-)])([}|%]})", r"\1\2 \3", tmp)
        tmp = re.sub(r"({[{|%])([^}].+?[^ ])(\-[}|%]})", r"\1\2 \3", tmp)

        # handlebars templates
        tmp = re.sub(r"({{#(?:each|if).+?[^ ])(}})", r"\1 \2", tmp)

        # if a opening raw tag then start ignoring.. only if there is no closing tag
        # on the same line
        if (
            re.search(config.ignored_group_opening, item, re.IGNORECASE | re.VERBOSE)
        ) or re.search(config.ignored_block_opening, item, re.IGNORECASE | re.VERBOSE):
            is_block_raw = True

        # if a normal tag, we can try to expand attributes
        elif (
            config.format_long_attributes
            and is_block_raw is False
            and len(tmp) > int(config.max_line_length)
        ):
            # get leading space, and attributes
            func = partial(_format_attributes, config)
            tmp = re.sub(r"(\s*?)(<\w+\s)([^>]+?)(/?>)", func, tmp)

        # turn off raw block if we hit end - for one line raw blocks
        if (
            re.search(
                re.sub(r"\s", "", config.ignored_group_closing), item, re.IGNORECASE
            )
        ) or re.search(
            re.sub(r"\s", "", config.ignored_block_closing), item, re.IGNORECASE
        ):

            is_block_raw = False

        beautified_code = beautified_code + tmp

    return beautified_code.strip() + "\n"
