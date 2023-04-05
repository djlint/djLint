"""Djlint linter rule tests.

run::

   pytest tests/test_linter.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_linter/test_linter.py::test_random

Test setup

(html, (list of codes that should file, plus optional line number))


"""
# pylint: disable=C0116,C0103,C0302


import pytest

from src.djlint.lint import linter
from tests.conftest import lint_printer

test_data = [
    pytest.param(
        ("{%- test-%}"),
        ([("T001", 1)]),
        (),
        id="T001",
    ),
    pytest.param(
        ("{%-test -%}"),
        ([("T001", 1)]),
        (),
        id="T001_2",
    ),
    pytest.param(
        ("{%- test -%}"),
        (),
        (["T001"]),
        id="T001_3",
    ),
]


@pytest.mark.parametrize(("source", "expected", "excluded"), test_data)
def test_jinja_linter(source, expected, excluded, nunjucks_config) -> None:
    filename = "file"
    filepath = filename
    lint = linter(nunjucks_config, source, filename, filepath)[filename]

    lint_printer(source, expected, excluded, lint)

    def check_rule(rule, lint):
        if isinstance(rule, tuple):
            return (
                any(
                    x["code"] == rule[0] and int(x["line"].split(":")[0]) == rule[1]
                    for x in lint
                )
                is True
            )
        else:
            return any(x["code"] == rule for x in lint) is True

    for rule in expected:
        assert check_rule(rule, lint) is True

    for rule in excluded:
        assert check_rule(rule, lint) is False


# def test_T001(runner: CliRunner, tmp_file: TextIO) -> None:


#     write_to_file(tmp_file.name, b"{%-test -%}")
#     result = runner.invoke(djlint, [tmp_file.name, "--profile", "nunjucks"])
#     assert result.exit_code == 1
#     assert "T001 1:" in result.output

#     write_to_file(tmp_file.name, b"{%- test -%}")
#     result = runner.invoke(djlint, [tmp_file.name, "--profile", "nunjucks"])
#     assert result.exit_code == 0
