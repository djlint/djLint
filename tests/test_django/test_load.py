"""Djlint tests specific to django.

run::

   pytest tests/test_django.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_django.py::test_alpine_js --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_load_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% block content %}{% load i18n %}{% endblock %}""",
    )
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{% block content %}
    {% load i18n %}
{% endblock %}
"""
    )
