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


def remove_indentation(rawcode):
    """Remove indentation from raw code."""
    rawcode_flat = ""
    is_block_ignored = False
    is_block_raw = False

    for item in rawcode.strip().splitlines():

        # ignore raw code
        if re.search(tag_raw_flat_closing, item, re.IGNORECASE):
            tmp = clean_line(item)
            is_block_raw = False

        elif re.search(tag_raw_flat_opening, item, re.IGNORECASE):
            tmp = clean_line(item)
            is_block_raw = True

        # find ignored blocks and retain indentation, otherwise strip white space
        if re.search(ignored_tag_closing, item, re.IGNORECASE):
            tmp = clean_line(item)
            is_block_ignored = False

        elif re.search(ignored_tag_opening, item, re.IGNORECASE):
            tmp = item
            is_block_ignored = True

        # not filtered so just output it
        elif is_block_raw:
            # remove tabs from raw_flat content
            tmp = re.sub(indent, "", item)

        elif is_block_ignored:
            tmp = item

        else:
            tmp = item.strip()

        rawcode_flat = rawcode_flat + tmp + "\n"

    # put attributes back on one line
    rawcode_flat = re.sub(
        tag_pattern,
        flatten_attributes,
        rawcode_flat,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )

    # add missing line breaks before tag
    rawcode_flat = re.sub(
        tag_newline_before,
        r"\1\n\2",
        rawcode_flat,
        flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
    )

    # add missing line breaks after tag
    rawcode_flat = re.sub(
        tag_newline_after, r"\1\n\2", rawcode_flat, flags=re.IGNORECASE | re.MULTILINE
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

        # if a one-line, inline tag, just process it
        if re.search(tag_pos_inline, item, re.IGNORECASE):
            tmp = (indent * indent_level) + item
            blank_counter = 0

        # if unindent, move left
        elif re.search(tag_unindent, item, re.IGNORECASE):
            indent_level = indent_level - 1
            tmp = (indent * indent_level) + item
            blank_counter = 0

        elif re.search(tag_unindent_line, item, re.IGNORECASE):
            tmp = (indent * (indent_level - 1)) + item
            blank_counter = 0

        # if indent, move right
        elif re.search(tag_indent, item, re.IGNORECASE):
            tmp = (indent * indent_level) + item
            indent_level = indent_level + 1
            blank_counter = 0

        # if raw, flatten! no indenting!
        elif tag_raw_flat_opening and re.search(
            tag_raw_flat_opening, item, re.IGNORECASE
        ):
            tmp = item
            is_block_raw = True
            blank_counter = 0

        elif tag_raw_flat_closing and re.search(
            tag_raw_flat_closing, item, re.IGNORECASE
        ):
            tmp = item
            is_block_raw = False
            blank_counter = 0

        elif is_block_raw is True:
            tmp = item

        # if just a blank line
        elif item.strip() == "":
            if blank_counter < int(reduce_extralines_gt) or blank_counter + 1:
                tmp = item.strip()

        # otherwise, just leave same level
        else:
            tmp = item  # (indent * indent_level) + item

        beautified_code = beautified_code + tmp + "\n"

    if format_long_attributes:
        # find lines longer than x
        new_beautified = ""
        for line in beautified_code.splitlines():
            if len(line) > max_line_length:
                # get leading space, and attributes
                line = re.sub(r"(\s*?)(<\w+)(.+?)(/?>)", format_attributes, line)

            new_beautified += "\n" + line
        beautified_code = new_beautified

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
