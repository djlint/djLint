"""Djlint tests for html small tag.

run:

    pytest tests/test_html/test_tag_small.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

    pytest tests/test_html/test_tag_small.py::test_small_tag


"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint
from tests.conftest import write_to_file


def test_small_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""<small>text</small>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<small>text</small>
"""
    )
