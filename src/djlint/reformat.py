"""Djlint reformat html files."""

# import difflib
# from pathlib import Path

# from .formatter.compress import compress_html
# from .formatter.condense import condense_html
# from .formatter.expand import expand_html
# from .formatter.indent import indent_html
# from .settings import Config


# def reformat_file(config: Config, this_file: Path) -> dict:
#     """Reformat html file."""
#     rawcode = this_file.read_text(encoding="utf8")

#     compressed = compress_html(rawcode, config)
#     expanded = expand_html(compressed, config)
#     condensed = condense_html(expanded, config)
#     indented = indent_html(condensed, config)

#     beautified_code = indented

#     if config.check is not True:
#         # update the file
#         this_file.write_text(beautified_code, encoding="utf8")

#     out = {
#         this_file: list(
#             difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
#         )
#     }
#     return out


import difflib
from pathlib import Path

from .formatter.indent import indent_html
from .settings import Config


def reformat_file(config: Config, this_file: Path) -> dict:
    """Reformat html file."""
    rawcode = this_file.read_text(encoding="utf8")

    indented = indent_html(rawcode, config)
    # indented = condense_html(indented, config)

    beautified_code = indented #+ "\n"

    if config.check is not True:
        # update the file
        this_file.write_text(beautified_code, encoding="utf8")

    out = {
        this_file: list(
            difflib.unified_diff(rawcode.splitlines(), beautified_code.splitlines())
        )
    }
    return out
