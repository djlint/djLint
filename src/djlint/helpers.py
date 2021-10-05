"""Collection of shared djLint functions."""
import regex as re

from .settings import Config


def is_ignored_group_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            re.compile(config.ignored_group_opening, re.IGNORECASE | re.VERBOSE),
            item[last_index:],
        )
    )


def is_ignored_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return bool(
        re.search(
            re.compile(config.ignored_block_opening, re.IGNORECASE | re.VERBOSE),
            item[last_index:],
        )
    )


def is_ignored_group_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            config.ignored_inline_blocks, item, flags=re.IGNORECASE | re.VERBOSE
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return (
        re.search(
            re.compile(config.ignored_group_opening, re.IGNORECASE | re.VERBOSE),
            item[last_index:],
        )
    ) or re.search(
        re.compile(config.ignored_block_opening, re.IGNORECASE | re.VERBOSE),
        item[last_index:],
    )


def is_ignored_group_closing(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            re.compile(config.ignored_inline_blocks, flags=re.IGNORECASE | re.VERBOSE),
            item,
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return re.search(
        re.compile(config.ignored_group_closing, flags=re.VERBOSE | re.IGNORECASE),
        item[last_index:],
    )


def is_ignored_group_block_closing(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            re.compile(config.ignored_inline_blocks, flags=re.IGNORECASE | re.VERBOSE),
            item,
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return (
        re.search(
            re.compile(config.ignored_group_closing, flags=re.VERBOSE | re.IGNORECASE),
            item[last_index:],
        )
    ) or re.search(
        re.compile(config.ignored_block_closing, flags=re.IGNORECASE | re.VERBOSE),
        item[last_index:],
    )


def is_ignored_block_closing(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            re.compile(config.ignored_inline_blocks, flags=re.IGNORECASE | re.VERBOSE),
            item,
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return re.search(
        re.compile(config.ignored_block_closing, flags=re.IGNORECASE | re.VERBOSE),
        item[last_index:],
    )
