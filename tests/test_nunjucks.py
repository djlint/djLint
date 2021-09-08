"""Djlint tests specific to nunjucks.

run::

   pytest tests/test_nunjucks.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116
from pathlib import Path
from typing import TextIO

from click.testing import CliRunner

from src.djlint import main as djlint

from .conftest import write_to_file


def test_template_tags(runner: CliRunner, tmp_file: TextIO) -> None:
    write_to_file(
        tmp_file.name,
        b"""{%- set posts = collections.docs -%}""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text() == """{%- set posts = collections.docs -%}\n"""
    )

    # ensure spaces are added
    write_to_file(
        tmp_file.name,
        b"""{%-set posts = collections.docs-%}\n{%asdf%}""",
    )
    runner.invoke(djlint, [tmp_file.name, "--reformat"])
    assert (
        Path(tmp_file.name).read_text()
        == """{%- set posts = collections.docs -%}\n{% asdf %}\n"""
    )
