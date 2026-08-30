"""Shared driver for the css and js beautifiers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IS,
    child_of_unformatted_block,
    mask_template_tags,
    restore_template_tags,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Any

    from djlint.settings import Config


def raw_text_block_pattern(tag: str) -> re.Pattern[str]:
    """Match a tag's leading indent, its opening tag and its contents."""
    return re.compile(
        rf"([ ]*?)(<{tag}\b(?:\"[^\"]*\"|'[^']*'|{{[^}}]*}}|[^'\">{{}}])*>)(.*?)(?=</{tag}>)",
        RE_FLAGS_IS,
        cache_pattern=False,
    )


def _beautify_indented(
    source: str,
    beautify: Callable[[str, dict[str, Any]], str],
    beautifier_config: Mapping[str, Any],
    indent: str,
) -> str:
    """Beautify source, indenting it below the tag it was written in.

    The beautifier options cannot express a fixed leading indent, so the
    source is laid out twice at different indent levels; the lines that move
    are the ones the beautifier owns, and only those take `indent`.
    """
    options = dict(beautifier_config)

    options["indent_level"] = 1
    lines = beautify(source, options).splitlines()

    options["indent_level"] = 2
    shifted = beautify(source, options).splitlines()

    return "".join(
        f"\n{indent}{line}" if line != moved else f"\n{line}"
        for line, moved in zip(lines, shifted, strict=False)
    )


def format_blocks(
    html: str,
    config: Config,
    *,
    pattern: re.Pattern[str],
    beautify: Callable[[str, dict[str, Any]], str],
    beautifier_config: Mapping[str, Any],
) -> str:
    """Beautify the contents of every block the pattern matches."""

    def format_block(match: re.Match[str]) -> str:
        leading, opening_tag, source = match.group(1, 2, 3)

        if not source.strip() or child_of_unformatted_block(
            config, html, match
        ):
            return match.group()

        indent = " " * len(leading)
        masked, replacements = mask_template_tags(config, source)
        beautified = _beautify_indented(
            masked, beautify, beautifier_config, indent
        )

        for marker, _ in replacements:
            beautified = re.sub(
                rf"\n[ \t]*\n([ \t]*/\*{re.escape(marker)}\*/[ \t]*(?=\n|$))",
                r"\n\1",
                beautified,
            )

        return (
            f"{leading}{opening_tag}"
            f"{restore_template_tags(beautified, replacements).rstrip()}"
            f"\n{indent}"
        )

    return pattern.sub(format_block, html)
