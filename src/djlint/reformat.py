"""Djlint reformat html files.

Much code is borrowed from https://github.com/rareyman/HTMLBeautify, many thanks!
"""

import difflib
import re
from pathlib import Path

from djlint.settings import (
    attribute_pattern,
    format_long_attributes,
    ignored_tag_closing,
    ignored_tag_opening,
    indent,
    max_line_length,
    reduce_extralines_gt,
    tag_indent,
    tag_newline_after,
    tag_newline_before,
    tag_pattern,
    tag_pos_inline,
    tag_raw_flat_closing,
    tag_raw_flat_opening,
    tag_unindent,
    tag_unindent_line,
)


def clean_line(line):
    """Clean up a line of html.

    * remove duplicate spaces
    * remove trailing spaces

    """
    return re.sub(r" {2,}", " ", line.strip())


def flatten_attributes(match):
    """Flatten multiline attributes back to one line."""
    return "{} {}{}".format(
        match.group(1),
        " ".join(match.group(2).strip().splitlines()),
        match.group(3),
    )


def format_attributes(match):
    """Spread long attributes over multiple lines."""
    leading_space = match.group(1)

    tag = match.group(2)

    attributes = "{}{}".format(
        ("\n" + leading_space + indent),
        ("\n" + leading_space + indent).join(
            re.findall(attribute_pattern, match.group(3).strip())
        ),
    )

    close = match.group(4)

    return "{}{}{}{}".format(
        leading_space,
        tag,
        attributes,
        close,
    )


def add_newlines(match):
    """Only add newlines of the match is not in our acceptable one line pattern."""
    g_one = match.group(1)
    g_two = match.group(2)

    if not re.search(tag_pos_inline, g_one + g_two, flags=re.IGNORECASE | re.MULTILINE):
        return g_one + "\n" + g_two

    return g_one + g_two


def remove_indentation(rawcode):
    """Remove indentation from raw code."""
    rawcode_flat = ""
    is_block_ignored = False
    is_block_raw = False

    for item in rawcode.strip().splitlines():

        # ignore raw code
        if re.search(tag_raw_flat_closing, item, re.IGNORECASE):
            is_block_raw = False

        elif re.search(tag_raw_flat_opening, item, re.IGNORECASE):
            is_block_raw = True

        # find ignored blocks and retain indentation, otherwise strip white space
        if re.search(ignored_tag_closing, item, re.IGNORECASE):
            tmp = clean_line(item)
            is_block_ignored = False

        elif re.search(ignored_tag_opening, item, re.IGNORECASE):
            tmp = clean_line(item)
            is_block_ignored = True

        # not filtered so just output it
        elif is_block_raw:
            # remove tabs from raw_flat content
            tmp = re.sub(indent, "", item)

        elif is_block_ignored:
            tmp = item

        else:
            tmp = clean_line(item)  # item.strip()

            # add missing line breaks before tag
            tmp = re.sub(
                tag_newline_before,
                add_newlines,
                tmp,
                flags=re.IGNORECASE | re.MULTILINE,
            )

            # add missing line breaks after tag
            tmp = re.sub(
                tag_newline_after, add_newlines, tmp, flags=re.IGNORECASE | re.MULTILINE
            )

        rawcode_flat = rawcode_flat + tmp + "\n"

    # put attributes back on one line
    rawcode_flat = re.sub(
        tag_pattern,
        flatten_attributes,
        rawcode_flat,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )

    # put empty tags on one line
    rawcode_flat = re.sub(
        r"(<([\w]+)[^>]*>)\n(<\/\2>)",
        r"\1\3",
        rawcode_flat,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    return rawcode_flat


def add_indentation(rawcode):
    """Indent raw code."""
    rawcode_flat_list = re.split("\n", rawcode)

    beautified_code = ""
    indent_level = 0
    is_block_raw = False
    blank_counter = 0

    for item in rawcode_flat_list:

        # if a raw tag then start ignoring
        if (
            tag_raw_flat_closing
            and re.search(tag_raw_flat_closing, item, re.IGNORECASE)
        ) or re.search(ignored_tag_closing, item, re.IGNORECASE):
            is_block_raw = False

        # if a one-line, inline tag, just process it
        if re.search(tag_pos_inline, item, re.IGNORECASE) and is_block_raw is False:
            tmp = (indent * indent_level) + item
            blank_counter = 0

        # if unindent, move left
        elif re.search(tag_unindent, item, re.IGNORECASE) and is_block_raw is False:
            indent_level = indent_level - 1
            tmp = (indent * indent_level) + item
            blank_counter = 0

        elif (
            re.search(tag_unindent_line, item, re.IGNORECASE) and is_block_raw is False
        ):
            tmp = (indent * (indent_level - 1)) + item
            blank_counter = 0

        # if indent, move right
        elif re.search(tag_indent, item, re.IGNORECASE) and is_block_raw is False:
            tmp = (indent * indent_level) + item
            indent_level = indent_level + 1
            blank_counter = 0

        elif is_block_raw is True:
            tmp = item

        # if just a blank line
        elif item.strip() == "" and (
            blank_counter < int(reduce_extralines_gt) or blank_counter + 1
        ):
            tmp = item.strip()

        # otherwise, just leave same level
        else:
            tmp = (indent * indent_level) + item

        # if not raw, we can try to fix django tags
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
            tmp = re.sub(r"(\s*?)(<\w+)(\s[^>]+?)(/?>)", format_attributes, tmp)

        # turn off raw block if we hit end - for one line raw blocks
        if (
            tag_raw_flat_closing
            and re.search(tag_raw_flat_closing, item, re.IGNORECASE)
        ) or re.search(ignored_tag_closing, item, re.IGNORECASE):
            is_block_raw = False

        beautified_code = beautified_code + tmp + "\n"

    return beautified_code.strip() + "\n"


def reformat_file(check: bool, this_file: Path):
    """Reformat html file."""
    rawcode = this_file.read_text(encoding="utf8")

    beautified_code = add_indentation(remove_indentation(rawcode))

    if check is not True:
        # update the file
        this_file.write_text(beautified_code)

    out = {
        this_file: list(
            difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
        )
    }
    return out
