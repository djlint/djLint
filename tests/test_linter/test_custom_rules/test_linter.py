"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_linter/test_custom_rules/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config.py::test_custom_html --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint
from tests.conftest import write_to_file

if TYPE_CHECKING:
    from tempfile import _TemporaryFileWrapper

    from click.testing import CliRunner


def test_custom_rules(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_linter/test_custom_rules/", "--profile", "django")
    )
    assert """Linting""" in result.output
    assert """1/1""" in result.output
    assert """T001 1:""" in result.output
    assert result.exit_code == 1


def test_rules_option(
    runner: CliRunner, tmp_file: _TemporaryFileWrapper[bytes]
) -> None:
    """A rules file outside the project root can be given with --rules."""
    write_to_file(tmp_file.name, b"This is trichotillomania.")
    result = runner.invoke(
        djlint,
        (
            tmp_file.name,
            "--profile",
            "django",
            "--rules",
            "tests/test_linter/test_custom_rules/.djlint_rules.yaml",
        ),
    )
    assert """T001 1:""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(djlint, (tmp_file.name, "--profile", "django"))
    assert """T001""" not in result.output
    assert result.exit_code == 0
