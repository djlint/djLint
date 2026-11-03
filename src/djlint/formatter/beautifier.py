"""Shared driver for the css and js beautifiers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

from djlint.const import TAG_ATTRIBUTES
from djlint.helpers import (
    RE_FLAGS_IS,
    child_of_unformatted_block,
    compile_pattern,
    mask_raw_text_bodies,
    mask_template_tags,
    restore_template_tags,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Any, Final

    from djlint.settings import Config


def raw_text_block_pattern(tag: str) -> re.Pattern[str]:
    """Match a tag's leading indent, its opening tag and its contents.

    A template tag in the opening tag is read whole, so a ">" in one, as in
    data-x="{{ "a > b" }}", is not taken for the start of the contents. A
    tag that no closing tag follows has none for any tag after it either,
    so the search ends there rather than reading the rest of the file again
    from each.
    """
    return compile_pattern(
        rf"([ ]*?)(<{tag}\b{TAG_ATTRIBUTES}>)(?:(.*?)(?=</{tag}>)|.*+(*SKIP)(*FAIL))", RE_FLAGS_IS
    )


# How many more runs a beautifier gets to settle on a layout of its own.
_MAX_SETTLING_RUNS: Final = 3


def _beautify_indented(
    source: str,
    beautify: Callable[[str, dict[str, Any]], str],
    beautifier_config: Mapping[str, Any],
    indent: str,
) -> str:
    """Beautify source, indenting it below the tag it was written in.

    The beautifier options cannot express a fixed leading indent, so the
    source is laid out twice at different indent levels; the lines that move
    are the ones the beautifier owns, and only those take `indent`. A
    `wrap_line_length` narrow enough to wrap differently at the two levels
    leaves the runs with nothing to compare, and there every line is taken
    as the beautifier's.

    The beautifier does not always reach its own layout in one run: a
    ternary written over lines comes out one way, and that way again comes
    out another. It is run until it leaves its output alone, so formatting
    the file a second time changes nothing.
    """
    options = dict(beautifier_config)
    options["indent_level"] = 1
    laid_out = beautify(source, options)
    for _ in range(_MAX_SETTLING_RUNS):
        again = beautify(laid_out, options)
        if again == laid_out:
            break
        laid_out = again
    lines = laid_out.splitlines()

    if not indent:
        return "".join(f"\n{line}" for line in lines)

    options["indent_level"] = 2
    shifted = beautify(laid_out, options).splitlines()
    comparable = len(lines) == len(shifted)

    return "".join(
        f"\n{line}" if comparable and line == shifted[index] else f"\n{indent}{line}"
        for index, line in enumerate(lines)
    )


def format_blocks(
    html: str,
    config: Config,
    *,
    pattern: re.Pattern[str],
    beautify: Callable[[str, dict[str, Any]], str],
    beautifier_config: Mapping[str, Any],
    holds_code: Callable[[str], bool] = lambda _opening_tag: True,
) -> str:
    """Beautify the contents of every block the pattern matches.

    `holds_code` says from the opening tag whether the beautifier can read
    the contents.

    The blocks are looked for with the bodies of the raw text elements
    blanked, so a `<style` written in a javascript string, as in
    `new RegExp("<style(.*?)>")`, starts no block.
    """

    def format_block(match: re.Match[str]) -> str:
        leading, opening_tag, source = (html[slice(*match.span(group))] for group in (1, 2, 3))

        if (
            not source.strip()
            or not holds_code(opening_tag)
            or child_of_unformatted_block(config, html, match)
        ):
            return html[match.start() : match.end()]

        # The contents go below the line the tag is on, also when the tag
        # follows other markup there, as in `<span>a</span><script>`.
        line_start = html.rfind("\n", 0, match.start(2)) + 1
        before_tag = html[line_start : match.start(2)]
        indent = " " * (len(before_tag) - len(before_tag.lstrip(" ")))
        masked, replacements = mask_template_tags(config, source)
        beautified = _beautify_indented(masked, beautify, beautifier_config, indent)

        for marker, _ in replacements:
            beautified = re.sub(
                rf"\n[ \t]*\n([ \t]*/\*{re.escape(marker)}\*/[ \t]*(?=\n|$))", r"\n\1", beautified
            )

        return (
            f"{leading}{opening_tag}"
            f"{restore_template_tags(beautified, replacements).rstrip()}"
            f"\n{indent}"
        )

    output: list[str] = []
    previous_end = 0
    for match in pattern.finditer(mask_raw_text_bodies(html)):
        output.extend((html[previous_end : match.start()], format_block(match)))
        previous_end = match.end()
    output.append(html[previous_end:])
    return "".join(output)
