"""djLint add indentation to html."""

from functools import partial

import regex as re

from ..helpers import (
    is_ignored_block_closing,
    is_ignored_block_opening,
    is_safe_closing_tag,
)
from ..settings import Config
from .attributes import format_attributes


def indent_html(rawcode: str, config: Config) -> str:
    """Indent raw code."""
    rawcode_flat_list = re.split("\n", rawcode)

    indent = config.indent

    beautified_code = ""
    indent_level = 0
    is_raw_first_line = False
    is_block_raw = False

    slt_html = config.indent_html_tags

    # here using all tags cause we allow empty tags on one line
    always_self_closing_html = config.always_self_closing_html_tags

    # here using all tags cause we allow empty tags on one line
    slt_template = config.optional_single_line_template_tags

    for item in rawcode_flat_list:
        # if a raw tag first line
        if not is_block_raw and is_ignored_block_opening(config, item):
            is_raw_first_line = True

        # if a raw tag then start ignoring
        if is_ignored_block_opening(config, item):
            is_block_raw = True

        if re.findall(
            config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
        ):
            tmp = (indent * indent_level) + item + "\n"

        # if a one-line, inline tag, just process it, only if line starts w/ it
        elif (
            re.findall(
                fr"(<({slt_html})>)(.*?)(</(\2)>)", item, re.IGNORECASE | re.VERBOSE
            )
            or re.findall(
                re.compile(
                    fr"(<({slt_html})\b.+?>)(.*?)(</(\2)>)", re.IGNORECASE | re.VERBOSE
                ),
                item,
            )
            or re.findall(
                fr"^({{%[ ]*?({slt_template})[ ]+?.+?%}})(.*?)({{%[ ]+?end(\2)[ ]+?.*?%}})",
                item,
                re.IGNORECASE | re.MULTILINE | re.VERBOSE,
            )
            or re.findall(
                fr"(<({slt_html})\b.*?/>)", item, flags=re.IGNORECASE | re.VERBOSE
            )
            or re.findall(
                re.compile(
                    fr"(<({always_self_closing_html})\b.*?/?>)",
                    re.IGNORECASE | re.VERBOSE,
                ),
                item,
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
                re.compile(
                    r"^(?:" + str(config.tag_indent) + r")",
                    re.IGNORECASE | re.MULTILINE | re.VERBOSE,
                ),
                item,
            )
            and is_block_raw is False
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level = indent_level + 1

        elif is_raw_first_line is True or is_safe_closing_tag(config, item):
            tmp = (indent * indent_level) + item + "\n"

        elif is_block_raw is True or item.strip() == "":

            tmp = item + "\n"

        # otherwise, just leave same level
        else:
            tmp = (indent * indent_level) + item + "\n"

        # we can try to fix template tags. ignore handlebars
        if config.profile not in ["handlebars", "golang"]:
            tmp = re.sub(r"({[{|%]\-?)(\w[^}].+?)([}|%]})", r"\1 \2\3", tmp)
            tmp = re.sub(r"({[{|%])([^}].+?[^(?:\ |\-)])([}|%]})", r"\1\2 \3", tmp)
            tmp = re.sub(r"({[{|%])([^}].+?[^ -])(\-+?[}|%]})", r"\1\2 \3", tmp)

        elif config.profile == "handlebars":
            # handlebars templates
            tmp = re.sub(r"({{#(?:each|if).+?[^ ])(}})", r"\1 \2", tmp)

        # if a opening raw tag then start ignoring.. only if there is no closing tag
        # on the same line

        if is_ignored_block_opening(config, item):
            is_block_raw = True
            is_raw_first_line = False

        # if a normal tag, we can try to expand attributes
        elif is_block_raw is False:
            # get leading space, and attributes
            func = partial(format_attributes, config, item)

            tmp = re.sub(
                re.compile(
                    fr"(\s*?)(<(?:{config.indent_html_tags})\b)((?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])+?)(/?>)",
                    re.VERBOSE | re.IGNORECASE,
                ),
                func,
                tmp,
            )

        # turn off raw block if we hit end - for one line raw blocks, but not an inline raw
        if is_ignored_block_closing(config, item):
            is_block_raw = False

        beautified_code = beautified_code + tmp

    return beautified_code.strip() + "\n"
