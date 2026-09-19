"""Test that djLint compiles its patterns the same on any supported regex.

uv run pytest tests/test_compile_pattern.py
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import regex as re

from djlint import helpers

if TYPE_CHECKING:
    from typing import Final


def _regex_accepts_cache_pattern() -> bool:
    try:
        re.compile(r"", cache_pattern=False)
    except (TypeError, ValueError):
        return False
    return True


_SOURCE_ROOT: Final = Path("src/djlint")
_SHIM_FILE: Final = _SOURCE_ROOT / "helpers.py"
_PATTERNS: Final = (
    (r"a(b)c", 0),
    (r"a(b)c", re.I),
    (r"a (b) c  # a comment the x flag drops", helpers.RE_FLAGS_IX),
    (r"^a.c$", helpers.RE_FLAGS_IMSX),
)


@pytest.mark.parametrize(("pattern", "flags"), _PATTERNS)
def test_compile_pattern_compiles_what_regex_compile_would(
    pattern: str, flags: int
) -> None:
    compiled = helpers.compile_pattern(pattern, flags)
    expected = re.compile(pattern, flags)

    assert compiled.pattern == expected.pattern
    assert compiled.flags == expected.flags


@pytest.mark.parametrize(("pattern", "flags"), _PATTERNS)
def test_compile_pattern_compiles_the_same_on_an_older_regex(
    pattern: str, flags: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A regex without ``cache_pattern`` gets the same pattern, cached."""
    monkeypatch.setattr(helpers, "_CACHE_PATTERN_SUPPORTED", False)

    compiled = helpers.compile_pattern(pattern, flags)
    expected = re.compile(pattern, flags)

    assert compiled.pattern == expected.pattern
    assert compiled.flags == expected.flags


@pytest.mark.skipif(
    not _regex_accepts_cache_pattern(),
    reason="the installed regex predates cache_pattern",
)
def test_compile_pattern_leaves_the_regex_cache_alone() -> None:
    """What the shim is for, when the installed regex can do it."""
    assert re.compile(r"cached\b") is re.compile(r"cached\b")
    assert helpers.compile_pattern(r"uncached\b") is not (
        helpers.compile_pattern(r"uncached\b")
    )


def test_only_the_shim_names_cache_pattern() -> None:
    """Everything else compiles through it, so an old regex still runs."""
    assert [
        str(path)
        for path in sorted(_SOURCE_ROOT.rglob("*.py"))
        if path != _SHIM_FILE
        and "cache_pattern" in path.read_text(encoding="utf-8")
    ] == []
