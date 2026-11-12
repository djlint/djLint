"""djLint · lint and reformat HTML templates."""
# ruff: noqa: RUF067

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

    from djlint._cli import main as main, process as process, process_stdin as process_stdin

# The command line used to live here. Its names are still found here, but
# only loaded when asked for, so that importing djlint.api, as editors do,
# does not build the command line too.
_CLI_NAMES: Final = frozenset(("main", "process", "process_stdin"))


def __getattr__(name: str) -> object:
    if name in _CLI_NAMES:
        from djlint import _cli  # noqa: PLC0415

        value = getattr(_cli, name)
        globals()[name] = value
        return value
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
