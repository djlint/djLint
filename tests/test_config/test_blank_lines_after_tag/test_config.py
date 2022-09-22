"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config/test_blank_lines_after_tag/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config/test_blank_lines_after_tag/test_config.py::test_blank_lines_after_tag_eight --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_blank_lines_after_tag(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/test_config/test_blank_lines_after_tag/html.html", "--check"]
    )
    assert (
        """+{% extends "nothing.html" %}
+
+{% load stuff %}
+{% load stuff 2 %}
+
+{% include "html_two.html" %}
+
+<div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1


def test_blank_lines_after_tag_two(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_after_tag/html_two.html", "--check"],
    )
    assert (
        """ {% load stuff %}
+
 <div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1


def test_blank_lines_after_tag_three(runner: CliRunner) -> None:
    # check blocks that do not start on a newline - they should be left as is.
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_after_tag/html_three.html", "--check"],
    )

    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0


def test_blank_lines_after_tag_four(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_after_tag/html_four.html", "--check"],
    )

    assert result.exit_code == 1
    assert (
        """ {% block this %}
-{% load i18n %}
+    {% load i18n %}
+
 {% endblock this %}
"""
        in result.output
    )


def test_blank_lines_after_tag_five(runner: CliRunner) -> None:
    # something perfect should stay perfect :)
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_after_tag/html_five.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_after_tag_six(runner: CliRunner) -> None:
    # something perfect should stay perfect :)
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_after_tag/html_six.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_after_tag_seven(runner: CliRunner) -> None:
    # make sure endblock doesn't pick up endblocktrans :)
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_after_tag/html_seven.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_after_tag_eight(runner: CliRunner) -> None:
    # check that multiple blank lines are not added
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_blank_lines_after_tag/html_eight.html",
            "--preserve-blank-lines",
            "--check",
        ],
    )
    print(result.output)
    assert result.exit_code == 0


def test_blank_lines_after_tag_nine(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_blank_lines_after_tag/html_nine.html",
            "--check",
        ],
    )
    assert result.exit_code == 0


def test_blank_lines_after_tag_ten(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_blank_lines_after_tag/html_ten.html",
            "--check",
        ],
    )
    assert result.exit_code == 0
