"""Test module for custom rules."""

# ruff: noqa: ARG001
from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.lint import get_line

if TYPE_CHECKING:
    from typing_extensions import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> tuple[LintError, ...]:
    """Rule that fails if if the html file contains 'bad'.

    In the real world, this should be done with a simple regex rule.
    """
    return tuple(
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in re.finditer(r"bad", html)
    )
