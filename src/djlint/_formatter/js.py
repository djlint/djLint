"""djLint function to call jsbeautifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

import jsbeautifier

from djlint._formatter.beautifier import format_blocks, raw_text_block_pattern
from djlint._formatter.tokenizer import tokenize_tags

if TYPE_CHECKING:
    from typing import Final

    from djlint._settings import Config


_SCRIPT_BLOCK_PATTERN: Final = raw_text_block_pattern("script")

# The types a browser runs as javascript, those it reads as json, and the
# jsx that babel runs in the browser. Any other type makes the element a data
# block, such as a client side template written in html, which the beautifier
# would take apart as javascript.
_CODE_TYPES: Final = frozenset((
    "",
    "module",
    "importmap",
    "speculationrules",
    "application/json",
    "application/ecmascript",
    "application/javascript",
    "application/x-ecmascript",
    "application/x-javascript",
    "text/babel",
    "text/ecmascript",
    "text/javascript",
    "text/javascript1.0",
    "text/javascript1.1",
    "text/javascript1.2",
    "text/javascript1.3",
    "text/javascript1.4",
    "text/javascript1.5",
    "text/jscript",
    "text/json",
    "text/jsx",
    "text/livescript",
    "text/x-ecmascript",
    "text/x-javascript",
))


def _holds_code(config: Config, opening_tag: str) -> bool:
    """Whether the script's type is one the beautifier can read.

    A browser reads the first type written. One a template tag writes may
    be anything, so the script is left alone.
    """
    token = next(tokenize_tags(opening_tag), None)
    if token is None:
        return False
    for attribute in config.attribute_pattern.finditer(
        opening_tag, token.name_end, token.attributes_end
    ):
        name, value = attribute.group(1, 2)
        if name and name.lower() == "type":
            script_type = (value or "").strip("\"'").strip().lower()
            return "{" not in script_type and (
                script_type in _CODE_TYPES or script_type.endswith("+json")
            )
    return True


def format_js(html: str, config: Config) -> str:
    """Format javascript inside <script> tags."""
    return format_blocks(
        html,
        config,
        pattern=_SCRIPT_BLOCK_PATTERN,
        beautify=jsbeautifier.beautify,
        beautifier_config=config.js_config,
        holds_code=lambda opening_tag: _holds_code(config, opening_tag),
    )
