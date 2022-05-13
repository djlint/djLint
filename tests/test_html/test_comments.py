"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html.py::test_front_matter --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import write_to_file


def test_html_comments_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<div>\n    <!-- asdf--><!--\n multi\nline\ncomment--></div>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])

    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<div>
    <!-- asdf--><!--
 multi
line
comment-->
</div>
"""
    )
