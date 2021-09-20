"""Djlint reformat html files.

Much code is borrowed from https://github.com/rareyman/HTMLBeautify, many thanks!
"""

import difflib
from pathlib import Path

from .formatter.compress_html import compress_html
from .formatter.expand_html import expand_html
from .formatter.indent_html import indent_html
from .settings import Config


def reformat_file(config: Config, check: bool, this_file: Path) -> dict:
    """Reformat html file."""
    rawcode = this_file.read_text(encoding="utf8")

    expanded = expand_html(rawcode, config)
    compressed = compress_html(expanded, config)
    indented = indent_html(compressed, config)

    beautified_code = indented

    if check is not True:
        # update the file
        this_file.write_text(beautified_code)

    out = {
        this_file: list(
            difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
        )
    }
    return out
