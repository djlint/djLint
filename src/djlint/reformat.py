"""Djlint reformat html files.

Much code is borrowed from https://github.com/rareyman/HTMLBeautify, many thanks!
"""

import difflib
from pathlib import Path

from .formatter.compress_html import compress_html
from .formatter.expand_html import expand_html
from .formatter.indent_html import indent_html


def reformat_file(check: bool, this_file: Path):
    """Reformat html file."""
    rawcode = this_file.read_text(encoding="utf8")

    itteration = 0

    beautified_code = rawcode

    while itteration < 10:

        expanded = expand_html(rawcode)
        compressed = compress_html(expanded)
        indented = indent_html(compressed)

        if (
            len(
                list(
                    difflib.unified_diff(
                        beautified_code.splitlines(), indented.splitlines()
                    )
                )
            )
            == 0
        ):
            beautified_code = indented
            break

        beautified_code = indented

        itteration += 1

    if check is not True:
        # update the file
        this_file.write_text(beautified_code)

    out = {
        this_file: list(
            difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
        )
    }
    return out
