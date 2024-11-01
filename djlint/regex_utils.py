from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any, Callable

import regex as re

FlagsType = Union[re.RegexFlag, int, None]


def search(
    regex: str, text: str, flags: FlagsType = None, **kwargs: Any
) -> re.Match[str] | None:
    return _compile_cached(regex, flags=flags).search(text, **kwargs)


def finditer(
    regex: str, text: str, flags: FlagsType = None, **kwargs: Any
) -> Iterable[re.Match[str]]:
    return _compile_cached(regex, flags=flags).finditer(text, **kwargs)


def sub(
    regex: str,
    repl: str | Callable[[re.Match[str]], str],
    text: str,
    flags: FlagsType = None,
    **kwargs: Any,
) -> str:
    return _compile_cached(regex, flags=flags).sub(repl, text, **kwargs)


def match(
    regex: str, text: str, flags: FlagsType = None, **kwargs: Any
) -> re.Match[str] | None:
    return _compile_cached(regex, flags=flags).match(text, **kwargs)


@cache
def _compile_cached(regex: str, flags: FlagsType = None) -> re.Pattern[str]:
    return re.compile(regex, flags=flags or 0)
