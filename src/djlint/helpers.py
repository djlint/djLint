"""Collection of shared djLint functions."""
# ruff: noqa: ERA001

from __future__ import annotations

import itertools
from bisect import bisect_right
from functools import lru_cache
from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Final

    from typing_extensions import TypeVar

    from djlint.settings import Config
    from djlint.types import SpanMatch

    T = TypeVar("T")


RE_FLAGS_IS: Final = re.I | re.S
RE_FLAGS_IX: Final = re.I | re.X
RE_FLAGS_MS: Final = re.M | re.S
RE_FLAGS_MX: Final = re.M | re.X
RE_FLAGS_IMS: Final = re.I | re.M | re.S
RE_FLAGS_IMX: Final = re.I | re.M | re.X
RE_FLAGS_ISX: Final = re.I | re.S | re.X
RE_FLAGS_IMSX: Final = re.I | re.M | re.S | re.X

_PATTERN_CACHE_SIZE = 32
_SPAN_CACHE_SIZE = 1


@lru_cache(maxsize=_PATTERN_CACHE_SIZE)
def _compile_pattern(pattern: str, flags: int, /) -> re.Pattern[str]:
    return re.compile(pattern, flags=flags)


def _finditer(
    pattern: str, string: str, /, *, flags: int
) -> Iterable[re.Match[str]]:
    return _compile_pattern(pattern, flags).finditer(string)


def _search(
    pattern: str, string: str, /, *, flags: int
) -> re.Match[str] | None:
    return _compile_pattern(pattern, flags).search(string)


def _last_item(iterable: Iterable[T], /) -> T | None:
    last = None
    for item in iterable:
        last = item
    return last


def _inside_non_overlapping_span(
    spans: tuple[tuple[int, int], ...], match_start: int, match_end: int, /
) -> bool:
    index = bisect_right(spans, (match_start, float("inf"))) - 1
    if index < 0:
        return False

    span_start, span_end = spans[index]
    return span_start <= match_start and match_end <= span_end


def is_ignored_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    inline = _last_item(
        _finditer(config.ignored_blocks_inline, item, flags=RE_FLAGS_IMSX)
    )
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(
        _search(
            config.ignored_block_opening, item[last_index:], flags=RE_FLAGS_IX
        )
    )


def is_script_style_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    inline = _last_item(
        _finditer(config.script_style_inline, item, flags=RE_FLAGS_IMSX)
    )
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(
        _search(
            config.script_style_opening, item[last_index:], flags=RE_FLAGS_IX
        )
    )


def inside_protected_trans_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.

    True = non indentable > inside ignored trans block
    False = indentable > either inside a trans trimmed block, or somewhere else, but not a trans non trimmed :)
    """
    close_block = _search(
        config.ignored_trans_blocks_closing, match.group(), flags=RE_FLAGS_IX
    )

    if not close_block:
        return False

    non_trimmed = _last_item(
        _finditer(config.ignored_trans_blocks, html, flags=RE_FLAGS_ISX)
    )

    trimmed = _last_item(
        _finditer(config.trans_trimmed_blocks, html, flags=RE_FLAGS_ISX)
    )

    # who is max?
    if non_trimmed and (not trimmed or non_trimmed.end() > trimmed.end()):
        # non trimmed!
        # check that this is not an inline block.
        non_trimmed_inline = bool(
            _search(
                config.ignored_trans_blocks, match.group(), flags=RE_FLAGS_ISX
            )
        )

        if non_trimmed_inline:
            last_index = non_trimmed.end()  # get the last index. The ignored opening should start after this.

            return bool(
                _search(
                    config.ignored_trans_blocks_closing,
                    html[last_index:],
                    flags=RE_FLAGS_IX,
                )
            )

        return close_block.end() <= non_trimmed.end()

    if trimmed:
        # inside a trimmed block, we can return true to continue as if
        # this is a indentable block
        return close_block.end() > trimmed.end()
    return False

    # print(close_block)
    # if non_trimmed:
    #     last_index = (
    #         non_trimmed[-1].end()
    #     )  # get the last index. The ignored opening should start after this.

    # return re.search(
    #     config.ignored_trans_blocks_closing,
    #     html[last_index:],
    #     flags=RE_FLAGS_IX,
    # )


def is_ignored_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.
    """
    inline = _last_item(
        _finditer(config.ignored_inline_blocks, item, flags=RE_FLAGS_IX)
    )
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(
        _search(
            config.ignored_block_closing, item[last_index:], flags=RE_FLAGS_IX
        )
    )


def is_script_style_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.
    """
    inline = _last_item(
        _finditer(config.script_style_inline, item, flags=RE_FLAGS_IX)
    )
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(
        _search(
            config.script_style_closing, item[last_index:], flags=RE_FLAGS_IX
        )
    )


def is_safe_closing_tag(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    inline = _last_item(
        _finditer(
            config.ignored_inline_blocks + r" | " + config.ignored_blocks,
            item,
            flags=RE_FLAGS_IMSX,
        )
    )
    last_index = (
        inline.end()  # get the last index. The ignored opening should start after this.
        if inline
        else 0
    )
    return bool(
        _search(config.safe_closing_tag, item[last_index:], flags=RE_FLAGS_IX)
    )


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_template_block(
    html: str, /, *, template_blocks: str
) -> tuple[tuple[int, int], ...]:
    return tuple(
        x.span() for x in _finditer(template_blocks, html, flags=RE_FLAGS_IMSX)
    )


def inside_template_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Check if a re.Match is inside of a template block."""
    match_start, match_end = match.span()
    return _inside_non_overlapping_span(
        _inside_template_block(html, template_blocks=config.template_blocks),
        match_start,
        match_end,
    )


def mask_template_tags(
    config: Config, html: str
) -> tuple[str, list[tuple[str, str]]]:
    """Hide template tags from formatters that parse JS or CSS."""
    if "{%" not in html and "{{" not in html and "{#" not in html:
        return html, []

    replacements: list[tuple[str, str]] = []
    marker_prefix = "__DJLINT_TEMPLATE_TAG_"
    while marker_prefix in html:
        marker_prefix = f"_{marker_prefix}"

    def replace(match: re.Match[str]) -> str:
        marker = f"{marker_prefix}{len(replacements)}__"
        replacements.append((marker, match.group()))
        line_start = html.rfind("\n", 0, match.start()) + 1
        line_end = html.find("\n", match.end())
        if line_end < 0:
            line_end = len(html)
        if (
            not html[line_start : match.start()].strip()
            and not html[match.end() : line_end].strip()
        ):
            return f"/*{marker}*/"
        return marker

    template_tags = rf"(?:{config.template_tags})|\{{\#(?:(?!\#\}}).)*\#\}}"

    return (
        _compile_pattern(template_tags, RE_FLAGS_ISX).sub(replace, html),
        replacements,
    )


def restore_template_tags(
    html: str, replacements: list[tuple[str, str]]
) -> str:
    """Put masked template tags back after JS or CSS formatting."""
    for marker, replacement in replacements:
        html = html.replace(f"/*{marker}*/", replacement).replace(
            marker, replacement
        )
    return html


_UNFORMATTED_BLOCKS = r"""
      <!--\s*djlint\:off\s*-->.*?(?:<!--\s*djlint\:on\s*-->|\Z)
    | {\#\s*djlint\:\s*off\s*\#}.*?(?:{\#\s*djlint\:\s*on\s*\#}|\Z)
    | {%\s*comment\s*%\}\s*djlint\:off\s*\{%\s*endcomment\s*%\}.*?(?:{%\s*comment\s*%\}\s*djlint\:on\s*\{%\s*endcomment\s*%\}|\Z)
    | {{!--\s*djlint\:off\s*--}}.*?(?:{{!--\s*djlint\:on\s*--}}|\Z)
    | {{-?\s*/\*\s*djlint\:off\s*\*/\s*-?}}.*?(?:{{-?\s*/\*\s*djlint\:on\s*\*/\s*-?}}|\Z)
"""


def mask_unformatted_blocks(html: str) -> tuple[str, list[tuple[str, str]]]:
    """Hide djlint:off blocks from the formatter pipeline."""
    if "djlint:" not in html:
        return html, []

    replacements: list[tuple[str, str]] = []
    marker_prefix = "__DJLINT_UNFORMATTED_BLOCK_"
    while marker_prefix in html:
        marker_prefix = f"_{marker_prefix}"

    def replace(match: re.Match[str]) -> str:
        marker = f"/*{marker_prefix}{len(replacements)}__*/"
        replacements.append((marker, match.group()))
        return marker

    return (
        _compile_pattern(_UNFORMATTED_BLOCKS, RE_FLAGS_IMSX).sub(replace, html),
        replacements,
    )


def restore_unformatted_blocks(
    html: str, replacements: list[tuple[str, str]]
) -> str:
    """Put masked djlint:off blocks back after formatting."""
    for marker, replacement in replacements:

        def replace_marker(
            match: re.Match[str], replacement: str = replacement
        ) -> str:
            indent = match.group(1)
            lines = replacement.split("\n")
            lines[0] = indent + lines[0].lstrip()
            if "djlint:on" in lines[-1]:
                lines[-1] = indent + lines[-1].lstrip()
            return "\n".join(lines)

        html = _compile_pattern(
            rf"^([ \t]*){re.escape(marker)}[ \t]*$", RE_FLAGS_MX
        ).sub(replace_marker, html)
        html = html.replace(marker, replacement)
    return html


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_html_attribute(
    html: str, /, *, html_tag_regex: str
) -> tuple[tuple[int, int], ...]:
    return tuple(
        # group 3 are the attributes
        attr_span
        for x in _finditer(html_tag_regex, html, flags=RE_FLAGS_IMSX)
        if (attr_span := x.span(3))[0] >= 0
    )


def inside_html_attribute(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Check if a re.Match is inside of an html attribute."""
    match_start, match_end = match.span()
    return _inside_non_overlapping_span(
        _inside_html_attribute(html, html_tag_regex=config.html_tag_regex),
        match_start,
        match_end,
    )


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_ignored_linter_block(
    html: str, /, *, ignored_linter_blocks: str
) -> tuple[tuple[int, int], ...]:
    return tuple(
        x.span()
        for x in _finditer(ignored_linter_blocks, html, flags=RE_FLAGS_IMSX)
    )


def inside_ignored_linter_block(
    config: Config, html: str, match: SpanMatch
) -> bool:
    """Check if a re.Match is inside of a ignored linter block."""
    match_start, match_end = match.span()
    return _inside_non_overlapping_span(
        _inside_ignored_linter_block(
            html, ignored_linter_blocks=config.ignored_linter_blocks
        ),
        match_start,
        match_end,
    )


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_ignored_block(
    html: str, /, *, ignored_blocks: str, ignored_inline_blocks: str
) -> tuple[tuple[int, int], ...]:
    return tuple(
        x.span()
        for x in itertools.chain(
            _finditer(ignored_blocks, html, flags=RE_FLAGS_IMSX),
            _finditer(ignored_inline_blocks, html, flags=RE_FLAGS_IX),
        )
    )


def inside_ignored_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match_start, ignored_match_end in _inside_ignored_block(
        html,
        ignored_blocks=config.ignored_blocks,
        ignored_inline_blocks=config.ignored_inline_blocks,
    ):
        if (
            ignored_match_start <= match_start
            and match_end <= ignored_match_end
        ):
            return True
    return False


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _child_of_unformatted_block(
    html: str, /, *, unformatted_blocks: str, unformatted_blocks_coarse: str
) -> tuple[tuple[int, int], ...]:
    if not _search(unformatted_blocks_coarse, html, flags=RE_FLAGS_IMSX):
        return ()
    return tuple(
        x.span()
        for x in _finditer(unformatted_blocks, html, flags=RE_FLAGS_IMSX)
    )


def child_of_unformatted_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match_start, ignored_match_end in _child_of_unformatted_block(
        html,
        unformatted_blocks=config.unformatted_blocks,
        unformatted_blocks_coarse=config.unformatted_blocks_coarse,
    ):
        if ignored_match_start < match_start and match_end <= ignored_match_end:
            return True
    return False


def child_of_ignored_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match in itertools.chain(
        _finditer(config.ignored_blocks, html, flags=RE_FLAGS_IMSX),
        _finditer(config.ignored_inline_blocks, html, flags=RE_FLAGS_IX),
    ):
        ignored_match_start, ignored_match_end = ignored_match.span()
        if ignored_match_start < match_start and match_end <= ignored_match_end:
            return True
    return False


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _overlaps_ignored_block(
    html: str, /, *, ignored_blocks: str, ignored_inline_blocks: str
) -> tuple[tuple[int, int], ...]:
    return tuple(
        x.span()
        for x in itertools.chain(
            _finditer(ignored_blocks, html, flags=RE_FLAGS_IMSX),
            _finditer(ignored_inline_blocks, html, flags=RE_FLAGS_IX),
        )
    )


def overlaps_ignored_block(config: Config, html: str, match: SpanMatch) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    match_start, match_end = match.span()
    for ignored_match_start, ignored_match_end in _overlaps_ignored_block(
        html,
        ignored_blocks=config.ignored_blocks,
        ignored_inline_blocks=config.ignored_inline_blocks,
    ):
        # don't require the match to be fully inside the ignored block.
        # poorly build html will probably span ignored blocks and should be ignored.
        if (ignored_match_start <= match_start <= ignored_match_end) or (
            ignored_match_start <= match_end <= ignored_match_end
        ):
            return True
    return False


@lru_cache(maxsize=_SPAN_CACHE_SIZE)
def _inside_ignored_rule(
    html: str, /, *, ignored_rules: tuple[str, ...]
) -> tuple[tuple[int, int, frozenset[str], bool], ...]:
    rule_spans = []
    for rule_regex in ignored_rules:
        for ignored_match in _finditer(rule_regex, html, flags=RE_FLAGS_ISX):
            ignored_match_start, ignored_match_end = ignored_match.span()
            rule_names = ignored_match.group(1).strip()
            rule_spans.append((
                ignored_match_start,
                ignored_match_end,
                frozenset(x for x in re.split(r"\s|,", rule_names) if x),
                not rule_names,
            ))
    return tuple(rule_spans)


def inside_ignored_rule(
    config: Config, html: str, match: SpanMatch, rule: str
) -> bool:
    """Check if match is inside an ignored pattern."""
    match_start, match_end = match.span()
    for (
        ignored_match_start,
        ignored_match_end,
        ignored_rule_names,
        ignore_all_rules,
    ) in _inside_ignored_rule(html, ignored_rules=config.ignored_rules):
        if (
            (ignored_match_start <= match_start <= ignored_match_end)
            and rule in ignored_rule_names
        ) or (
            (ignored_match_start <= match_end <= ignored_match_end)
            and ignore_all_rules
        ):
            return True
    return False
