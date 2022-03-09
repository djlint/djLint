"""Djlint tests specific to django.

run::

   pytest tests/test_django.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_django.py::test_comment --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat

def test_templatetag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}""",
    )
    assert output.exit_code == 0
    assert (
        output.text
        == r"""{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}
"""
    )


def test_empty_tags_on_one_line(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"{% if stuff %}\n{% endif %}")
    assert output.text == """{% if stuff %}{% endif %}\n"""
    assert output.exit_code == 1


def test_single_line_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% if messages|length %}{% for message in messages %}{{ message }}{% endfor %}{% endif %}""",
    )
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{% if messages|length %}
    {% for message in messages %}{{ message }}{% endfor %}
{% endif %}
"""
    )
