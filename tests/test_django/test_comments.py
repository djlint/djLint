"""Test django comment tag.

uv run pytest tests/test_django/test_comments.py
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
        ("{# comment #}{% if this %}<div></div>{% endif %}"),
        ("{# comment #}\n{% if this %}<div></div>{% endif %}\n"),
        id="dj_comments_tag",
    ),
    pytest.param(
        ('{% comment "Optional note" %}{{ body }}{% endcomment %}'),
        ('{% comment "Optional note" %}{{ body }}{% endcomment %}\n'),
        id="multi_line",
    ),
    pytest.param(
        (
            '<div class="hi">\n'
            '    <div class="poor">\n'
            '        <p class="format">\n'
            "            Lorem ipsum dolor\n"
            '            <span class="bold">sit</span>\n'
            "            amet\n"
            "        </p>\n"
            '        <img src="./pic.jpg">\n'
            "    </div>\n"
            '    <script src="file1.js"></script>\n'
            '    {% comment %} <script src="file2.js"></script>\n'
            '    <script src="file3.js"></script> {% endcomment %}\n'
            '    <script src="file4.js"></script>\n'
            "</div>"
        ),
        (
            '<div class="hi">\n'
            '    <div class="poor">\n'
            '        <p class="format">\n'
            "            Lorem ipsum dolor\n"
            '            <span class="bold">sit</span>\n'
            "            amet\n"
            "        </p>\n"
            '        <img src="./pic.jpg">\n'
            "    </div>\n"
            '    <script src="file1.js"></script>\n'
            '    {% comment %} <script src="file2.js"></script>\n'
            '    <script src="file3.js"></script> {% endcomment %}\n'
            '    <script src="file4.js"></script>\n'
            "</div>\n"
        ),
        id="nested_multi_line",
    ),
    pytest.param(
        (
            '<div class="hi">\n'
            '    <div class="poor">\n'
            "        {# djlint:off #}\n"
            '        <p class="format">\n'
            '            Lorem ipsum dolor <span class="bold">sit</span> amet\n'
            "        </p>\n"
            "        {# djlint:on #}\n"
            '        <img src="./pic.jpg">\n'
            "    </div>\n"
            "    <ul>\n"
            "        {% for i in items %}\n"
            "            <li>item {{i}}</li>\n"
            "            {% if i > 10 %}{% endif %}\n"
            "            <li>item {{i}}</li>\n"
            "        {% endfor %}\n"
            "    </ul>\n"
            "</div>"
        ),
        (
            '<div class="hi">\n'
            '    <div class="poor">\n'
            "        {# djlint:off #}\n"
            '        <p class="format">\n'
            '            Lorem ipsum dolor <span class="bold">sit</span> amet\n'
            "        </p>\n"
            "        {# djlint:on #}\n"
            '        <img src="./pic.jpg">\n'
            "    </div>\n"
            "    <ul>\n"
            "        {% for i in items %}\n"
            "            <li>item {{ i }}</li>\n"
            "            {% if i > 10 %}{% endif %}\n"
            "            <li>item {{ i }}</li>\n"
            "        {% endfor %}\n"
            "    </ul>\n"
            "</div>\n"
        ),
        id="djlint_comment",
    ),
    pytest.param(
        (
            "<html>\n"
            "    <head>\n"
            '        <script src="file1.js"></script>\n'
            "        {% comment %}\n"
            '        <script src="file2.js"></script>\n'
            '        <script src="file3.js"></script>\n'
            '        <script src="file4.js"></script>\n'
            "        {% endcomment %}\n"
            '        <script src="file5.js"></script>\n'
            "    </head>\n"
            "    <body></body>\n"
            "</html>"
        ),
        (
            "<html>\n"
            "    <head>\n"
            '        <script src="file1.js"></script>\n'
            "        {% comment %}\n"
            '        <script src="file2.js"></script>\n'
            '        <script src="file3.js"></script>\n'
            '        <script src="file4.js"></script>\n'
            "        {% endcomment %}\n"
            '        <script src="file5.js"></script>\n'
            "    </head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        id="comment_around_script",
    ),
    pytest.param(
        ("{# <div></div> #}\n{% if this %}<div></div>{% endif %}"),
        ("{# <div></div> #}\n{% if this %}<div></div>{% endif %}\n"),
        id="inline_comment",
    ),
    pytest.param(
        (
            "<div>\n"
            "    {% if 1 %}\n"
            '        <div class="{% if 1 %}class {% else %} class {% endif %}">\n'
            '            <div class="class"\n'
            '                 data-parameters="{#?@ViewBag.DefaultFilters#}"\n'
            '                 data-target="profile-{{ profile_type }}-{{ profile_id }}"></div>\n'
            "        </div>\n"
            "    {% endif %}"
        ),
        (
            "<div>\n"
            "    {% if 1 %}\n"
            '        <div class="{% if 1 %}class {% else %} class {% endif %}">\n'
            '            <div class="class"\n'
            '                 data-parameters="{#?@ViewBag.DefaultFilters#}"\n'
            '                 data-target="profile-{{ profile_type }}-{{ profile_id }}"></div>\n'
            "        </div>\n"
            "    {% endif %}\n"
        ),
        id="nested_inline_comment",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source: str, expected: str, django_config: Config) -> None:
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
