"""djLint function to call cssbeautifier."""

from __future__ import annotations

from functools import partial
from io import StringIO
from typing import TYPE_CHECKING

import regex as re

from djlint.helpers import (
    RE_FLAGS_IS,
    child_of_unformatted_block,
    mask_template_tags,
    restore_template_tags,
)

if TYPE_CHECKING:
    from djlint.settings import Config


def format_css(html: str, config: Config) -> str:
    """Format css inside <style> tags."""
    import cssbeautifier  # noqa: PLC0415
    from cssbeautifier.css.options import BeautifierOptions  # noqa: PLC0415

    def launch_formatter(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        """Add break after if not in ignored block."""
        if child_of_unformatted_block(config, html, match):
            return match.group()

        if not match.group(3).strip():
            return match.group()

        indent = len(match.group(1)) * " "

        # because of the param options for css-beautifier we cannot pass
        # in a fixed space leading.
        # so, call formatter twice, once with a fake indent.
        # check which lines changed (these are the formattable lines)
        # and add the leading space to them.

        css, replacements = mask_template_tags(config, match.group(3))

        config.css_config["indent_level"] = 1
        opts = BeautifierOptions(config.css_config)
        beautified_lines = cssbeautifier.beautify(css, opts).splitlines()

        config.css_config["indent_level"] = 2
        opts = BeautifierOptions(config.css_config)
        beautified_lines_test = cssbeautifier.beautify(css, opts).splitlines()

        with StringIO() as buf:
            for line, test in zip(
                beautified_lines, beautified_lines_test, strict=False
            ):
                buf.write("\n")
                if line != test:
                    buf.write(indent)
                buf.write(line)
            beautified = buf.getvalue()
            for marker, _ in replacements:
                beautified = re.sub(
                    rf"\n[ \t]*\n([ \t]*/\*{re.escape(marker)}\*/[ \t]*(?=\n|$))",
                    r"\n\1",
                    beautified,
                )
            beautified = restore_template_tags(beautified, replacements)

        return match.group(1) + match.group(2) + beautified + "\n" + indent

    func = partial(launch_formatter, config, html)

    return re.sub(
        r"([ ]*?)(<(?:style)\b(?:\"[^\"]*\"|'[^']*'|{[^}]*}|[^'\">{}])*>)(.*?)(?=</style>)",
        func,
        html,
        flags=RE_FLAGS_IS,
    )
