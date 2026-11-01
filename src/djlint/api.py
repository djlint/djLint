"""Format and lint text from Python, as the command line does.

This module is the supported way to call djLint from a program. Everything
else in the package can change in any release.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, final

from djlint.lint import linter
from djlint.output import finding_end, finding_position
from djlint.reformat import formatter
from djlint.settings import Config
from djlint.src import has_pragma, is_excluded as _is_excluded

if sys.version_info >= (3, 13):
    from typing import NamedTuple
else:
    from typing_extensions import NamedTuple

if TYPE_CHECKING:
    import os
    from typing import Any

__all__ = ("Finding", "format_text", "is_excluded", "lint_text", "load_config")


@final
class Finding(NamedTuple):
    """Something the linter reports, from `line:column` to `end_line:end_column`.

    Lines count from 1 and columns from 0, in characters. The end is
    exclusive, and can be on a later line than the start.
    """

    code: str
    message: str
    match: str
    line: int
    column: int
    end_line: int
    end_column: int


def load_config(
    folder: str | os.PathLike[str] = ".",
    *,
    python_rules: bool = True,
    **options: Any,
) -> Config:
    """Read the configuration that applies to the files of a folder.

    Options take the names of the command line, with underscores, and work
    as they do there: a value counts if it is set, so `False` doesn't turn off
    what the configuration turns on. With `python_rules=False`, custom rules
    with a `python_module` aren't loaded,
    which keeps the project's code from running. Their names are then in
    `config.skipped_rules`.
    """
    return Config(str(folder), python_rules=python_rules, **options)


def is_excluded(config: Config, path: str | os.PathLike[str]) -> bool:
    """Tell whether `exclude`, `extend_exclude` or the gitignore leave out a file."""
    return _is_excluded(config, Path(path))


def _is_turned_off(config: Config, text: str) -> bool:
    if not config.require_pragma:
        return False
    return not has_pragma(config, text.split("\n", 1)[0])


def format_text(config: Config, text: str) -> str:
    """Return the formatted text."""
    if _is_turned_off(config, text):
        return text
    return formatter(config, text)


def lint_text(config: Config, text: str, filename: str = "-") -> list[Finding]:
    """Return the findings in the text, in document order.

    `filename` is what `per-file-ignores` is matched against.
    """
    if _is_turned_off(config, text):
        return []
    # As reading a file does, or a rule on blank lines misses `\r\n`.
    text = text.replace("\r\n", "\n")
    errors = linter(config, text, filename, Path(filename).as_posix())[filename]
    return [
        Finding(
            error["code"],
            error["message"],
            error["match"],
            *finding_position(error),
            *finding_end(error),
        )
        for error in sorted(errors, key=finding_position)
    ]
