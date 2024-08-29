"""Djlint tests specific to linter output format.

run::

   pytest tests/test_config_linter_output_format.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_linter_output_format.py::test_with_config --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_with_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_linter_output_format", "--lint")
    )
    assert result.exit_code == 1

    print(result.output)
    assert (
        """html-one.html:1:0: H025 Tag seems to be an orphan. <h1>
html-one.html:1:8: H025 Tag seems to be an orphan. </h2>
html-two.html:1:0: H025 Tag seems to be an orphan. <h1>
html-two.html:1:8: H025 Tag seems to be an orphan. </h2>"""
        in result.output
    )
