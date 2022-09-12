"""Djlint reformat html files.

Much code is borrowed from https://github.com/rareyman/HTMLBeautify, many thanks!
"""

import difflib
from pathlib import Path

from .formatter.compress import compress_html
from .formatter.condense import condense_html
from .formatter.css import format_css
from .formatter.expand import expand_html
from .formatter.indent import indent_html
from .formatter.js import format_js
from .settings import Config


def reformat_file(config: Config, this_file: Path) -> dict:
    """Reformat html file."""
    rawcode = this_file.read_text(encoding="utf8")

    compressed = compress_html(rawcode, config)

    expanded = expand_html(compressed, config)

    condensed = condense_html(expanded, config)

    beautified_code = indent_html(condensed, config)

    if config.format_css:
        beautified_code = format_css(beautified_code, config)

    if config.format_js:
        beautified_code = format_js(beautified_code, config)

    if config.check is not True:
        # update the file
        this_file.write_text(beautified_code, encoding="utf8")

    out = {
        str(this_file): list(
            difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
        )
    }
    return out
