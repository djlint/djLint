"""Djlint tests specific to django.

run::

   pytest tests/test_django.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_django.py::test_attribute_include --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from .conftest import reformat


def test_empty_tags_on_one_line(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"{% if stuff %}\n{% endif %}")
    assert output["text"] == """{% if stuff %}{% endif %}\n"""
    assert output["exit_code"] == 1


def test_dj_comments_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{# comment #}\n{% if this %}<div></div>{% endif %}"
    )
    assert output["text"] == """{# comment #}\n{% if this %}<div></div>{% endif %}\n"""
    # no change was required
    assert output["exit_code"] == 0


def test_reformat_asset_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    # pylint: disable=C0301
    output = reformat(
        tmp_file,
        runner,
        b"""{% block css %}{% assets "css_error" %}<link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />{% endassets %}{% endblock css %}""",
    )  # noqa: E501
    assert (
        output["text"]
        == """{% block css %}
    {% assets "css_error" %}
        <link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />
    {% endassets %}
{% endblock css %}
"""
    )
    assert output["exit_code"] == 1


def test_autoescape(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{% autoescape on %}{{ body }}{% endautoescape %}"
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% autoescape on %}
    {{ body }}
{% endautoescape %}
"""
    )


def test_comment(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"""{% comment "Optional note" %}{{ body }}{% endcomment %}"""
    )
    assert output["exit_code"] == 0
    # too short to put on multiple lines
    assert (
        output["text"]
        == r"""{% comment "Optional note" %}{{ body }}{% endcomment %}
"""
    )


def test_inline_comment(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{# <div></div> #}\n{% if this %}<div></div>{% endif %}"
    )
    assert (
        output["text"] == """{# <div></div> #}\n{% if this %}<div></div>{% endif %}\n"""
    )
    assert output["exit_code"] == 0


def test_for_loop(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<ul>{% for athlete in athlete_list %}<li>{{ athlete.name }}</li>{% empty %}<li>Sorry, no athletes in this list.</li>{% endfor %}</ul>""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""<ul>
    {% for athlete in athlete_list %}
        <li>{{ athlete.name }}</li>
    {% empty %}
        <li>Sorry, no athletes in this list.</li>
    {% endfor %}
</ul>
"""
    )


def test_filter(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% filter force_escape|lower %}This text will be HTML-escaped, and will appear in all lowercase.{% endfilter %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% filter force_escape|lower %}
    This text will be HTML-escaped, and will appear in all lowercase.
{% endfilter %}
"""
    )


def test_if(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% if athlete_list %}Number of athletes: {{ athlete_list|length }}{% elif athlete_in_locker_room_list %}Athletes should be out of the locker room soon!{% else %}No athletes.{% endif %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
"""
    )


def test_ifchanged(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% for match in matches %}<div style="background-color:"pink">{% ifchanged match.ballot_id %}{% cycle "red" "blue" %}{% else %}gray{% endifchanged %}{{ match }}</div>{% endfor %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% for match in matches %}
    <div style="background-color:"pink">
        {% ifchanged match.ballot_id %}
            {% cycle "red" "blue" %}
        {% else %}
            gray
        {% endifchanged %}
        {{ match }}
    </div>
{% endfor %}
"""
    )


def test_include(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"""{% include "this" %}{% include "that"%}""")
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% include "this" %}
{% include "that" %}
"""
    )


def test_spaceless(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% spaceless %}<p><a href="foo/">Foo</a></p>{% endspaceless %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% spaceless %}
    <p>
        <a href="foo/">Foo</a>
    </p>
{% endspaceless %}
"""
    )


def test_templatetag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}""",
    )
    assert output["exit_code"] == 0
    assert (
        output["text"]
        == r"""{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}
"""
    )


def test_verbatim(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"""{% verbatim %}Still alive.{% endverbatim %}"""
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% verbatim %}
    Still alive.
{% endverbatim %}
"""
    )


def test_blocktranslate(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktranslate %}The width is: {{ width }}{% endblocktranslate %}""",
    )
    assert output["exit_code"] == 0
    assert (
        output["text"]
        == r"""{% blocktranslate %}The width is: {{ width }}{% endblocktranslate %}
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktranslate trimmed %}The width is: {{ width }}{% endblocktranslate %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% blocktranslate trimmed %}
    The width is: {{ width }}
{% endblocktranslate %}
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktrans %}The width is: {{ width }}{% endblocktrans %}""",
    )
    assert output["exit_code"] == 0
    assert (
        output["text"]
        == r"""{% blocktrans %}The width is: {{ width }}{% endblocktrans %}
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""{% blocktrans trimmed %}The width is: {{ width }}{% endblocktrans %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% blocktrans trimmed %}
    The width is: {{ width }}
{% endblocktrans %}
"""
    )


def test_trans(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"""<p>{% trans 'Please do <b>Blah</b>.' %}</p>"""
    )
    assert output["exit_code"] == 1
    assert (
        """<p>
    {% trans 'Please do <b>Blah</b>.' %}
</p>
"""
        in output["text"]
    )


def test_with(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% with total=business.employees.count %}{{ total }}<div>employee</div>{{ total|pluralize }}{% endwith %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% with total=business.employees.count %}
    {{ total }}
    <div>employee</div>
    {{ total|pluralize }}
{% endwith %}
"""
    )


def test_single_line_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% if messages|length %}{% for message in messages %}{{ message }}{% endfor %}{% endif %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% if messages|length %}
    {% for message in messages %}{{ message }}{% endfor %}
{% endif %}
"""
    )


def test_complex_attributes(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96"}}{% else %}{% static '/img/report_thumb_placeholder_400x300.png' %}{% endif %}" src="{% static '/img/loader.gif' %}" alt="report image"/>""",
    )
    assert output["exit_code"] == 1

    assert (
        output["text"]
        == r"""<img data-src="{% if report.imgs.exists %}
                   {{ report.imgs.first.get_absolute_url|size:"96x96" }}
               {% else %}
                   {% static '/img/report_thumb_placeholder_400x300.png' %}
               {% endif %}"
     src="{% static '/img/loader.gif' %}"
     alt="report image"/>
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""<a class="asdf {% if favorite == "yes" %}favorite{% endif %} has-tooltip-arrow has-tooltip-right" data-tooltip="{% if favorite == "yes" %}Remove from Favorites {% else %}Add to Favorites{% endif %}" fav-type="report" object-id="{{ report.report_id }}"><span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span></a>""",
    )
    assert output["exit_code"] == 1

    assert (
        output["text"]
        == r"""<a class="asdf
          {% if favorite == "yes" %}
              favorite
          {% endif %}
          has-tooltip-arrow has-tooltip-right"
   data-tooltip="{% if favorite == "yes" %}
                     Remove from Favorites
                 {% else %}
                     Add to Favorites
                 {% endif %}"
   fav-type="report"
   object-id="{{ report.report_id }}">
    <span class="icon has-text-grey is-large ">
        <i class="fas fa-lg fa-star"></i>
    </span>
</a>
"""
    )
    output = reformat(
        tmp_file,
        runner,
        b"""<div class="media-content" {% ifchanged comment.stream_id %} comments-msg {% else %} comments-newMsgReply {% endifchanged %}>""",
    )
    assert output["exit_code"] == 1
    print(output["text"])
    assert (
        output["text"]
        == r"""<div class="media-content"
     {% ifchanged comment.stream_id %}
         comments-msg
     {% else %}
         comments-newMsgReply
     {% endifchanged %}>
"""
    )
    output = reformat(
        tmp_file,
        runner,
        b"""<a class="piwik_download" href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}">""",
    )
    assert (
        output["text"]
        == """<a class="piwik_download"
   href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}">
"""
    )
    assert output["exit_code"] == 1

    output = reformat(
        tmp_file,
        runner,
        b"""<span {%if a%}required{%endif%}title="{% if eev.status == eev.STATUS_CURRENT %} {% trans 'A' %} {% elif eev.status == eev.STATUS_APPROVED %} {% trans 'B' %} {% elif eev.status == eev.STATUS_EXPIRED %} {% trans 'C' %}{% endif %}" class="asdf{%if a%}b{%endif%} asdf" {%if a%}checked{%endif%}>""",
    )

    print(output["text"])
    assert (
        output["text"]
        == """<span {% if a %}
          required
      {% endif %}
      title="{% if eev.status == eev.STATUS_CURRENT %}
                 {% trans 'A' %}
             {% elif eev.status == eev.STATUS_APPROVED %}
                 {% trans 'B' %}
             {% elif eev.status == eev.STATUS_EXPIRED %}
                 {% trans 'C' %}
             {% endif %}"
      class="asdf
             {% if a %}
                 b
             {% endif %}
             asdf"
      {% if a %}
          checked
      {% endif %}>
"""
    )
    assert output["exit_code"] == 1

    output = reformat(
        tmp_file,
        runner,
        b"""<div class="bg-level{% if value >= 70 %}1{% elif value >= 60 %}2{% elif value >= 50 %}3{% else %}4{% endif %}>\n</div>""",
    )
    assert output["exit_code"] == 0

    # check attributes that have short if inside a attribute tag

    output = reformat(
        tmp_file,
        runner,
        b"""{% block body %}
    <form action="{% if gpg -%}asdf something pretty long. can't beat this length{%- endif %}"
          method="POST">
    </form>
{% endblock body %}
""",
    )
    assert output["exit_code"] == 0


def test_load_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% block content %}{% load i18n %}{% endblock %}""",
    )
    assert output["exit_code"] == 1
    assert (
        output["text"]
        == r"""{% block content %}
    {% load i18n %}
{% endblock %}
"""
    )


def test_attribute_for_loop(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<ul class="menu-list{% for child in entry.children %}{% if child.url== page.url %}is-active{%else%}not-active{% endif %}{% endfor %} is-collapsible">""",
    )
    assert output["exit_code"] == 1

    assert (
        output["text"]
        == r"""<ul class="menu-list
           {% for child in entry.children %}
               {% if child.url== page.url %}
                   is-active
               {% else %}
                   not-active
               {% endif %}
           {% endfor %}
           is-collapsible">
"""
    )


def test_attribute_include(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<div {% if true %}class="test"{% endif %} {% include "django/forms/widgets/attrs.html" %}></div>""",
    )
    assert output["exit_code"] == 1

    assert (
        output["text"]
        == r"""<div {% if true %}
         class="test"
     {% endif %}
     {% include "django/forms/widgets/attrs.html" %}></div>
"""
    )


def test_multiple_endblocks(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% block content %}{% block scripts %}{% endblock %}{% endblock %}""",
    )
    assert output["exit_code"] == 1
    assert (
        """{% block content %}\n    {% block scripts %}{% endblock %}\n{% endblock %}
"""
        == output["text"]
    )
