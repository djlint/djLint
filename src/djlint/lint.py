"""Deprecated: what custom rules imported from here is in `djlint.api`."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from djlint import _lint
from djlint._helpers import keep_mypyc_wheels_from_crashing

if sys.version_info >= (3, 13):  # pragma: >=3.13 cover
    from warnings import deprecated
else:  # pragma: <3.13 cover
    from typing_extensions import deprecated

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


@deprecated("Import get_line from djlint.api instead", category=FutureWarning)
@keep_mypyc_wheels_from_crashing
def get_line(start: int, line_ends: Sequence[Mapping[str, int]]) -> str:
    """Get the line number and index of match."""
    return _lint.get_line(start, line_ends)
