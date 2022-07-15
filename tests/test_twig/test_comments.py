"""Djlint tests specific to twig.

run::

   pytest tests/test_twig/test_comments.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_twig/test_comments.py::test_nested --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_macro(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{% if %}
    {#
        line
    #}
{% endif %}
""",
    )
    assert output.exit_code == 0
