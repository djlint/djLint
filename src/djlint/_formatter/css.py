"""djLint function to call cssbeautifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cssbeautifier

from djlint._formatter.beautifier import format_blocks, raw_text_block_pattern

if TYPE_CHECKING:
    from typing import Final

    from djlint._settings import Config


_STYLE_BLOCK_PATTERN: Final = raw_text_block_pattern("style")


def format_css(html: str, config: Config) -> str:
    """Format css inside <style> tags."""
    return format_blocks(
        html,
        config,
        pattern=_STYLE_BLOCK_PATTERN,
        beautify=cssbeautifier.beautify,
        beautifier_config=config.css_config,
    )
