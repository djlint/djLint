"""Deprecated: what custom rules imported from here is in `djlint.api`."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from djlint import _helpers
from djlint._helpers import keep_mypyc_wheels_from_crashing

if sys.version_info >= (3, 13):  # pragma: >=3.13 cover
    from warnings import deprecated
else:  # pragma: <3.13 cover
    from typing_extensions import deprecated

if TYPE_CHECKING:
    from djlint._settings import Config
    from djlint._types import SpanMatch


@deprecated("Import inside_ignored_linter_block from djlint.api instead", category=FutureWarning)
@keep_mypyc_wheels_from_crashing
def inside_ignored_linter_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Check if a re.Match is inside of a ignored linter block."""
    return _helpers.inside_ignored_linter_block(config, html, match)


@deprecated("Import inside_ignored_rule from djlint.api instead", category=FutureWarning)
@keep_mypyc_wheels_from_crashing
def inside_ignored_rule(config: Config, html: str, match: SpanMatch, rule: str) -> bool:
    """Check if match is inside an ignored pattern."""
    return _helpers.inside_ignored_rule(config, html, match, rule)
