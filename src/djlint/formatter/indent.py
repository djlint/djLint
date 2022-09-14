"""djLint add indentation to html."""

from functools import partial

import regex as re

from ..helpers import (
    inside_ignored_block,
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

    # nested ignored blocks..
    ignored_level = 0

    for item in rawcode_flat_list:
        # if a raw tag first line
        if not is_block_raw and is_ignored_block_opening(config, item):
            is_raw_first_line = True

        # if a raw tag then start ignoring
        if is_ignored_block_opening(config, item):
            is_block_raw = True
            ignored_level += 1

        if is_safe_closing_tag(config, item):
            ignored_level -= 1
            ignored_level = max(ignored_level, 0)
            if is_block_raw is True and ignored_level == 0:
                is_block_raw = False

        if (
            re.findall(
                config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
            )
            and is_block_raw is False
        ):
            tmp = (indent * indent_level) + item + "\n"

        # if a one-line, inline tag, just process it, only if line starts w/ it
        elif (
            re.findall(
                rf"(^<({slt_html})>)(.*?)(</(\2)>[^<]*?$)",
                item,
                re.IGNORECASE | re.VERBOSE | re.MULTILINE,
            )
            or re.findall(
                re.compile(
                    rf"(<({slt_html})\b.+?>)(.*?)(</(\2)>[^<]*?$)",
                    re.IGNORECASE | re.VERBOSE | re.MULTILINE,
                ),
                item,
            )
            or re.findall(
                rf"^({{%[ ]*?({slt_template})[ ]+?.*?%}})(.*?)({{%[ ]+?end(\2)[ ]+?.*?%}})",
                item,
                re.IGNORECASE | re.MULTILINE | re.VERBOSE,
            )
            or re.findall(
                rf"(<({slt_html})\b.*?/>)", item, flags=re.IGNORECASE | re.VERBOSE
            )
            or re.findall(
                re.compile(
                    rf"(<({always_self_closing_html})\b.*?/?>)",
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
            and not is_safe_closing_tag(config, item)
        ):
            # block to catch inline block followed by a non-break tag
            if (
                len(
                    re.findall(
                        rf"(^<({slt_html})>)(.*?)(</(\2)>)",
                        item,
                        re.IGNORECASE | re.VERBOSE | re.MULTILINE,
                    )
                    or re.findall(
                        re.compile(
                            rf"(^<({slt_html})\b.+?>)(.*?)(</(\2)>)",
                            re.IGNORECASE | re.VERBOSE | re.MULTILINE,
                        ),
                        item,
                    )
                )
                > 0
            ):
                # unindent after instead of before
                tmp = (indent * indent_level) + item + "\n"
                indent_level = max(indent_level - 1, 0)
            else:
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

        elif is_raw_first_line is True or (
            is_safe_closing_tag(config, item) and is_block_raw is False
        ):
            tmp = (indent * indent_level) + item + "\n"

        elif is_block_raw is True or item.strip() == "":
            tmp = item + "\n"

        # otherwise, just leave same level
        else:
            if not config.preserve_leading_space:
                # if we are not trying to preserve indenting
                # on text, the add it now.
                tmp = (indent * indent_level) + item + "\n"
            else:
                tmp = item + "\n"

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
                    rf"(\s*?)(<(?:{config.indent_html_tags})\b)((?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])+?)(/?>)",
                    re.VERBOSE | re.IGNORECASE,
                ),
                func,
                tmp,
            )

        # turn off raw block if we hit end - for one line raw blocks, but not an inline raw
        if is_ignored_block_closing(config, item):
            if not is_safe_closing_tag(config, item):
                ignored_level -= 1
                ignored_level = max(ignored_level, 0)
            if ignored_level == 0:
                is_block_raw = False

        beautified_code = beautified_code + tmp

    # we can try to fix template tags. ignore handlebars
    if config.profile not in ["handlebars", "golang"]:

        def fix_non_handlebars_template_tags(
            html: str, out_format: str, match: re.Match
        ) -> str:

            if inside_ignored_block(config, html, match):
                return match.group()

            return out_format % (
                match.group(1),
                match.group(2),
                match.group(3),
            )

        func = partial(fix_non_handlebars_template_tags, beautified_code, "%s %s%s")
        beautified_code = re.sub(
            r"({[{|%]\-?)(\w[^}].+?)([}|%]})", func, beautified_code
        )

        func = partial(fix_non_handlebars_template_tags, beautified_code, "%s%s %s")
        beautified_code = re.sub(
            r"({[{|%])([^}].+?[^(?:\ |\-)])([}|%]})", func, beautified_code
        )

        func = partial(fix_non_handlebars_template_tags, beautified_code, "%s%s %s")
        beautified_code = re.sub(
            r"({[{|%])([^}].+?[^ -])(\-+?[}|%]})", func, beautified_code
        )

    elif config.profile == "handlebars":

        def fix_handlebars_template_tags(
            html: str, out_format: str, match: re.Match
        ) -> str:

            if inside_ignored_block(config, html, match):
                return match.group()

            return out_format % (
                match.group(1),
                match.group(2),
            )

        func = partial(fix_handlebars_template_tags, beautified_code, "%s %s")
        # handlebars templates
        beautified_code = re.sub(r"({{#(?:each|if).+?[^ ])(}})", func, beautified_code)

    if not config.preserve_blank_lines:
        beautified_code = beautified_code.lstrip()

    return beautified_code.rstrip() + "\n"
