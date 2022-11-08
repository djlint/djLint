"""djLint function to call jsbeautifier."""
from functools import partial

import jsbeautifier
import regex as re
from jsbeautifier.javascript.options import BeautifierOptions

from ..settings import Config


def format_js(html: str, config: Config) -> str:
    """Format javascript inside <script> tags."""

    def launch_formatter(config: Config, match: re.Match) -> str:
        """Add break after if not in ignored block."""
        if not match.group(3).strip():
            return match.group()

        indent = len(match.group(1)) * " "
        inner_indent = indent + config.indent

        opts = BeautifierOptions(config.js_config)

        beautified_lines = jsbeautifier.beautify(match.group(3), opts).splitlines()
        beautified = ""

        # add indent back
        ignore_indent = False
        for line in beautified_lines:

            if re.search(
                re.compile(
                    r"\/\*[ ]*?beautify[ ]+?(?:preserve|ignore):end[ ]*?\*\/",
                    re.DOTALL | re.IGNORECASE | re.MULTILINE,
                ),
                line,
            ):
                line = line.lstrip()
                ignore_indent = False

            if ignore_indent is False and line:
                beautified += "\n" + inner_indent + line

            else:
                beautified += "\n" + line

            if re.search(
                re.compile(
                    r"\/\*[ ]*?beautify[ ]+?(?:preserve|ignore):start[ ]*?\*\/",
                    re.DOTALL | re.IGNORECASE | re.MULTILINE,
                ),
                line,
            ):
                ignore_indent = True

        return match.group(1) + match.group(2) + beautified + "\n" + indent

    func = partial(launch_formatter, config)

    return re.sub(
        re.compile(
            r"([ ]*?)(<(?:script)\b(?:\"[^\"]*\"|'[^']*'|{[^}]*}|[^'\">{}])*>)(.*?)(?=</script>)",
            re.IGNORECASE | re.DOTALL,
        ),
        func,
        html,
    )
