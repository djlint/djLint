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

def test_reformat_asset_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    # pylint: disable=C0301
    output = reformat(
        tmp_file,
        runner,
        b"""{% block css %}{% assets "css_error" %}<link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />{% endassets %}{% endblock css %}""",
    )  # noqa: E501
    assert (
        output.text
        == """{% block css %}
    {% assets "css_error" %}
        <link type="text/css" rel="stylesheet" href="{{ ASSET_URL }}" />
    {% endassets %}
{% endblock css %}
"""
    )
    assert output.exit_code == 1

