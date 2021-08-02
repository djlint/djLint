"""djLint Attempt to logically shrink html."""
import re as old_re

import regex as re

from ..settings import (
    ignored_inline_blocks,
    ignored_tag_closing,
    ignored_tag_opening,
    single_line_html_tags,
    single_line_template_tags,
    start_template_tags,
    tag_raw_flat_closing,
    tag_raw_flat_opening,
)


def _clean_line(line):
    """Clean up a line of html.

    * remove duplicate spaces
    * remove trailing spaces

    """
    return re.sub(r" {2,}", " ", line.strip())


def _strip_html_whitespace(html):
    """Remove unnecessary whitespace from text."""
    rawcode_flat = ""
    is_block_ignored = False
    is_block_raw = False

    for item in html.strip().splitlines():

        # start of ignored block
        is_block_raw = bool(re.search(tag_raw_flat_opening, item, re.IGNORECASE))

        # find ignored blocks and retain indentation, otherwise strip white space
        if re.findall(
            r"(?:%s)" % "|".join(ignored_inline_blocks), item, flags=re.IGNORECASE
        ):
            tmp = _clean_line(item)

        elif (
            re.search(ignored_tag_closing, item, re.IGNORECASE)
            and is_block_raw is False
        ):
            tmp = _clean_line(item)
            is_block_ignored = False

        elif (
            re.search(ignored_tag_opening, item, re.IGNORECASE)
            and is_block_raw is False
        ):
            tmp = _clean_line(item)
            is_block_ignored = True

        elif is_block_raw or is_block_ignored:
            tmp = item

        else:
            tmp = _clean_line(item)

        # end of ignore raw code
        is_block_raw = not bool(re.search(tag_raw_flat_closing, item, re.IGNORECASE))

        rawcode_flat = rawcode_flat + tmp + "\n"

    return rawcode_flat


def compress_html(html):
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line
    html = _strip_html_whitespace(html)

    html = re.sub(
        r"(<([\w]+)[^>]*>)\s+?(<\/\2>)",
        r"\1\3",
        html,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    # put empty template tags on one line
    html = re.sub(
        r"(" + start_template_tags + r")\s+?(\{\% end[^}]*?\%\})",
        r"\1\2",
        html,
        re.MULTILINE,
    )

    # put short single line tags on one line
    slt_html = "|".join(single_line_html_tags)
    html = old_re.sub(
        r"(<(%s)>)\s*([^<\n]{,80})\s*?(</(\2)>)" % slt_html,
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    html = old_re.sub(
        r"(<(%s)>)\s*?([^<\n]{,80})\s*?(</(\2)>)" % slt_html,
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    html = re.sub(
        r"(<(%s) [^\n]{,40}>)\s*([^<\n]{,50})\s*?(</(\2)>)" % slt_html,
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    slt_template = "|".join(single_line_template_tags)
    html = re.sub(
        r"({% +?("
        + slt_template
        + r") +?[^\n]{,30}%})\s*([^%\n]{,50})\s*?({% +?end(\2) +?%})",
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE,
    )

    return html
