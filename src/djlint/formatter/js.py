"""djLint function to call jsbeautifier."""

from __future__ import annotations

from functools import partial
from io import StringIO
from typing import TYPE_CHECKING

import jsbeautifier
import regex as re
from jsbeautifier.javascript.options import BeautifierOptions

from djlint.helpers import RE_FLAGS_IS, RE_FLAGS_IMSX, child_of_unformatted_block

if TYPE_CHECKING:
    from djlint.settings import Config


def format_js(html: str, config: Config) -> str:
    """Format javascript inside <script> tags."""

    def launch_formatter(
        config: Config, html: str, match: re.Match[str]
    ) -> str:
        """Add break after if not in ignored block."""
        if child_of_unformatted_block(config, html, match):
            return match.group()

        if not match.group(3).strip():
            return match.group()

        script_content = match.group(3)
        indent = len(match.group(1)) * " "

        # Check for unformatted blocks within the script content
        unformatted_blocks = []
        for unformatted_match in re.finditer(
            config.unformatted_blocks, script_content, flags=RE_FLAGS_IMSX
        ):
            # Only consider non-empty matches
            if unformatted_match.group():
                unformatted_blocks.append(unformatted_match.span())

        # If there are no unformatted blocks within the script, format normally
        if not unformatted_blocks:
            # because of the param options for js-beautifier we cannot pass
            # in a fixed space leading.
            # so, call formatter twice, once with a fake indent.
            # check which lines changed (these are the formattable lines)
            # and add the leading space to them.

            config.js_config["indent_level"] = 1
            opts = BeautifierOptions(config.js_config)
            beautified_lines = jsbeautifier.beautify(
                script_content, opts
            ).splitlines()

            config.js_config["indent_level"] = 2
            opts = BeautifierOptions(config.js_config)
            beautified_lines_test = jsbeautifier.beautify(
                script_content, opts
            ).splitlines()

            with StringIO() as buf:
                for line, test in zip(beautified_lines, beautified_lines_test):
                    buf.write("\n")
                    if line != test:
                        buf.write(indent)
                    buf.write(line)
                beautified = buf.getvalue()

            return match.group(1) + match.group(2) + beautified + "\n" + indent

        # If there are unformatted blocks, we need to preserve them while formatting the rest
        result_parts = []
        last_end = 0

        for unformatted_start, unformatted_end in unformatted_blocks:
            # Format the content before this unformatted block
            if unformatted_start > last_end:
                formattable_content = script_content[last_end:unformatted_start]
                if formattable_content.strip():
                    config.js_config["indent_level"] = 1
                    opts = BeautifierOptions(config.js_config)
                    beautified_lines = jsbeautifier.beautify(
                        formattable_content, opts
                    ).splitlines()

                    config.js_config["indent_level"] = 2
                    opts = BeautifierOptions(config.js_config)
                    beautified_lines_test = jsbeautifier.beautify(
                        formattable_content, opts
                    ).splitlines()

                    with StringIO() as buf:
                        for line, test in zip(beautified_lines, beautified_lines_test):
                            buf.write("\n")
                            if line != test:
                                buf.write(indent)
                            buf.write(line)
                        formatted_part = buf.getvalue()
                    result_parts.append(formatted_part)
                else:
                    result_parts.append(formattable_content)

            # Preserve the unformatted block as-is
            unformatted_content = script_content[unformatted_start:unformatted_end]
            result_parts.append(unformatted_content)
            last_end = unformatted_end

        # Format any remaining content after the last unformatted block
        if last_end < len(script_content):
            remaining_content = script_content[last_end:]
            if remaining_content.strip():
                config.js_config["indent_level"] = 1
                opts = BeautifierOptions(config.js_config)
                beautified_lines = jsbeautifier.beautify(
                    remaining_content, opts
                ).splitlines()

                config.js_config["indent_level"] = 2
                opts = BeautifierOptions(config.js_config)
                beautified_lines_test = jsbeautifier.beautify(
                    remaining_content, opts
                ).splitlines()

                with StringIO() as buf:
                    for line, test in zip(beautified_lines, beautified_lines_test):
                        buf.write("\n")
                        if line != test:
                            buf.write(indent)
                        buf.write(line)
                    formatted_part = buf.getvalue()
                result_parts.append(formatted_part)
            else:
                result_parts.append(remaining_content)

        beautified = "".join(result_parts)
        return match.group(1) + match.group(2) + beautified + "\n" + indent

    func = partial(launch_formatter, config, html)

    return re.sub(
        r"([ ]*?)(<(?:script)\b(?:\"[^\"]*\"|'[^']*'|{[^}]*}|[^'\">{}])*>)(.*?)(?=</script>)",
        func,
        html,
        flags=RE_FLAGS_IS,
    )
