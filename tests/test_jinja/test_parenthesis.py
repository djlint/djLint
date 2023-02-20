"""Djlint tests specific to jinja.

run::

   pytest tests/test_jinja/test_parenthesis.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_jinja/test_parenthesis.py::test_parenthesis --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_parenthesis(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(tmp_file, runner, b"{{ url('foo')}}")
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{{ url('foo') }}
"""
    )
