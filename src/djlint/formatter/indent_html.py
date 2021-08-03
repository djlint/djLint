"""djLint add indentation to html."""
import regex as re

from ..settings import (
    always_single_line_html_tags,
    attribute_pattern,
    break_html_tags,
    format_long_attributes,
    ignored_inline_blocks,
    ignored_tag_closing,
    ignored_tag_opening,
    indent,
    max_line_length,
    reduce_extralines_gt,
    single_line_template_tags,
    tag_indent,
    tag_raw_flat_closing,
    tag_raw_flat_opening,
    tag_unindent,
    tag_unindent_line,
)


def _format_attributes(match):
    """Spread long attributes over multiple lines."""
    leading_space = match.group(1)

    tag = match.group(2)

    spacing = "\n" + leading_space + len(tag) * " "

    attributes = (spacing).join(re.findall(attribute_pattern, match.group(3).strip()))

    close = match.group(4)

    return "{}{}{}{}".format(
        leading_space,
        tag,
        attributes,
        close,
    )


def indent_html(rawcode):
    """Indent raw code."""
    rawcode_flat_list = re.split("\n", rawcode)

    beautified_code = ""
    indent_level = 0
    is_block_raw = False
    blank_counter = 0

    slt_html = "|".join(
        break_html_tags
    )  # here using all tags cause we allow empty tags on one line

    always_slt_html = "|".join(
        always_single_line_html_tags
    )  # here using all tags cause we allow empty tags on one line

    slt_template = "|".join(single_line_template_tags)

    for item in rawcode_flat_list:
        # if a raw tag then start ignoring
        if (
            tag_raw_flat_opening
            and re.search(tag_raw_flat_opening, item, re.IGNORECASE)
        ) or re.search(tag_raw_flat_opening, item, re.IGNORECASE):
            is_block_raw = True

        if re.findall(
            r"(?:%s)" % "|".join(ignored_inline_blocks), item, flags=re.IGNORECASE
        ):
            tmp = (indent * indent_level) + item + "\n"

        # if a one-line, inline tag, just process it, only if line starts w/ it
        elif (
            re.findall(r"(<(%s)>)(.*?)(</(\2)>)" % slt_html, item, re.IGNORECASE)
            or re.findall(r"(<(%s) .+?>)(.*?)(</(\2)>)" % slt_html, item, re.IGNORECASE)
            or re.findall(
                r"^({% +?(" + slt_template + r") +?.+?%})(.*?)({% +?end(\2) +?.*?%})",
                item,
                re.IGNORECASE | re.MULTILINE,
            )
            or re.findall(r"(<(%s) .*?/>)" % slt_html, item, flags=re.IGNORECASE)
            or re.findall(
                r"(<(%s) .*?/?>)" % always_slt_html, item, flags=re.IGNORECASE
            )
        ) and is_block_raw is False:
            tmp = (indent * indent_level) + item + "\n"
            blank_counter = 0

        # if unindent, move left
        elif (
            re.search(r"^(?:" + tag_unindent + r")", item, re.IGNORECASE | re.MULTILINE)
            and is_block_raw is False
            or re.search(ignored_tag_closing, item, re.IGNORECASE)
        ):
            indent_level = max(indent_level - 1, 0)
            tmp = (indent * indent_level) + item + "\n"
            blank_counter = 0

        elif (
            re.search(r"^" + tag_unindent_line, item, re.IGNORECASE | re.MULTILINE)
            and is_block_raw is False
        ):
            tmp = (indent * (indent_level - 1)) + item + "\n"
            blank_counter = 0

        # if indent, move right
        elif (
            re.search(r"^(?:" + tag_indent + r")", item, re.IGNORECASE | re.MULTILINE)
            and is_block_raw is False
        ):
            tmp = (indent * indent_level) + item + "\n"
            indent_level = indent_level + 1
            blank_counter = 0

        elif is_block_raw is True:
            tmp = item + "\n"

        # if just a blank line
        elif item.strip() == "" and (
            blank_counter < int(reduce_extralines_gt) or blank_counter + 1
        ):
            tmp = item.strip()

        # otherwise, just leave same level
        else:
            tmp = (indent * indent_level) + item + "\n"

        # we can try to fix django tags
        tmp = re.sub(r"({[{|%])(\w[^}].+?)([}|%]})", r"\1 \2\3", tmp)
        tmp = re.sub(r"({[{|%])([^}].+?[^ ])([}|%]})", r"\1\2 \3", tmp)

        # handlebars templates
        tmp = re.sub(r"({{#(?:each|if).+?[^ ])(}})", r"\1 \2", tmp)

        # if a opening raw tag then start ignoring.. only if there is no closing tag
        # on the same line
        if (
            tag_raw_flat_closing
            and re.search(tag_raw_flat_opening, item, re.IGNORECASE)
        ) or re.search(ignored_tag_opening, item, re.IGNORECASE):
            is_block_raw = True

        # if a normal tag, we can try to expand attributes
        elif (
            format_long_attributes
            and is_block_raw is False
            and len(tmp) > max_line_length
        ):
            # get leading space, and attributes
            tmp = re.sub(r"(\s*?)(<\w+\s)([^>]+?)(/?>)", _format_attributes, tmp)

        # turn off raw block if we hit end - for one line raw blocks
        if (
            tag_raw_flat_closing
            and re.search(tag_raw_flat_closing, item, re.IGNORECASE)
        ) or re.search(ignored_tag_closing, item, re.IGNORECASE):
            is_block_raw = False

        beautified_code = beautified_code + tmp

    return beautified_code.strip() + "\n"
