"""Write a block's name into the tag that closes it."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IS,
    inside_ignored_linter_block,
    overlaps_ignored_block,
)

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_BLOCK_PATTERN: Final = re.compile(
    r"(?P<keyword>{%[-+]?\s*(?P<closing>end)?block(?!trans)\b)"
    r"(?:\s+(?P<name>[^\s%+-](?:[^\s%]*[^\s%+-])?))?"
    r"(?:(?!%}).)*?[-+]?%}",
    RE_FLAGS_IS,
    cache_pattern=False,
)


def name_endblocks(html: str, config: Config) -> str:
    """Name the `{% endblock %}` of a block written across lines.

    This is what `T003` asks for, and only where it asks: a block opened
    and closed on one line says which block it closes by itself. An
    endblock that already carries a name is left as written, and so is one
    closing a block that has no name to copy.
    """
    if not config.name_endblocks:
        return html

    insertions: list[tuple[int, str]] = []
    open_blocks: list[tuple[str | None, int]] = []

    for match in _BLOCK_PATTERN.finditer(html):
        if overlaps_ignored_block(
            config, html, match
        ) or inside_ignored_linter_block(config, html, match):
            continue

        if not match.group("closing"):
            open_blocks.append((match.group("name"), match.end()))
            continue

        if not open_blocks:
            continue

        name, opened_at = open_blocks.pop()
        if (
            name
            and not match.group("name")
            and "\n" in html[opened_at : match.start()]
        ):
            insertions.append((match.end("keyword"), f" {name}"))

    if not insertions:
        return html

    parts: list[str] = []
    cursor = 0
    for position, name in insertions:
        parts.extend((html[cursor:position], name))
        cursor = position
    parts.append(html[cursor:])
    return "".join(parts)
