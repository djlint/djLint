"""Collection of shared djLint functions."""
import regex as re

from .settings import Config


def is_ignored_block_opening(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            config.ignored_blocks,
            item,
            flags=re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL,
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


def is_ignored_block_closing(config: Config, item: str) -> bool:
    """Find ignored group closing.

    A valid ignored group closing tag will not be part of a
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


def is_safe_closing_tag(config: Config, item: str) -> bool:
    """Find ignored group opening.

    A valid ignored group opening tag will not be part of a
    single line block.
    """
    last_index = 0
    inline = list(
        re.finditer(
            re.compile(
                config.ignored_inline_blocks + r" | " + config.ignored_blocks,
                flags=re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL,
            ),
            item,
        )
    )

    if inline:
        last_index = inline[
            -1
        ].end()  # get the last index. The ignored opening should start after this.

    return re.search(
        re.compile(config.safe_closing_tag, flags=re.IGNORECASE | re.VERBOSE),
        item[last_index:],
    )


def inside_template_block(config: Config, html: str, match: re.Match) -> bool:
    """Check if a re.Match is inside of a template block."""
    return any(
        ignored_match.start(0) <= match.start() and match.end(0) <= ignored_match.end()
        for ignored_match in list(
            re.finditer(
                re.compile(
                    config.template_blocks,
                    re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
                ),
                html,
            )
        )
    )


def inside_ignored_block(config: Config, html: str, match: re.Match) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        ignored_match.start(0) <= match.start() and match.end(0) <= ignored_match.end()
        for ignored_match in list(
            re.finditer(
                re.compile(
                    config.ignored_blocks,
                    re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
                ),
                html,
            )
        )
        + list(
            re.finditer(
                re.compile(config.ignored_inline_blocks, re.IGNORECASE | re.VERBOSE),
                html,
            )
        )
    )


def child_of_ignored_block(config: Config, html: str, match: re.Match) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        ignored_match.start(0) < match.start() and match.end(0) <= ignored_match.end()
        for ignored_match in list(
            re.finditer(
                re.compile(
                    config.ignored_blocks,
                    re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE,
                ),
                html,
            )
        )
        + list(
            re.finditer(
                re.compile(config.ignored_inline_blocks, re.IGNORECASE | re.VERBOSE),
                html,
            )
        )
    )


def overlaps_ignored_block(config: Config, html: str, match: re.Match) -> bool:
    """Do not add whitespace if the tag is in a non indent block."""
    return any(
        # don't require the match to be fully inside the ignored block.
        # poorly build html will probably span ignored blocks and should be ignored.
        (
            ignored_match.start(0) <= match.start()
            and match.start() <= ignored_match.end()
        )
        or (
            ignored_match.start(0) <= match.end() and match.end() <= ignored_match.end()
        )
        for ignored_match in list(
            re.finditer(
                re.compile(
                    config.ignored_blocks,
                    re.DOTALL | re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL,
                ),
                html,
            )
        )
        + list(
            re.finditer(
                re.compile(config.ignored_inline_blocks, re.IGNORECASE | re.VERBOSE),
                html,
            )
        )
    )


def inside_ignored_rule(config: Config, html: str, match: re.Match, rule: str) -> bool:
    """Check if match is inside an ignored pattern."""
    for rule_regex in config.ignored_rules:
        for ignored_match in list(
            re.finditer(
                re.compile(rule_regex, re.DOTALL | re.IGNORECASE | re.VERBOSE),
                html,
            )
        ):
            if (
                rule in list(set(re.split(r"\s|,", ignored_match.group(1).strip())))
                and (
                    ignored_match.start(0) <= match.start()
                    and match.start() <= ignored_match.end()
                )
                or (
                    ignored_match.start(0) <= match.end()
                    and match.end() <= ignored_match.end()
                )
            ):
                return True
    return False
