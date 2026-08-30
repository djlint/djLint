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
        ("{% block this %}\n    {% load i18n %}\n\n{% endblock this %}\n"),
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
            "{% set first = 1 %}\n"
            "{# comment about second #}\n"
            "{% set second = 2 %}"
        ),
        (
            "{% set first = 1 %}\n"
            "\n"
            "{# comment about second #}\n"
            "{% set second = 2 %}\n"
        ),
        ({"blank_line_before_tag": "set"}),
        id="issue_744_blank_line_above_comment",
    ),
    pytest.param(
        (
            "{% set first = 1 %}\n"
            "\n"
            "{# comment about second #}\n"
            "{% set second = 2 %}"
        ),
        (
            "{% set first = 1 %}\n"
            "\n"
            "{# comment about second #}\n"
            "{% set second = 2 %}\n"
        ),
        ({"blank_line_before_tag": "set"}),
        id="issue_744_comment_stays_attached_roundtrip",
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
    pytest.param(
        (
            "{% block content %}\n"
            '<div id="panel">\n'
            "{% block panel %}\n"
            "{% endblock panel %}\n"
            "</div>\n"
            "{% endblock content %}\n"
            "{% block extra_css %}\n"
            "{% block workflow_css %}\n"
            "{% endblock workflow_css %}\n"
            "{% endblock extra_css %}\n"
        ),
        (
            "{% block content %}\n"
            '    <div id="panel">\n'
            "        {% block panel %}\n"
            "        {% endblock panel %}\n"
            "    </div>\n"
            "{% endblock content %}\n"
            "\n"
            "{% block extra_css %}\n"
            "    {% block workflow_css %}\n"
            "    {% endblock workflow_css %}\n"
            "{% endblock extra_css %}\n"
        ),
        ({
            "blank_line_before_tag": "block",
            "blank_line_after_tag": "endblock",
        }),
        id="issue_2317_no_blank_line_after_increased_indent",
    ),
    pytest.param(
        (
            '<img src="a.png">\n'
            '{% include "x.html" %}\n'
            "<div></div>\n"
            '{% include "y.html" %}\n'
            "<span>text</span>\n"
            '{% include "z.html" %}\n'
        ),
        (
            '<img src="a.png">\n'
            "\n"
            '{% include "x.html" %}\n'
            "<div></div>\n"
            "\n"
            '{% include "y.html" %}\n'
            "<span>text</span>\n"
            "\n"
            '{% include "z.html" %}\n'
        ),
        ({"blank_line_before_tag": "include"}),
        id="a line that opens nothing is a sibling",
    ),
    pytest.param(
        (
            "<p>before macro</p>\n"
            "{%- macro Foo() -%}\n"
            "  <div>foo</div>\n"
            "{%- endmacro -%}\n"
        ),
        (
            "<p>before macro</p>\n"
            "\n"
            "{%- macro Foo() -%}\n"
            "    <div>foo</div>\n"
            "{%- endmacro -%}\n"
        ),
        ({"blank_line_before_tag": "macro"}),
        id="nunjucks whitespace control dash - before",
    ),
    pytest.param(
        ("<p>before</p>\n{% macro Foo() %}\n<div>foo</div>\n{% endmacro %}\n"),
        (
            "<p>before</p>\n"
            "\n"
            "{% macro Foo() %}\n"
            "    <div>foo</div>\n"
            "{% endmacro %}\n"
        ),
        ({"blank_line_before_tag": "macro, ,"}),
        id="blank entries are dropped",
    ),
    pytest.param(
        (
            '<svg viewBox="0 0 24 24">\n'
            '    <path d="\n'
            "    {% block p %}\n"
            "    {% endblock p %}\n"
            '    " />\n'
            "</svg>\n"
        ),
        (
            '<svg viewBox="0 0 24 24">\n'
            '    <path d="\n'
            "    {% block p %}\n"
            "    {% endblock p %}\n"
            '    " />\n'
            "</svg>\n"
        ),
        ({"blank_line_before_tag": "block", "profile": "django"}),
        id="no blank line inside an attribute value",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    config = config_builder(args)
    output = formatter(config, source)

    printer(expected, source, output)
    assert expected == output
    assert expected == formatter(config, output)
