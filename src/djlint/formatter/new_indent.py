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

    attribute_pattern = (
        r"\b(?:(?:\"[^\"]*\"|'[^']*'|{{(?:(?!}}).)*}}|{%(?:(?!%}).)*%}|[^'\">{}])*)"
    )

    def format_line(config, line):
        print("formatting line!")
        func = partial(format_attributes, config, line)

        return re.sub(
            re.compile(
                fr"(\s*?)(<(?:{config.indent_html_tags})\b)((?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])+?)(/?>)",
                re.VERBOSE | re.IGNORECASE,
            ),
            func,
            line,
        )

    def format_block(config, html, match):
        # if there was a child, indent the lines
        if match.group(3) and not inside_ignored_block(config, html, match):
            child = find_blocks(match.group(3))

            build = []
            ignored = False
            is_raw_first_line = False
            for line in child.splitlines():
                print(line)
                if is_ignored_block_opening(config, line) and ignored == False:
                    ignored = True
                    is_raw_first_line = True

                if (
                    ignored == False
                    or is_raw_first_line == True
                    or is_safe_closing_tag(config, line)
                ):
                    new_line = config.indent + line
                else:
                    new_line = line

                if is_ignored_block_closing(config, line):
                    ignored = False

                if is_raw_first_line == False and is_block_raw == False:
                    # get leading space, and attributes
                    new_line = format_line(config, new_line)

                is_raw_first_line = False

                build.append(new_line)

            return match.group(1) + ("\n").join(build) + "\n" + match.group(4)

        return match.group(1) + format_line(config, match.group(3)) + match.group(4)

    def find_blocks(rawcode):
        func = partial(format_block, config, rawcode)

        re_expresion = re.compile(
            fr"(<({config.format_html_tags}){attribute_pattern}>)((?:(?:<\2{attribute_pattern}>.*?</\2[ ]*?>)?.+?)*?)(</\2[ ]*?>)",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE | re.DOTALL,
        )
        if re.search(re_expresion, rawcode):
            rawcode = re.sub(re_expresion, func, rawcode)
        else:
            rawcode = format_line(config, rawcode)

        return rawcode

    return ("\n").join(
        [x.rstrip() for x in find_blocks(rawcode).strip().splitlines()]
    ) + "\n"
