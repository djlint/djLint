from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from typing import Any, Callable

    from regex._regex import Scanner


def match(
    pattern: str, string: str, /, *, flags: int = 0
) -> re.Match[str] | None:
    return _compile_cached(pattern, flags=flags).match(string)


def search(
    pattern: str, string: str, /, *, flags: int = 0
) -> re.Match[str] | None:
    return _compile_cached(pattern, flags=flags).search(string)


def sub(
    pattern: str,
    repl: str | Callable[[re.Match[str]], str],
    string: str,
    /,
    *,
    flags: int = 0,
) -> str:
    return _compile_cached(pattern, flags=flags).sub(repl, string)


def split(pattern: str, string: str, /) -> list[str | Any]:
    return _compile_cached(pattern).split(string)


def finditer(pattern: str, string: str, /, *, flags: int = 0) -> Scanner[str]:
    return _compile_cached(pattern, flags=flags).finditer(string)


@cache
def _compile_cached(pattern: str, /, *, flags: int = 0) -> re.Pattern[str]:
    return re.compile(pattern, flags=flags, cache_pattern=False)
