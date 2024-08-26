"""Collection of shared djLint functions."""
# ruff: noqa: ERA001

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from .settings import Config


def is_ignored_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = tuple(
        re.finditer(
            config.ignored_blocks_inline,
            item,
            flags=re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL,
        )
    )

    if inline:
        last_index = (
            inline[-1].end()
        )  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            config.ignored_block_opening,
            item[last_index:],
            flags=re.IGNORECASE | re.VERBOSE,
        )
    )


def is_script_style_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = tuple(
        re.finditer(
            config.script_style_inline,
            item,
            flags=re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL,
        )
    )

    if inline:
        last_index = (
            inline[-1].end()
        )  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            config.script_style_opening,
            item[last_index:],
            flags=re.IGNORECASE | re.VERBOSE,
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
    last_index = 0
    close_block = re.search(
        config.ignored_trans_blocks_closing,
        match.group(),
        flags=re.IGNORECASE | re.VERBOSE,
    )

    if not close_block:
        return False

    non_trimmed = tuple(
        re.finditer(
            config.ignored_trans_blocks,
            html,
            flags=re.IGNORECASE | re.VERBOSE | re.DOTALL,
        )
    )

    trimmed = tuple(
        re.finditer(
            config.trans_trimmed_blocks,
            html,
            flags=re.IGNORECASE | re.VERBOSE | re.DOTALL,
        )
    )

    # who is max?
    if non_trimmed and (
        not trimmed or non_trimmed[-1].end() > trimmed[-1].end()
    ):
        # non trimmed!
        # check that this is not an inline block.
        non_trimmed_inline = any(
            re.finditer(
                config.ignored_trans_blocks,
                match.group(),
                flags=re.IGNORECASE | re.VERBOSE | re.DOTALL,
            )
        )

        if non_trimmed_inline:
            last_index = non_trimmed[
                -1
            ].end()  # get the last index. The ignored opening should start after this.

            return bool(
                re.search(
                    config.ignored_trans_blocks_closing,
                    html[last_index:],
                    flags=re.IGNORECASE | re.VERBOSE,
                )
            )

        return close_block.end(0) <= non_trimmed[-1].end()

    if trimmed:
        # inside a trimmed block, we can return true to continue as if
        # this is a indentable block
        return close_block.end(0) > trimmed[-1].end()
    return False

    # print(close_block)
    # if non_trimmed:
    #     last_index = (
    #         non_trimmed[-1].end()
    #     )  # get the last index. The ignored opening should start after this.

    # return re.search(
    #     config.ignored_trans_blocks_closing,
    #     html[last_index:],
    #     flags=re.IGNORECASE | re.VERBOSE,
    # )


def is_ignored_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = tuple(
        re.finditer(
            config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
        )
    )

    if inline:
        last_index = (
            inline[-1].end()
        )  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            config.ignored_block_closing,
            item[last_index:],
            flags=re.IGNORECASE | re.VERBOSE,
        )
    )


def is_script_style_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = tuple(
        re.finditer(
            config.script_style_inline, item, flags=re.IGNORECASE | re.VERBOSE
        )
    )

    if inline:
        last_index = (
            inline[-1].end()
        )  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            config.script_style_closing,
            item[last_index:],
            flags=re.IGNORECASE | re.VERBOSE,
        )
    )


def is_safe_closing_tag(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = tuple(
        re.finditer(
            config.ignored_inline_blocks + r" | " + config.ignored_blocks,
            item,
            flags=re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL,
        )
    )

    if inline:
        last_index = (
            inline[-1].end()
        )  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            config.safe_closing_tag,
            item[last_index:],
            flags=re.IGNORECASE | re.VERBOSE,
        )
    )


def inside_template_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Check if a re.Match is inside of a template block."""
    return any(
        ignored_match.start(0) <= match.start()
        and match.end(0) <= ignored_match.end()
        for ignored_match in re.finditer(
            config.template_blocks,
            html,
            flags=re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
        )
    )


def inside_ignored_linter_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Check if a re.Match is inside of a ignored linter block."""
    return any(
        ignored_match.start(0) <= match.start()
        and match.end(0) <= ignored_match.end()
        for ignored_match in re.finditer(
            config.ignored_linter_blocks,
            html,
            flags=re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
        )
    )


def inside_ignored_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        ignored_match.start(0) <= match.start()
        and match.end(0) <= ignored_match.end()
        for ignored_match in itertools.chain(
            re.finditer(
                config.ignored_blocks,
                html,
                flags=re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
            ),
            re.finditer(
                config.ignored_inline_blocks,
                html,
                flags=re.IGNORECASE | re.VERBOSE,
            ),
        )
    )


def child_of_unformatted_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        ignored_match.start(0) < match.start()
        and match.end(0) <= ignored_match.end()
        for ignored_match in re.finditer(
            config.unformatted_blocks,
            html,
            flags=re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
        )
    )


def child_of_ignored_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        ignored_match.start(0) < match.start()
        and match.end(0) <= ignored_match.end()
        for ignored_match in itertools.chain(
            re.finditer(
                config.ignored_blocks,
                html,
                flags=re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
            ),
            re.finditer(
                config.ignored_inline_blocks,
                html,
                flags=re.IGNORECASE | re.VERBOSE,
            ),
        )
    )


def overlaps_ignored_block(
    config: Config, html: str, match: re.Match[str]
) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        # don't require the match to be fully inside the ignored block.
        # poorly build html will probably span ignored blocks and should be ignored.
        (
            ignored_match.start(0) <= match.start()
            and match.start() <= ignored_match.end()
        )
        or (
            ignored_match.start(0) <= match.end()
            and match.end() <= ignored_match.end()
        )
        for ignored_match in itertools.chain(
            re.finditer(
                config.ignored_blocks,
                html,
                flags=re.DOTALL
                | re.IGNORECASE
                | re.VERBOSE
                | re.MULTILINE
                | re.DOTALL,
            ),
            re.finditer(
                config.ignored_inline_blocks,
                html,
                flags=re.IGNORECASE | re.VERBOSE,
            ),
        )
    )


def inside_ignored_rule(
    config: Config, html: str, match: re.Match[str], rule: str
) -> bool:
    """Check if match is inside an ignored pattern."""
    for rule_regex in config.ignored_rules:
        for ignored_match in re.finditer(
            rule_regex, html, flags=re.DOTALL | re.IGNORECASE | re.VERBOSE
        ):
            if (
                rule in re.split(r"\s|,", ignored_match.group(1).strip())
                and (
                    ignored_match.start(0) <= match.start()
                    and match.start() <= ignored_match.end()
                )
            ) or (
                not ignored_match.group(1).strip()
                and (
                    ignored_match.start(0) <= match.end()
                    and match.end() <= ignored_match.end()
                )
            ):
                return True
    return False
