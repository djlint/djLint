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


def test_custom_html(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/test_config/test_custom_html/html.html", "--check"])
    print(result.output)
    assert (
        """-<mjml><mj-body>this is a email text</mj-body></mjml>
+<mjml>
+    <mj-body>
+        this is a email text
+    </mj-body>
+</mjml>
"""
        in result.output
    )
    assert result.exit_code == 1

