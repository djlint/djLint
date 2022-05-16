"""Djlint tests specific to django.

run::

   pytest tests/test_django/test_comments.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_django/test_comments.py::test_comment

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_dj_comments_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{# comment #}\n{% if this %}<div></div>{% endif %}"
    )
    assert output.text == """{# comment #}\n{% if this %}<div></div>{% endif %}\n"""
    # no change was required
    assert output.exit_code == 0


def test_comment(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"""{% comment "Optional note" %}{{ body }}{% endcomment %}"""
    )
    assert output.exit_code == 0
    # too short to put on multiple lines
    assert (
        output.text
        == r"""{% comment "Optional note" %}{{ body }}{% endcomment %}
"""
    )

    output = reformat(
        tmp_file,
        runner,
        b"""<div class="hi">
    <div class="poor">
        <p class="format">
            Lorem ipsum dolor
            <span class="bold">sit</span>
            amet
        </p>
        <img src="./pic.jpg">
    </div>
    <script src="file1.js"></script>
    {% comment %} <script src="file2.js"></script>
    <script src="file3.js"></script> {% endcomment %}
    <script src="file4.js"></script>
</div>""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<div class="hi">
    <div class="poor">
        {# djlint:off #}
        <p class="format">
            Lorem ipsum dolor <span class="bold">sit</span> amet
        </p>
        {# djlint:on #}
        <img src="./pic.jpg">
    </div>
    <ul>
        {% for i in items %}
            <li>item {{i}}</li>
            {% if i > 10 %}{% endif %}
            <li>item {{i}}</li>
        {% endfor %}
    </ul>
</div>
""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<html>
    <head>
        <script src="file1.js"></script>
        {% comment %}
        <script src="file2.js"></script>
        <script src="file3.js"></script>
        <script src="file4.js"></script>
        {% endcomment %}
        <script src="file5.js"></script>
    </head>
    <body></body>
</html>
""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<html>
    <head>
        <script src="file1.js"></script>
        {# djlint:off #}
        {% comment %}
        <script src="file2.js"></script>
        <script src="file3.js"></script>
        <script src="file4.js"></script>
        {% endcomment %}
        {# djlint:on #}
        <script src="file5.js"></script>
    </head>
    <body></body>
</html>
""",
    )

    assert output.exit_code == 0


def test_inline_comment(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{# <div></div> #}\n{% if this %}<div></div>{% endif %}"
    )
    assert output.text == """{# <div></div> #}\n{% if this %}<div></div>{% endif %}\n"""
    assert output.exit_code == 0
