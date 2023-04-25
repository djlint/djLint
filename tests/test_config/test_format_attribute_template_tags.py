"""Test for format attribute template tags.

--format-attribute-template-tags

poetry run pytest tests/test_config/test_format_attribute_template_tags.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            "<!-- list of good and complex attribute patterns -->\n"
            '<input class="{% if this %}\n'
            "                  then something neat\n"
            "              {% else %}\n"
            "                  that is long stuff asdf and more even\n"
            '              {% endif %}" />\n'
            '<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96" }}{% else %}{% static \'/img/report_thumb_placeholder_400x300.png\' %}{% endif %}"\n'
            "     src=\"{% static '/img/loader.gif' %}\"\n"
            '     alt="report image" />\n'
            '<a class="asdf\n'
            '          {% if favorite == "yes" %}favorite{% endif %}\n'
            '          has-tooltip-arrow has-tooltip-right"\n'
            '   data-tooltip="{% if favorite == "yes" %}\n'
            "                     Remove from Favorites\n"
            "                 {% else %}\n"
            "                     Add to Favorites\n"
            '                 {% endif %}"\n'
            '   fav-type="report"\n'
            '   object-id="{{ report.report_id }}"\n'
            '   href="{% if %}{% endif %}">\n'
            '    <span class="icon has-text-grey is-large">\n'
            '        <i class="fas fa-lg fa-star"></i>\n'
            "    </span>\n"
            "</a>\n"
            '<div class="media-content"\n'
            "     {% ifchanged comment.stream_id %}\n"
            "         comments-msg\n"
            "     {% else %}\n"
            "         comments-newMsgReply\n"
            "     {% endifchanged %}></div>\n"
            '<a class="piwik_download"\n'
            '   href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}"></a>\n'
            "<span {% if a %}required{% endif %}\n"
            '      title="{% if eev.status == eev.STATUS_CURRENT %}\n'
            "                 {% trans 'A' %}\n"
            "             {% elif eev.status == eev.STATUS_APPROVED %}\n"
            "                 {% trans 'B' %}\n"
            "             {% elif eev.status == eev.STATUS_EXPIRED %}\n"
            "                 {% trans 'C' %}\n"
            '             {% endif %}"\n'
            '      class="asdf\n'
            "             {% if a %}b{% endif %}\n"
            '             asdf"\n'
            "      {% if a %}checked{% endif %}></span>\n"
            "{% block body %}\n"
            '    <form action="{% if gpg -%}asdf something pretty long. can\'t beat this length{%- endif %}"\n'
            '          method="POST">\n'
            "    </form>\n"
            "{% endblock body %}\n"
            '<ul class="menu-list\n'
            "           {% for child in entry.children %}\n"
            "               {% if child.url== page.url %}\n"
            "                   is-active\n"
            "               {% else %}\n"
            "                   not-active\n"
            "               {% endif %}\n"
            "           {% endfor %}\n"
            '           is-collapsible">\n'
            "</ul>\n"
            '<div {% if true %}class="test"{% endif %}\n'
            '     {% include "django/forms/widgets/attrs.html" %}></div>\n'
        ),
        (
            "<!-- list of good and complex attribute patterns -->\n"
            '<input class="{% if this %}\n'
            "                  then something neat\n"
            "              {% else %}\n"
            "                  that is long stuff asdf and more even\n"
            '              {% endif %}" />\n'
            '<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96" }}{% else %}{% static \'/img/report_thumb_placeholder_400x300.png\' %}{% endif %}"\n'
            "     src=\"{% static '/img/loader.gif' %}\"\n"
            '     alt="report image" />\n'
            '<a class="asdf\n'
            '          {% if favorite == "yes" %}favorite{% endif %}\n'
            '          has-tooltip-arrow has-tooltip-right"\n'
            '   data-tooltip="{% if favorite == "yes" %}\n'
            "                     Remove from Favorites\n"
            "                 {% else %}\n"
            "                     Add to Favorites\n"
            '                 {% endif %}"\n'
            '   fav-type="report"\n'
            '   object-id="{{ report.report_id }}"\n'
            '   href="{% if %}{% endif %}">\n'
            '    <span class="icon has-text-grey is-large">\n'
            '        <i class="fas fa-lg fa-star"></i>\n'
            "    </span>\n"
            "</a>\n"
            '<div class="media-content"\n'
            "     {% ifchanged comment.stream_id %}\n"
            "         comments-msg\n"
            "     {% else %}\n"
            "         comments-newMsgReply\n"
            "     {% endifchanged %}></div>\n"
            '<a class="piwik_download"\n'
            '   href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}"></a>\n'
            "<span {% if a %}required{% endif %}\n"
            '      title="{% if eev.status == eev.STATUS_CURRENT %}\n'
            "                 {% trans 'A' %}\n"
            "             {% elif eev.status == eev.STATUS_APPROVED %}\n"
            "                 {% trans 'B' %}\n"
            "             {% elif eev.status == eev.STATUS_EXPIRED %}\n"
            "                 {% trans 'C' %}\n"
            '             {% endif %}"\n'
            '      class="asdf\n'
            "             {% if a %}b{% endif %}\n"
            '             asdf"\n'
            "      {% if a %}checked{% endif %}></span>\n"
            "{% block body %}\n"
            '    <form action="{% if gpg -%}asdf something pretty long. can\'t beat this length{%- endif %}"\n'
            '          method="POST">\n'
            "    </form>\n"
            "{% endblock body %}\n"
            '<ul class="menu-list\n'
            "           {% for child in entry.children %}\n"
            "               {% if child.url== page.url %}\n"
            "                   is-active\n"
            "               {% else %}\n"
            "                   not-active\n"
            "               {% endif %}\n"
            "           {% endfor %}\n"
            '           is-collapsible">\n'
            "</ul>\n"
            '<div {% if true %}class="test"{% endif %}\n'
            '     {% include "django/forms/widgets/attrs.html" %}></div>\n'
        ),
        ({"format_attribute_template_tags": True}),
        id="one",
    ),
    pytest.param(
        (
            '<input class="{% if this %}then something neat{% else %}that is long stuff asdf and more even{% endif %}" />\n'
        ),
        (
            '<input class="{% if this %}then something neat{% else %}that is long stuff asdf and more even{% endif %}" />\n'
        ),
        (),
        id="no option",
    ),
    pytest.param(
        (
            '<a href="#"\n   class="list-group-item{% if not is_allowed %} disabled{% endif %}">foo</a>\n'
        ),
        (
            '<a href="#"\n   class="list-group-item{% if not is_allowed %} disabled{% endif %}">foo</a>\n'
        ),
        (),
        id="no option two",
    ),
    pytest.param(
        (
            '<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96"}}{% else %}{% static \'/img/report_thumb_placeholder_400x300.png\' %}{% endif %}" src="{% static \'/img/loader.gif\' %}" alt="report image"/>'
        ),
        (
            '<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96" }}{% else %}{% static \'/img/report_thumb_placeholder_400x300.png\' %}{% endif %}"\n'
            "     src=\"{% static '/img/loader.gif' %}\"\n"
            '     alt="report image" />\n'
        ),
        (),
        id="no option three",
    ),
    pytest.param(
        (
            '<a class="asdf {% if favorite == "yes" %}favorite{% endif %} has-tooltip-arrow has-tooltip-right" data-tooltip="{% if favorite == "yes" %}Remove from Favorites {% else %}Add to Favorites{% endif %}" fav-type="report" object-id="{{ report.report_id }}"><span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span></a>'
        ),
        (
            '<a class="asdf {% if favorite == "yes" %}favorite{% endif %} has-tooltip-arrow has-tooltip-right"\n'
            '   data-tooltip="{% if favorite == "yes" %}Remove from Favorites {% else %}Add to Favorites{% endif %}"\n'
            '   fav-type="report"\n'
            '   object-id="{{ report.report_id }}"><span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span></a>\n'
        ),
        (),
        id="no option four",
    ),
    pytest.param(
        (
            '<div class="media-content" {% ifchanged comment.stream_id %} comments-msg {% else %} comments-newMsgReply {% endifchanged %}>\n'
        ),
        (
            '<div class="media-content"\n'
            "     {% ifchanged comment.stream_id %} comments-msg {% else %} comments-newMsgReply {% endifchanged %}>\n"
        ),
        (),
        id="no option five",
    ),
    pytest.param(
        (
            '<a class="piwik_download" href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}">'
        ),
        (
            '<a class="piwik_download"\n'
            '   href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}">\n'
        ),
        (),
        id="no option six",
    ),
    pytest.param(
        (
            "<span {%if a%}required{%endif%}title=\"{% if eev.status == eev.STATUS_CURRENT %} {% trans 'A' %} {% elif eev.status == eev.STATUS_APPROVED %} {% trans 'B' %} {% elif eev.status == eev.STATUS_EXPIRED %} {% trans 'C' %}{% endif %}\" class=\"asdf{%if a%}b{%endif%} asdf\" {%if a%}checked{%endif%}>\n"
        ),
        (
            "<span {% if a %}required{% endif %}\n"
            "      title=\"{% if eev.status == eev.STATUS_CURRENT %} {% trans 'A' %} {% elif eev.status == eev.STATUS_APPROVED %} {% trans 'B' %} {% elif eev.status == eev.STATUS_EXPIRED %} {% trans 'C' %}{% endif %}\"\n"
            '      class="asdf{% if a %}b{% endif %} asdf"\n'
            "      {% if a %}checked{% endif %}>\n"
        ),
        (),
        id="no option seven",
    ),
    pytest.param(
        (
            '<div class="bg-level{% if value >= 70 %}1{% elif value >= 60 %}2{% elif value >= 50 %}3{% else %}4{% endif %}>\n</div>\n'
        ),
        (
            '<div class="bg-level{% if value >= 70 %}1{% elif value >= 60 %}2{% elif value >= 50 %}3{% else %}4{% endif %}>\n</div>\n'
        ),
        (),
        id="no option eight",
    ),
    pytest.param(
        (
            "{% block body %}\n"
            '   <form action="{% if gpg -%}asdf something pretty long. can\'t beat this length{%- endif %}"\n'
            '         method="POST">\n'
            "    </form>\n"
            "{% endblock body %}\n"
        ),
        (
            "{% block body %}\n"
            '    <form action="{% if gpg -%}asdf something pretty long. can\'t beat this length{%- endif %}"\n'
            '          method="POST">\n'
            "    </form>\n"
            "{% endblock body %}\n"
        ),
        (),
        id="no option nine",
    ),
    pytest.param(
        (
            '<ul class="menu-list{% for child in entry.children %}{% if child.url== page.url %}is-active{%else%}not-active{% endif %}{% endfor %} is-collapsible">\n'
        ),
        (
            '<ul class="menu-list{% for child in entry.children %}{% if child.url== page.url %}is-active{% else %}not-active{% endif %}{% endfor %} is-collapsible">\n'
        ),
        (),
        id="no option for loop",
    ),
    pytest.param(
        (
            '<div {% if true %}class="test"{% endif %} {% include "django/forms/widgets/attrs.html" %}></div>'
        ),
        (
            '<div {% if true %}class="test"{% endif %}\n'
            '     {% include "django/forms/widgets/attrs.html" %}></div>\n'
        ),
        (),
        id="no option include",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
