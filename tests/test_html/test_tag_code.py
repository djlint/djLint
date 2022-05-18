"""Djlint tests for html code tag.

run:

    pytest tests/test_html/test_tag_code.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_code.py::test_code_tag

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_code_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<ol>
    <li>
        <code>a</code> b
    </li>
</ol>""",
    )
    assert output.exit_code == 0
