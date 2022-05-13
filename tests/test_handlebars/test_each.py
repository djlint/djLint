"""Djlint tests specific to Handlebars.js.

run::

   pytest tests/test_handlebars.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_handlebars.py::test_each --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_each(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""{{#each people}}{{print_person}} <p>and more long stuff</p>{{/each}}""",
    )
    print(output.text)
    assert output.exit_code == 1
    assert (
        output.text
        == r"""{{#each people }}
    {{ print_person }}
    <p>
        and more long stuff
    </p>
{{/each }}
"""
    )
