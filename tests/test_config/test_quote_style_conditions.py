"""Test quote_style inside template conditions.

uv run pytest tests/test_config/test_quote_style_conditions.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "{% if abc == '101' %}{% endif %}\n",
        '{% if abc == "101" %}{% endif %}\n',
        "double",
        id="a condition takes the configured quote (issue 262)",
    ),
    pytest.param(
        '{% if abc == "101" %}{% endif %}\n',
        "{% if abc == '101' %}{% endif %}\n",
        "single",
        id="and the other way round",
    ),
    pytest.param(
        "{% if a %}{% elif b == 'x' %}{% endif %}\n",
        '{% if a %}\n{% elif b == "x" %}\n{% endif %}\n',
        "double",
        id="a branch is a condition too",
    ),
    pytest.param(
        "{% if a == 'say \"hi\"' %}{% endif %}\n",
        "{% if a == 'say \"hi\"' %}{% endif %}\n",
        "double",
        id="a string holding the wanted quote is left as written",
    ),
    pytest.param(
        "{% trans 'it\\'s' %}\n",
        '{% trans "it\'s" %}\n',
        "double",
        id="an escaped quote loses the backslash it no longer needs",
    ),
    pytest.param(
        "<div class=\"{% if x == 'a' %}y{% endif %}\"></div>\n",
        "<div class=\"{% if x == 'a' %}y{% endif %}\"></div>\n",
        "double",
        id="inside an attribute the attribute's own quotes decide",
    ),
    pytest.param(
        "{% raw %}{% if x == 'a' %}{% endraw %}\n",
        "{% raw %}\n    {% if x == 'a' %}\n    {% endraw %}\n",
        "double",
        id="a tag shown as text keeps the quotes it is shown with",
    ),
    pytest.param(
        "{% verbatim %}{% include 'a.html' %}{% endverbatim %}\n",
        "{% verbatim %}\n    {% include 'a.html' %}\n{% endverbatim %}\n",
        "double",
        id="and so does one inside verbatim",
    ),
]


@pytest.mark.parametrize(("source", "expected", "quote_style"), test_data)
def test_base(source: str, expected: str, quote_style: str) -> None:
    config = config_builder({"profile": "jinja", "quote_style": quote_style})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
