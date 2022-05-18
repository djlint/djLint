"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config/test_custom_tags/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config/test_custom_tags/test_config.py::test_custom_tags

"""
# pylint: disable=C0116


from click.testing import CliRunner

from src.djlint import main as djlint


def test_custom_tags(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/test_config/test_custom_tags/html.html", "--check"]
    )
    print(result.output)
    assert (
        """-{% example stuff %}<p>this is a very very long paragraph that does nothing except be a long paragraph asdfasdfasdfasdfasdf fasdf asdfasdfasdf</p>{% endexample %}
+{% example stuff %}
+    <p>
+        this is a very very long paragraph that does nothing except be a long paragraph asdfasdfasdfasdfasdf fasdf asdfasdfasdf
+    </p>
+{% endexample %}
"""
        in result.output
    )
    assert result.exit_code == 1
