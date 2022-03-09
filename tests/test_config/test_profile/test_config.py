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


def test_profile(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/test_config/test_profile/html.html"])

    assert "T001" in result.output
    assert "J018" not in result.output
    assert "D018" in result.output

    result = runner.invoke(
        djlint, ["tests/test_config/test_profile/html.html", "--profile", "jinja"]
    )
    assert "T001" in result.output
    assert "J018" in result.output
    assert "D018" not in result.output

    result = runner.invoke(
        djlint, ["tests/test_config/test_profile/html.html", "--profile", "handlebars"]
    )
    assert "T001" not in result.output
    assert "J018" not in result.output
    assert "D018" not in result.output

    result = runner.invoke(
        djlint, ["tests/test_config/test_profile/html.html", "--check", "--profile", "handlebars"]
    )

    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ["tests/test_config/test_profile/html.html", "--check", "--profile", "jinja"]
    )
    assert result.exit_code == 1
    assert (
        """-{{test}}
+{{ test }}"""
        in result.output
    )
