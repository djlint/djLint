"""DjLint tests for alpine.js.

run:

   pytest tests/test_html/test_alpinejs.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html/test_alpinejs.py::test_alpine_js

"""
# pylint: disable=C0116
from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_alpine_js(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<div id="collapse"
     x-data="{ show: true }"
     x-show="show"
     x-transition.duration.500ms></div>""",
    )

    assert output.exit_code == 0
