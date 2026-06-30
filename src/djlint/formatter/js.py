"""djLint function to call jsbeautifier."""

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


def format_js(html: str, config: Config) -> str:
    """Format javascript inside <script> tags."""
    import jsbeautifier  # noqa: PLC0415
    from jsbeautifier.javascript.options import (  # noqa: PLC0415
        BeautifierOptions,
    )

    def launch_formatter(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        """Add break after if not in ignored block."""
        if child_of_unformatted_block(config, html, match):
            return match.group()

        if not match.group(3).strip():
            return match.group()

        indent = len(match.group(1)) * " "

        # because of the param options for js-beautifier we cannot pass
        # in a fixed space leading.
        # so, call formatter twice, once with a fake indent.
        # check which lines changed (these are the formattable lines)
        # and add the leading space to them.

        js, replacements = mask_template_tags(config, match.group(3))

        config.js_config["indent_level"] = 1
        opts = BeautifierOptions(config.js_config)
        beautified_lines = jsbeautifier.beautify(js, opts).splitlines()

        config.js_config["indent_level"] = 2
        opts = BeautifierOptions(config.js_config)
        beautified_lines_test = jsbeautifier.beautify(js, opts).splitlines()

        with StringIO() as buf:
            for line, test in zip(
                beautified_lines, beautified_lines_test, strict=False
            ):
                buf.write("\n")
                if line != test:
                    buf.write(indent)
                buf.write(line)
            beautified = restore_template_tags(buf.getvalue(), replacements)

        return match.group(1) + match.group(2) + beautified + "\n" + indent

    func = partial(launch_formatter, config, html)

    return re.sub(
        r"([ ]*?)(<(?:script)\b(?:\"[^\"]*\"|'[^']*'|{[^}]*}|[^'\">{}])*>)(.*?)(?=</script>)",
        func,
        html,
        flags=RE_FLAGS_IS,
    )
