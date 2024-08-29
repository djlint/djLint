"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config/test_per_file_ignores/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config.py::test_custom_html --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_config/test_per_file_ignores"))
    assert "H025" not in result.output
    assert "H020" in result.output
