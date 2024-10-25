"""Test for blank line before tag.

--blank-line-before-tag 'include,load'

uv run pytest tests/test_config/test_blank_line_before_tag.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

test_data = [
    pytest.param(
        (
            '{% extends "nothing.html" %}{% load stuff %}{% load stuff 2 %}{% include "html_two.html" %}<div></div>'
        ),
        (
            '{% extends "nothing.html" %}\n'
            "\n"
            "{% load stuff %}\n"
            "{% load stuff 2 %}\n"
            "\n"
            '{% include "html_two.html" %}\n'
            "<div></div>\n"
        ),
        ({"blank_line_before_tag": "include,load, extends"}),
        id="one",
    ),
    pytest.param(
        (
            '<div class="tab-cnt">\n'
            '    <div class="tab-dta active" id="details">\n'
            '        <div class="em-grid">\n'
            '            {% include "pages/task/details_source.html.j2" %}\n'
            "\n"
            "        </div>\n"
            "    </div>\n"
            "</div>"
        ),
        (
            '<div class="tab-cnt">\n'
            '    <div class="tab-dta active" id="details">\n'
            '        <div class="em-grid">\n'
            "\n"
            '            {% include "pages/task/details_source.html.j2" %}\n'
            "        </div>\n"
            "    </div>\n"
            "</div>\n"
        ),
        ({"blank_line_before_tag": "include"}),
        id="blank_nested",
    ),
    pytest.param(
        ("{% block this %}\n{% load i18n %}\n{% endblock this %}"),
        ("{% block this %}\n\n    {% load i18n %}\n\n{% endblock this %}\n"),
        ({"blank_line_before_tag": "endblock  , junk,load "}),
        id="nested_indent",
    ),
    pytest.param(
        (
            "{% block include %}\n"
            "    {#    {% include 'common/sticky-topbar-hidden-nav.html' %}#}\n"
            "{% endblock %}\n"
        ),
        (
            "{% block include %}\n"
            "    {#    {% include 'common/sticky-topbar-hidden-nav.html' %}#}\n"
            "\n"
            "{% endblock %}\n"
        ),
        ({"blank_line_before_tag": "load, extends,endblock"}),
        id="test inside comment",
    ),
    pytest.param(
        (
            "{% blocktrans %}my words{% endblocktrans %}\n"
            "{% block body %}\n"
            "    <div></div>\n"
            "{% endblock body %}\n"
            "\n"
            "{% block js %}{% endblock %}"
        ),
        (
            "{% blocktrans %}my words{% endblocktrans %}\n"
            "{% block body %}\n"
            "    <div></div>\n"
            "\n"
            "{% endblock body %}\n"
            "{% block js %}{% endblock %}\n"
        ),
        ({"blank_line_before_tag": "endblock"}),
        id="endblock is not endblocktrans",
    ),
    pytest.param(
        ("{% extends nothing %}\n\n<div></div>\n"),
        ("{% extends nothing %}\n\n<div></div>\n"),
        ({
            "blank_line_before_tag": "load, extends",
            "preserve_blank_lines": True,
        }),
        id="option should work with preserve blank lines",
    ),
    pytest.param(
        (
            "{% block %}stuff{% endblock %}\n"
            "\n"
            "{% block %}stuff{% endblock %}\n"
            "\n"
        ),
        ("{% block %}stuff{% endblock %}\n{% block %}stuff{% endblock %}\n"),
        ({
            "blank_line_before_tag": "load, extends,     include     ,endblock "
        }),
        id="double block",
    ),
    pytest.param(
        (
            '{% include "pages/task/details/data_source.html.j2" %}\n'
            '{% include "pages/task/details/query_location.html.j2" %}\n'
            '{% include "pages/task/details/processing.html.j2" %}\n'
            '{% include "pages/task/details/destination.html.j2" %}\n'
        ),
        (
            '{% include "pages/task/details/data_source.html.j2" %}\n'
            '{% include "pages/task/details/query_location.html.j2" %}\n'
            '{% include "pages/task/details/processing.html.j2" %}\n'
            '{% include "pages/task/details/destination.html.j2" %}\n'
        ),
        ({"blank_line_before_tag": "   include     ,endblock "}),
        id="test multiple",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
