"""Djlint tests specific to .djlintrc configuration.

run::

   pytest tests/test_config_json.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config_json.py::test_custom_html --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_config(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_json/html.html", "--check"])

    print(result.output)

    assert (
        """-{% example stuff %}<p>this is a long paragraph</p>{% endexample %}
+{% example stuff %}
+  <p>
+    this is a long paragraph
+  </p>
+{% endexample %}
"""
        in result.output
    )
    assert result.exit_code == 1
