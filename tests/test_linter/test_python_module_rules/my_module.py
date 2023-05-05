"""Test module for custom rules."""
import re
from typing import Any, Dict, List

from djlint.lint import get_line
from djlint.settings import Config


def run(
    rule: Dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: List[Dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> List[Dict[str, str]]:
    """Rule that fails if if the html file contains 'bad'.

    In the real world, this should be done with a simple regex rule.
    """
    errors: List[Dict[str, str]] = []
    for match in re.finditer(r"bad", html):
        errors.append(
            {
                "code": rule["name"],
                "line": get_line(match.start(), line_ends),
                "match": match.group().strip()[:20],
                "message": rule["message"],
            }
        )
    return errors
