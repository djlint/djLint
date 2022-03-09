"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config/test_indent/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config/test_indent/test_config.py::test_indent --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_indent(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/test_config/test_indent", "--check"])
    print(result.output)
    assert (
        """-<section><p><div><span></span></div></p></section>
+<section>
+  <p>
+    <div>
+      <span></span>
+    </div>
+  </p>
+</section>"""
        in result.output
    )
    assert result.exit_code == 1

    result = runner.invoke(djlint, ["tests/test_config/test_indent", "--check", "--indent", 3])

    assert (
        """-<section><p><div><span></span></div></p></section>
+<section>
+   <p>
+      <div>
+         <span></span>
+      </div>
+   </p>
+</section>"""
        in result.output
    )
    assert result.exit_code == 1
