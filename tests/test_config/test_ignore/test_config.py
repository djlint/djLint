"""Djlint tests specific to pyproject.toml configuration.

pytest tests/test_config/test_ignore

"""
from click.testing import CliRunner

from src.djlint import main as djlint


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/test_config/test_ignore/html.html"])
    assert """Linted 1 file, found 0 errors.""" in result.output
    assert result.exit_code == 0


def test_ignored_rule_does_not_disable_formatting(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/test_config/test_ignore/html_two.html", "--check"]
    )
    print(result.output)
    assert (
        """ {# djlint:off H021 #}
 <div>
-<div>
-{{ test }}
-</div>
+    <div>{{ test }}</div>
 </div>
 {# djlint:on #}"""
        in result.output
    )
