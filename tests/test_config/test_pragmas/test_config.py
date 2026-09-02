"""Djlint tests specific to pyproject.toml configuration.

uv run pytest tests/test_config/test_pragmas/test_config.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint import main as djlint

if TYPE_CHECKING:
    from click.testing import CliRunner


def test_require_pragma(runner: CliRunner) -> None:
    """That is a successful no-op, not a failure."""
    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_pragmas/html_one.html",
            "--lint",
            "--check",
            "--profile",
            "django",
        ),
    )

    # the file has no pragma, so require_pragma skipped it on purpose;
    assert """No files to check!""" in result.stderr
    assert result.exit_code == 0

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_pragmas/html_two.html",
            "--check",
            "--profile",
            "django",
        ),
    )
    assert (
        """ {# djlint:on #}
-{% extends "nothing.html" %}{% load stuff %}{% load stuff 2 %}{% include "html_two.html" %}<div></div>
+{% extends "nothing.html" %}
+{% load stuff %}
+{% load stuff 2 %}
+{% include "html_two.html" %}
+<div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_pragmas/html_three.html",
            "--check",
            "--profile",
            "handlebars",
        ),
    )

    assert (
        """ {{!-- djlint:on --}}
-<p>
-
-{{firstname}} </p><p>{{lastname}}</p>
+<p>{{firstname}}</p>
+<p>{{lastname}}</p>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_pragmas/html_four.html",
            "--check",
            "--profile",
            "golang",
        ),
    )

    assert (
        """ {{ /* djlint:on */ }}
-<h1>Test</h1><p>{{ .Variable }}</p>
-{{ range .Items }} <p>{{ . }}
-
-</p>{{ end }}
+<h1>Test</h1>
+<p>{{ .Variable }}</p>
+{{ range .Items }}
+    <p>{{ . }}</p>
+{{ end }}

1 file would be updated."""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(
        djlint, ("tests/test_config/test_pragmas/html_five.html", "--check")
    )
    assert (
        """ <!-- djlint:on -->
-{% extends "nothing.html" %}{% load stuff %}{% load stuff 2 %}{% include "html_two.html" %}<div></div>
+{% extends "nothing.html" %}
+{% load stuff %}
+{% load stuff 2 %}
+{% include "html_two.html" %}
+<div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(
        djlint,
        (
            "tests/test_config/test_pragmas/html_six.html",
            "--check",
            "--profile",
            "django",
        ),
    )
    assert (
        """ {% comment %} djlint:on {% endcomment %}
-{% extends "nothing.html" %}{% load stuff %}{% load stuff 2 %}{% include "html_two.html" %}<div></div>
+{% extends "nothing.html" %}
+{% load stuff %}
+{% load stuff 2 %}
+{% include "html_two.html" %}
+<div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1
