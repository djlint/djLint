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

        beautified = (
            "\n"
            + inner_indent
            + ("\n" + inner_indent).join(
                jsbeautifier.beautify(match.group(3), opts).splitlines()
            )
        )

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
