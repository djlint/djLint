"""djLint function to call cssbeautifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint.formatter.beautifier import format_blocks, raw_text_block_pattern

if TYPE_CHECKING:
    from typing import Final

    from djlint.settings import Config


_STYLE_BLOCK_PATTERN: Final = raw_text_block_pattern("style")


def format_css(html: str, config: Config) -> str:
    """Format css inside <style> tags."""
    import cssbeautifier  # noqa: PLC0415
    from cssbeautifier.css.options import BeautifierOptions  # noqa: PLC0415

    return format_blocks(
        html,
        config,
        pattern=_STYLE_BLOCK_PATTERN,
        beautify=lambda source, options: cssbeautifier.beautify(
            source, BeautifierOptions(options)
        ),
        beautifier_config=config.css_config,
    )
