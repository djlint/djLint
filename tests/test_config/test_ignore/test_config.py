"""Djlint tests specific to pyproject.toml configuration.

pytest tests/test_config/test_ignore

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ("tests/test_config/test_ignore/html.html"))
    assert """Linted 1 file, found 0 errors.""" in result.output
    assert result.exit_code == 0


def test_ignored_rule_does_not_disable_formatting(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ("tests/test_config/test_ignore/html_two.html", "--check")
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


def test_ignore_list_may_hold_spaces(runner: CliRunner) -> None:
    """A code written after a comma and a space is still ignored."""
    result = runner.invoke(
        djlint, ("-", "--lint", "--ignore", "H011, H013"), input="<img src=x>\n"
    )

    assert "found 0 errors" in result.output


def test_include_list_may_hold_spaces(runner: CliRunner) -> None:
    """A code written after a comma and a space is still included."""
    result = runner.invoke(
        djlint,
        ("-", "--lint", "--profile", "django", "--include", "H006, T003"),
        input="{% block a %}\n<p>x</p>\n{% endblock %}\n",
    )

    assert "T003" in result.output
