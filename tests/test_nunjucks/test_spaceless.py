"""Djlint tests specific to nunjucks spaceless tags.

run::

   pytest tests/test_nunjucks/test_macro.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_nunjucks/test_macro.py::test_macro --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""

from typing import TextIO

from click.testing import CliRunner


from ..conftest import reformat


def test_spaceless(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{%- if entry.children.length -%}<strong>{%- endif -%}""",
    )

    assert output.exit_code == 0
    assert (
        output.text
        == r"""{%- if entry.children.length -%}<strong>{%- endif -%}
"""
    )
