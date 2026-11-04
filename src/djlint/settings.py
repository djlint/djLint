"""Deprecated: `Config` is in `djlint.api`."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from djlint import _settings

if TYPE_CHECKING:
    # The class is final, so a deprecated subclass can't stand in for it;
    # type checkers get the class itself, and code that runs, a warning.
    from djlint._settings import Config as Config  # noqa: PLC0414


def __getattr__(name: str) -> object:
    if name != "Config":
        msg = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)
    warnings.warn(
        "djlint.settings.Config is deprecated, import Config from djlint.api instead",
        FutureWarning,
        stacklevel=2,
    )
    return _settings.Config
