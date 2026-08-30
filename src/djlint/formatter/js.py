"""djLint function to call jsbeautifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.formatter.beautifier import format_blocks, raw_text_block_pattern

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_SCRIPT_BLOCK_PATTERN: Final = raw_text_block_pattern("script")


def format_js(html: str, config: Config) -> str:
    """Format javascript inside <script> tags."""
    import jsbeautifier  # noqa: PLC0415
    from jsbeautifier.javascript.options import (  # noqa: PLC0415
        BeautifierOptions,
    )

    return format_blocks(
        html,
        config,
        pattern=_SCRIPT_BLOCK_PATTERN,
        beautify=lambda source, options: jsbeautifier.beautify(
            source, BeautifierOptions(options)
        ),
        beautifier_config=config.js_config,
    )
