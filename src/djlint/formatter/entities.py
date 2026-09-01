"""Write entity references as the characters they name."""

from __future__ import annotations

from html import unescape
from typing import TYPE_CHECKING

from djlint.helpers import inside_ignored_block, inside_template_block

if TYPE_CHECKING:
    import regex as re

    from djlint.settings import Config


def format_entities(html: str, config: Config) -> str:
    """Replace an entity reference with the character it names.

    The entities left alone are the ones that have to survive: `&lt;`,
    `&amp;` and the rest carry syntax, and an invisible one such as
    `&zwnj;` cannot be reviewed as a literal. That is the same set `H023`
    allows, and the pattern is shared with it. An entity naming nothing,
    such as the misspelled `&mdsah;`, is left as written for the rule to
    go on reporting.

    One written inside a template tag is not html text but part of the
    tag, so `{% trans "a &mdash; b" %}` keeps the translation key it was
    written with, as the rule already leaves it alone.
    """
    if config.no_entity_formatting or config.entity_pattern is None:
        return html

    def replace(match: re.Match[str]) -> str:
        if inside_ignored_block(config, html, match) or inside_template_block(
            config, html, match
        ):
            return match.group()
        character = unescape(match.group())
        return match.group() if character == match.group() else character

    return config.entity_pattern.sub(replace, html)
