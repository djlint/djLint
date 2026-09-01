"""Djlint reformat html files.

Much code is borrowed from https://github.com/rareyman/HTMLBeautify, many thanks!
"""

from __future__ import annotations

import difflib
from typing import TYPE_CHECKING

import regex as re

from djlint.formatter.autofix import apply_autofixes
from djlint.formatter.class_attributes import (
    restore_class_attribute_newlines,
    restore_verbatim_attribute_newlines,
)
from djlint.formatter.compress import compress_html
from djlint.formatter.condense import clean_whitespace, condense_html
from djlint.formatter.expand import expand_html
from djlint.formatter.indent import indent_html
from djlint.helpers import mask_unformatted_blocks, restore_unformatted_blocks

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Final

    from djlint.settings import Config


_CARRIAGE_RETURN_LINE_ENDING_PATTERN: Final = re.compile(
    r"\r\n?", cache_pattern=False
)


def formatter(config: Config, rawcode: str) -> str:
    """Format a html string.

    Line endings are normalized with a pattern rather than
    str.splitlines(), which also breaks on U+2028, U+0085 and form feed.
    Those are content: rewriting one as a newline breaks a javascript
    string that holds it.
    """
    if not rawcode:
        return rawcode

    normalized_code = _CARRIAGE_RETURN_LINE_ENDING_PATTERN.sub(
        "\n", rawcode
    ).removesuffix("\n")
    normalized_code, unformatted_blocks = mask_unformatted_blocks(
        normalized_code
    )

    normalized_code = apply_autofixes(normalized_code, config)

    compressed = compress_html(normalized_code, config)

    expanded = expand_html(compressed, config)

    condensed = clean_whitespace(expanded, config)

    indented_code = indent_html(condensed, config)

    beautified_code = condense_html(
        indented_code, config, authored_html=compressed
    )

    if config.format_css:
        from djlint.formatter.css import format_css  # noqa: PLC0415

        beautified_code = format_css(beautified_code, config)

    if config.format_js:
        from djlint.formatter.js import format_js  # noqa: PLC0415

        beautified_code = format_js(beautified_code, config)

    if config.preserve_class_newlines:
        beautified_code = restore_class_attribute_newlines(beautified_code)

    beautified_code = restore_verbatim_attribute_newlines(beautified_code)

    beautified_code = restore_unformatted_blocks(
        beautified_code, unformatted_blocks
    )

    return _match_source_line_endings(beautified_code, rawcode)


def _match_source_line_endings(formatted: str, rawcode: str) -> str:
    """Write CRLF back when the source's first line ending used one."""
    first_newline = rawcode.find("\n")
    if first_newline < 0 or rawcode[max(first_newline - 1, 0)] != "\r":
        return formatted

    return formatted.replace("\r", "").replace("\n", "\r\n")


def reformat_string(
    config: Config, rawcode: str, filename: str
) -> tuple[dict[str, tuple[str, ...]], str]:
    """Reformat an html string."""
    beautified_code = formatter(config, rawcode)

    return {
        filename: tuple(
            difflib.unified_diff(
                rawcode.splitlines(), beautified_code.splitlines()
            )
        )
    }, beautified_code


def reformat_file(
    config: Config, this_file: Path
) -> dict[str, tuple[str, ...]]:
    """Reformat html file."""
    with this_file.open(encoding="utf-8", newline="") as f:
        rawcode = f.read()

    format_message, beautified_code = reformat_string(
        config, rawcode, str(this_file)
    )

    if config.check is not True and beautified_code != rawcode:
        with this_file.open("w", encoding="utf-8", newline="") as f:
            f.write(beautified_code)

    return format_message
