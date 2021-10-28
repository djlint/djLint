"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config.py::test_blank_lines_after_tag --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_custom_tags(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_custom_tags/html.html", "--check"])

    assert (
        """-{% example stuff %}<p>this is a long paragraph</p>{% endexample %}
+{% example stuff %}
+    <p>
+        this is a long paragraph
+    </p>
+{% endexample %}
"""
        in result.output
    )
    assert result.exit_code == 1


def test_extension(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_extension", "--check"])
    assert """Checking""" in result.output
    assert """1/1""" in result.output
    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0


def test_ignores(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_ignores"])
    assert """Linted 1 file, found 0 errors.""" in result.output
    assert result.exit_code == 0


def test_indent(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_indent", "--check"])

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

    result = runner.invoke(djlint, ["tests/config_indent", "--check", "--indent", 3])

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


def test_exclude(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_excludes"])
    assert """html.html""" in result.output
    assert """excluded.html""" not in result.output
    assert """foo/excluded.html""" not in result.output
    assert result.exit_code == 1


def test_blank_lines_after_tag(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/config_blank_lines_after_tag/html.html", "--check"]
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

    result = runner.invoke(
        djlint, ["tests/config_blank_lines_after_tag/html_two.html", "--check"]
    )
    assert (
        """ {% load stuff %}
+
 <div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    # check blocks that do not start on a newline - they should be left as is.
    result = runner.invoke(
        djlint, ["tests/config_blank_lines_after_tag/html_three.html", "--check"]
    )

    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ["tests/config_blank_lines_after_tag/html_four.html", "--check"]
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

    # something perfect should stay perfect :)
    result = runner.invoke(
        djlint, ["tests/config_blank_lines_after_tag/html_five.html", "--check"]
    )
    assert result.exit_code == 0


def test_profile(runner: CliRunner) -> None:
    result = runner.invoke(djlint, ["tests/config_profile/html.html"])

    assert "T001" in result.output
    assert "J018" not in result.output
    assert "D018" in result.output

    result = runner.invoke(
        djlint, ["tests/config_profile/html.html", "--profile", "jinja"]
    )
    assert "T001" in result.output
    assert "J018" in result.output
    assert "D018" not in result.output

    result = runner.invoke(
        djlint, ["tests/config_profile/html.html", "--profile", "handlebars"]
    )
    assert "T001" not in result.output
    assert "J018" not in result.output
    assert "D018" not in result.output

    result = runner.invoke(
        djlint, ["tests/config_profile/html.html", "--check", "--profile", "handlebars"]
    )

    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ["tests/config_profile/html.html", "--check", "--profile", "jinja"]
    )
    assert result.exit_code == 1
    assert (
        """-{{test}}
+{{ test }}"""
        in result.output
    )


def test_require_pragma(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        [
            "tests/config_pragmas/html_one.html",
            "--lint",
            "--check",
            "--profile",
            "django",
        ],
    )

    assert """No files to check!""" in result.output
    assert result.exit_code == 0

    result = runner.invoke(
        djlint, ["tests/config_pragmas/html_two.html", "--check", "--profile", "django"]
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
        ["tests/config_pragmas/html_three.html", "--check", "--profile", "handlebars"],
    )

    assert (
        """ {{!-- djlint:on --}}
 <p>
-
-{{firstname}} </p><p>{{lastname}}</p>
+    {{firstname}}
+</p>
+<p>
+    {{lastname}}
+</p>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(
        djlint,
        ["tests/config_pragmas/html_four.html", "--check", "--profile", "golang"],
    )

    assert (
        """ {{ /* djlint:on */ }}
-<h1>Test</h1><p>{{ .Variable }}</p>
-{{ range .Items }} <p>{{ . }}
-
-</p>{{ end }}
+<h1>Test</h1>
+<p>
+    {{ .Variable }}
+</p>
+{{ range .Items }}
+<p>
+    {{ . }}
+</p>
+{{ end }}

1 file would be updated."""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1

    result = runner.invoke(djlint, ["tests/config_pragmas/html_five.html", "--check"])
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
        djlint, ["tests/config_pragmas/html_six.html", "--check", "--profile", "django"]
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
