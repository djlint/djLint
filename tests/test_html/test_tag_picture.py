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


def test_picture_source_img_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""\
<picture><source media="(max-width:640px)"
srcset="image.jpg"><img src="image.jpg" alt="image"></picture>""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text(encoding="utf8")
        == """<picture>
    <source media="(max-width:640px)" srcset="image.jpg">
    <img src="image.jpg" alt="image">
</picture>
"""
    )
