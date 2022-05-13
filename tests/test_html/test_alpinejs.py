"""DjLint tests for alpine.js."""
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
