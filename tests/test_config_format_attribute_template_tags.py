"""Djlint tests specific to pyproject.toml > format_attribute_template_tags configuration.

run::

   pytest tests/test_config_format_attribute_template_tags.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_format_attribute_template_tags.py::test_attribute_include --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint

from .conftest import reformat


def test_with_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/config_format_attribute_template_tags", "--check"]
    )
    print(result.output)
    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0


def test_without_config(runner: CliRunner, tmp_file: TextIO) -> None:

    output = reformat(
        tmp_file,
        runner,
        b'<input class="{% if this %}then something neat{% else %}that is long stuff asdf and more even{% endif %}"/>\n',
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b'<a href="#"\n   class="list-group-item{% if not is_allowed %} disabled{% endif %}">foo</a>\n',
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96"}}{% else %}{% static '/img/report_thumb_placeholder_400x300.png' %}{% endif %}" src="{% static '/img/loader.gif' %}" alt="report image"/>""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == r"""<img data-src="{% if report.imgs.exists %}{{ report.imgs.first.get_absolute_url|size:"96x96" }}{% else %}{% static '/img/report_thumb_placeholder_400x300.png' %}{% endif %}"
     src="{% static '/img/loader.gif' %}"
     alt="report image"/>
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""<a class="asdf {% if favorite == "yes" %}favorite{% endif %} has-tooltip-arrow has-tooltip-right" data-tooltip="{% if favorite == "yes" %}Remove from Favorites {% else %}Add to Favorites{% endif %}" fav-type="report" object-id="{{ report.report_id }}"><span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span></a>""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == r"""<a class="asdf {% if favorite == "yes" %}favorite{% endif %} has-tooltip-arrow has-tooltip-right"
   data-tooltip="{% if favorite == "yes" %}Remove from Favorites {% else %}Add to Favorites{% endif %}"
   fav-type="report"
   object-id="{{ report.report_id }}">
    <span class="icon has-text-grey is-large "><i class="fas fa-lg fa-star"></i></span>
</a>
"""
    )
    output = reformat(
        tmp_file,
        runner,
        b"""<div class="media-content" {% ifchanged comment.stream_id %} comments-msg {% else %} comments-newMsgReply {% endifchanged %}>""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == r"""<div class="media-content"
     {% ifchanged comment.stream_id %} comments-msg {% else %} comments-newMsgReply {% endifchanged %}>
"""
    )
    output = reformat(
        tmp_file,
        runner,
        b"""<a class="piwik_download" href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}">""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == """<a class="piwik_download"
   href="{% static activity_version.get_win_document_with_images_file_path %}?{% now "jSFYHi" %}">
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""<span {%if a%}required{%endif%}title="{% if eev.status == eev.STATUS_CURRENT %} {% trans 'A' %} {% elif eev.status == eev.STATUS_APPROVED %} {% trans 'B' %} {% elif eev.status == eev.STATUS_EXPIRED %} {% trans 'C' %}{% endif %}" class="asdf{%if a%}b{%endif%} asdf" {%if a%}checked{%endif%}>""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == """<span {% if a %}required{% endif %}
      title="{% if eev.status == eev.STATUS_CURRENT %} {% trans 'A' %} {% elif eev.status == eev.STATUS_APPROVED %} {% trans 'B' %} {% elif eev.status == eev.STATUS_EXPIRED %} {% trans 'C' %}{% endif %}"
      class="asdf{% if a %}b{% endif %} asdf"
      {% if a %}checked{% endif %}>
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""<div class="bg-level{% if value >= 70 %}1{% elif value >= 60 %}2{% elif value >= 50 %}3{% else %}4{% endif %}>\n</div>""",
    )
    assert output.exit_code == 0

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
    assert output.exit_code == 0


def test_attribute_for_loop(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<ul class="menu-list{% for child in entry.children %}{% if child.url== page.url %}is-active{%else%}not-active{% endif %}{% endfor %} is-collapsible">""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == r"""<ul class="menu-list{% for child in entry.children %}{% if child.url== page.url %}is-active{% else %}not-active{% endif %}{% endfor %} is-collapsible">
"""
    )


def test_attribute_include(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<div {% if true %}class="test"{% endif %} {% include "django/forms/widgets/attrs.html" %}></div>""",
    )
    assert output.exit_code == 1

    assert (
        output.text
        == r"""<div {% if true %}class="test"{% endif %}
     {% include "django/forms/widgets/attrs.html" %}></div>
"""
    )
