"""Djlint tests specific to nunjucks macros.

run::

   pytest tests/test_nunjucks/test_macro.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_nunjucks/test_macro.py::test_macro --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_macro(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file, runner, b"{% macro 'cool' %}<div>some html</div>{% endmacro %}"
    )
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{% macro 'cool' %}
    <div>some html</div>
{% endmacro %}
"""
    )
