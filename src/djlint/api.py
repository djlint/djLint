"""Format and lint text from Python, as the command line does.

This module is the supported way to call djLint from a program, and the
`run()` of a custom rule's `python_module` imports what it needs from here
too. Everything else in the package can change in any release.
"""

from __future__ import annotations

import functools
import inspect
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, cast, final, overload

from djlint._helpers import inside_ignored_linter_block, inside_ignored_rule
from djlint._lint import get_line, linter
from djlint._output import finding_end, finding_position
from djlint._reformat import formatter
from djlint._settings import Config
from djlint._src import has_pragma, is_excluded as _is_excluded

if sys.version_info >= (3, 13):  # pragma: >=3.13 cover
    from typing import NamedTuple
    from warnings import deprecated
else:  # pragma: <3.13 cover
    from typing_extensions import NamedTuple, deprecated

if TYPE_CHECKING:
    import os
    from collections.abc import Callable
    from typing import Any, TypeVar

    # A TypedDict that only exists for type checkers: what a custom rule returns.
    from djlint._types import LintError as LintError  # noqa: PLC0414

    F = TypeVar("F", bound=Callable[..., Any])

__all__ = (
    "Config",
    "Finding",
    "format_text",
    "get_line",
    "inside_ignored_linter_block",
    "inside_ignored_rule",
    "is_excluded",
    "lint_text",
    "load_config",
)


def _warn_on_old_calls(positional: int, message: str) -> Callable[[F], F]:
    """Keep taking the calls of a signature before it was made stricter.

    The stricter signature takes the first `positional` parameters by
    position only and the rest by keyword only. A call that passes one of them
    the other way still works, and warns with `message`.
    """

    def decorate(func: F) -> F:
        signature = inspect.signature(func)
        names = tuple(signature.parameters)[:positional]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if len(args) > positional or not kwargs.keys().isdisjoint(names):
                try:
                    signature.bind(*args, **kwargs)
                except TypeError:
                    pass  # The call below raises it, without a warning first.
                else:
                    warnings.warn(message, FutureWarning, stacklevel=2)
            return func(*args, **kwargs)

        return cast("F", wrapper)

    return decorate


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


# The deprecated overload comes first: the other one would take the `folder`
# keyword into `options`.
@overload
@deprecated("Pass folder to load_config by position", category=FutureWarning)
def load_config(
    *, folder: str | os.PathLike[str], python_rules: bool = True, **options: Any
) -> Config: ...
@overload
def load_config(
    folder: str | os.PathLike[str] = ".", /, *, python_rules: bool = True, **options: Any
) -> Config: ...
@_warn_on_old_calls(1, "Pass folder to load_config by position")
def load_config(
    folder: str | os.PathLike[str] = ".", *, python_rules: bool = True, **options: Any
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


@overload
def is_excluded(config: Config, path: str | os.PathLike[str], /) -> bool: ...
@overload
@deprecated("Pass config and path to is_excluded by position", category=FutureWarning)
def is_excluded(config: Config, path: str | os.PathLike[str]) -> bool: ...
@_warn_on_old_calls(2, "Pass config and path to is_excluded by position")
def is_excluded(config: Config, path: str | os.PathLike[str]) -> bool:
    """Tell whether `exclude`, `extend_exclude` or the gitignore leave out a file."""
    return _is_excluded(config, Path(path))


def _is_turned_off(config: Config, text: str) -> bool:
    if not config.require_pragma:
        return False
    return not has_pragma(config, text.split("\n", 1)[0])


@overload
def format_text(config: Config, text: str, /) -> str: ...
@overload
@deprecated("Pass config and text to format_text by position", category=FutureWarning)
def format_text(config: Config, text: str) -> str: ...
@_warn_on_old_calls(2, "Pass config and text to format_text by position")
def format_text(config: Config, text: str) -> str:
    """Return the formatted text."""
    if _is_turned_off(config, text):
        return text
    return formatter(config, text)


@overload
def lint_text(config: Config, text: str, /, *, filename: str = "-") -> list[Finding]: ...
@overload
@deprecated(
    "Pass config and text to lint_text by position, and filename by keyword", category=FutureWarning
)
def lint_text(config: Config, text: str, filename: str = "-") -> list[Finding]: ...
@_warn_on_old_calls(2, "Pass config and text to lint_text by position, and filename by keyword")
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
