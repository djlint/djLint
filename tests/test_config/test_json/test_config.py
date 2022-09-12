"""Djlint tests specific to .djlintrc configuration.

run::

   pytest tests/test_config/test_json/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_json/test_config.py::test_custom_config

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_config(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/test_config/test_json/html.html", "--check"])

    print(result.output)

    assert (
        """-{% example stuff %}<p>this is a long paragraph</p>{% endexample %}
+{% example stuff %}
+  <p>this is a long paragraph</p>
+{% endexample %}
"""
        in result.output
    )
    assert result.exit_code == 1


def test_custom_config(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_json/html.html",
            "--check",
            "--configuration",
            "tests/test_config/test_json/.djlint-cust",
        ],
    )

    assert (
        """-{% example stuff %}<p>this is a long paragraph</p>{% endexample %}
+{% example stuff %}
+   <p>this is a long paragraph</p>
+{% endexample %}
"""
        in result.output
    )

    assert result.exit_code == 1
