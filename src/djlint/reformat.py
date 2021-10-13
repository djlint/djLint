"""Djlint reformat html files.

Much code is borrowed from https://github.com/rareyman/HTMLBeautify, many thanks!
"""

import difflib
from pathlib import Path
import regex as re

from .formatter.compress_html import compress_html
from .formatter.expand_html import expand_html
from .formatter.indent_html import indent_html
from .settings import Config

html_patterns = [re.compile(r"<!--\s*format\s*-->")]
django_jinja_patterns = [
    re.compile(r"\{#\s*format\s*#\}"),
    re.compile(r"\{%\s*comment\s*%\}\s*format\s*\{%\s*endcomment\s*%\}"),
]
nunjucks_patterns = [re.compile(r"\{#\s*format\s*#\}")]
handlebars_patterns = [re.compile(r"\{\{!--\s*format\s*--\}\}")]
golang_patterns = [
    re.compile(r"\{\{\s*/\*\s*format\s*\*/\s*\}\}"),
    re.compile(r"\{\{-\s*/\*\s*format\s*/\*\s*-\}\}"),
]


def has_pragma(config: Config, html_str: str):
    first_line = html_str.partition("\n")[0]

    pragma_patterns = {
        "django": django_jinja_patterns + html_patterns,
        "jinja": django_jinja_patterns + html_patterns,
        "nunjucks": nunjucks_patterns + html_patterns,
        "handlebars": handlebars_patterns + html_patterns,
        "golang": golang_patterns + html_patterns,
        "all": django_jinja_patterns
        + nunjucks_patterns
        + handlebars_patterns
        + golang_patterns
        + html_patterns,
    }

    for pattern in pragma_patterns[config.profile]:
        if re.match(pattern, first_line):
            return True
    return False


def reformat_file(config: Config, check: bool, this_file: Path) -> dict:
    """Reformat html file."""
    rawcode = this_file.read_text(encoding="utf8")

    if config.require_pragma and not has_pragma(config, rawcode):
        # The file should not be reformatted
        return {this_file: []}

    expanded = expand_html(rawcode, config)
    compressed = compress_html(expanded, config)
    indented = indent_html(compressed, config)

    beautified_code = indented

    if check is not True:
        # update the file
        this_file.write_text(beautified_code, encoding="utf8")

    out = {
        this_file: list(
            difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
        )
    }
    return out
