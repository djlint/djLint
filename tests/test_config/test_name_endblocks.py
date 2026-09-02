"""Test name_endblocks.

uv run pytest tests/test_config/test_name_endblocks.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        "{% block name %}\n   {% include 'header.twig' %}\n{% endblock %}\n",
        '{% block name %}\n    {% include "header.twig" %}\n{% endblock name %}\n',
        id="issue 475",
    ),
    pytest.param(
        "{% block a %}x{% endblock %}\n",
        "{% block a %}x{% endblock %}\n",
        id="a block closed on its own line says which it is",
    ),
    pytest.param(
        "{% block outer %}\n{% block inner %}\nx\n{% endblock %}\n{% endblock %}\n",
        (
            "{% block outer %}\n"
            "    {% block inner %}\n"
            "        x\n"
            "    {% endblock inner %}\n"
            "{% endblock outer %}\n"
        ),
        id="each name reaches the tag that closes it",
    ),
    pytest.param(
        "{%- block a -%}\nx\n{%- endblock -%}\n",
        "{%- block a -%}\n    x\n{%- endblock a -%}\n",
        id="whitespace control is left as written",
    ),
    pytest.param(
        "{% block %}\nx\n{% endblock %}\n",
        "{% block %}\n    x\n{% endblock %}\n",
        id="a block with no name has none to copy",
    ),
    pytest.param(
        "{% raw %}\n{% block a %}\nx\n{% endblock %}\n{% endraw %}\n",
        "{% raw %}\n    {% block a %}\n        x\n    {% endblock %}\n{% endraw %}\n",
        id="a block shown as text opens nothing",
    ),
    pytest.param(
        "{% blocktrans %}\nx\n{% endblocktrans %}\n",
        "{% blocktrans %}\nx\n{% endblocktrans %}\n",
        id="blocktrans is not a block",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str) -> None:
    config = config_builder({"name_endblocks": True, "profile": "django"})
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output


def test_default_leaves_the_endblock_bare() -> None:
    config = config_builder({"profile": "django"})
    output = formatter(config, "{% block a %}\nx\n{% endblock %}\n")

    assert output == "{% block a %}\n    x\n{% endblock %}\n"


def test_the_formatter_clears_t003() -> None:
    config = config_builder({
        "name_endblocks": True,
        "profile": "django",
        "include": "T003",
    })
    output = formatter(config, "{% block a %}\nx\n{% endblock %}\n")
    findings = linter(config, output, "a.html", "a.html")

    assert not [f for v in findings.values() for f in v if f["code"] == "T003"]
