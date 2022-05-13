"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config.py::test_custom_html --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116


from click.testing import CliRunner

from src.djlint import main as djlint


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/test_config/test_ignores"])
    assert """Linted 1 file, found 0 errors.""" in result.output
    assert result.exit_code == 0
