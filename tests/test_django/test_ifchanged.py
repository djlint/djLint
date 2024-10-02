"""Test django ifchanged tag.

uv run pytest tests/test_django/test_ifchanged.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import printer

if TYPE_CHECKING:
    from djlint.settings import Config

test_data = [
    pytest.param(
        (
            '{% for match in matches %}<div style="background-color:"pink">{% ifchanged match.ballot_id %}{% cycle "red" "blue" %}{% else %}gray{% endifchanged %}{{ match }}</div>{% endfor %}'
        ),
        (
            "{% for match in matches %}\n"
            '    <div style="background-color:"pink">\n'
            "        {% ifchanged match.ballot_id %}\n"
            '            {% cycle "red" "blue" %}\n'
            "        {% else %}\n"
            "            gray\n"
            "        {% endifchanged %}\n"
            "        {{ match }}\n"
            "    </div>\n"
            "{% endfor %}\n"
        ),
        id="ifchanged_tag",
    )
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
