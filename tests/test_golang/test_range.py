"""Djlint tests specific to go-lang.

run::

   pytest tests/test_golang.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_golang.py::test_inline_comment --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from ..conftest import reformat


def test_range(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"{{ range .Items }} {{ end }}")
    assert output.exit_code == 0
