"""Djlint tests specific to nunjucks template tags.

run::

   pytest tests/test_nunjucks/test_macro.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_nunjucks/test_macro.py::test_macro --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_template_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"{%- set posts = collections.docs -%}")

    assert output.text == r"""{%- set posts = collections.docs -%}\n"""

    output = reformat(tmp_file, runner, b"{%-set posts = collections.docs-%}\n{%asdf%}")

    assert output.text == r"""{%- set posts = collections.docs -%}\n{% asdf %}\n"""
