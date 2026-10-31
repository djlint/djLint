"""Test the Python API.

uv run pytest tests/test_api.py
"""

from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

from djlint.api import Finding, format_text, lint_text, load_config

if TYPE_CHECKING:
    from pathlib import Path

_RULE = """\
- rule:
    name: T9001
    message: From a module
    flags: re.I
    python_module: project_rule
"""
_MODULE = """\
def run(rule, config, html, filepath, line_ends, *args, **kwargs):
    return [{{
        "code": rule["name"],
        "line": {line!r},
        "match": "div",
        "message": rule["message"],
    }}]
"""


def _project(tmp_path: Path, line: object = "1:1") -> Path:
    (tmp_path / "djlint.toml").write_text("", encoding="utf-8")
    (tmp_path / ".djlint_rules.yaml").write_text(_RULE, encoding="utf-8")
    (tmp_path / "project_rule.py").write_text(
        _MODULE.format(line=line), encoding="utf-8"
    )
    return tmp_path


@pytest.fixture(autouse=True)
def _forget_rule_module(monkeypatch: pytest.MonkeyPatch) -> None:
    sys.modules.pop("project_rule", None)
    monkeypatch.setattr(sys, "path", list(sys.path))


def test_format_text_reads_the_configuration_of_the_folder(
    tmp_path: Path,
) -> None:
    sub = tmp_path / "templates"
    sub.mkdir()
    (tmp_path / "pyproject.toml").write_text(
        "[tool.djlint]\nindent = 7\n", encoding="utf-8"
    )
    config = load_config(sub)
    assert format_text(config, "<div><p>hi</p></div>") == (
        "<div>\n       <p>hi</p>\n</div>\n"
    )


def test_options_win_over_the_configuration(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text("indent = 7\n", encoding="utf-8")
    config = load_config(tmp_path, indent=2)
    assert format_text(config, "<div><p>hi</p></div>") == (
        "<div>\n  <p>hi</p>\n</div>\n"
    )


def test_lint_text_gives_positions_as_numbers_in_document_order(
    tmp_path: Path,
) -> None:
    config = load_config(tmp_path, profile="django")
    source = '<p>text</p>\n<img src="x">\n<img src="y">'
    findings = [x for x in lint_text(config, source) if x.code == "H013"]
    assert findings == [
        Finding(
            "H013",
            "Img tag should have an alt attribute.",
            '<img src="x">',
            2,
            0,
            2,
            13,
        ),
        Finding(
            "H013",
            "Img tag should have an alt attribute.",
            '<img src="y">',
            3,
            0,
            3,
            13,
        ),
    ]


def test_lint_text_matches_per_file_ignores_against_the_filename(
    tmp_path: Path,
) -> None:
    (tmp_path / "djlint.toml").write_text(
        '[per-file-ignores]\n"emails/.*" = "H013"\n', encoding="utf-8"
    )
    config = load_config(tmp_path)
    source = '<img src="x">'
    assert "H013" in {x.code for x in lint_text(config, source, "a.html")}
    assert "H013" not in {
        x.code for x in lint_text(config, source, "emails/a.html")
    }


@pytest.mark.parametrize("pragma", ["{# djlint:on #}", "<!-- djlint:on -->"])
def test_require_pragma(tmp_path: Path, pragma: str) -> None:
    config = load_config(tmp_path, profile="django", require_pragma=True)
    off = '<div><img src="x"></div>'
    on = f"{pragma}\n{off}"
    assert format_text(config, off) == off
    assert not lint_text(config, off)
    assert format_text(config, on) != on
    assert lint_text(config, on)


def test_a_rule_module_is_found_from_the_project_root(tmp_path: Path) -> None:
    config = load_config(_project(tmp_path), profile="django")
    codes = {x.code for x in lint_text(config, "<div>text</div>")}
    assert "T9001" in codes
    assert sys.path[-1] == str(config.project_root)


def test_the_project_stays_off_the_path_without_a_custom_rule(
    tmp_path: Path,
) -> None:
    config = load_config(_project(tmp_path), python_rules=False)
    lint_text(config, "<div>")
    assert str(config.project_root) not in sys.path


def test_python_rules_can_be_left_out(tmp_path: Path) -> None:
    config = load_config(
        _project(tmp_path), profile="django", python_rules=False
    )
    assert config.skipped_rules == ("T9001",)
    assert "project_rule" not in sys.modules
    findings = lint_text(config, "<div>")
    assert "project_rule" not in sys.modules
    assert {x.code for x in findings} == {"H025"}


def test_a_module_of_a_project_does_not_replace_the_standard_library(
    tmp_path: Path,
) -> None:
    """Runs in a process of its own, for what djLint first imports late."""
    (tmp_path / "pyproject.toml").write_text(
        "[tool.djlint]\n", encoding="utf-8"
    )
    (tmp_path / "html.py").write_text(
        'def unescape(text):\n    return "replaced"\n', encoding="utf-8"
    )
    code = (
        "from djlint.api import format_text, load_config\n"
        f"config = load_config({str(tmp_path)!r})\n"
        "print(format_text(config, '<div>&copy;</div>'))\n"
    )
    done = subprocess.run(  # noqa: S603
        (sys.executable, "-c", code),
        capture_output=True,
        check=True,
        encoding="utf-8",
        env={"PYTHONIOENCODING": "utf-8", "PATH": ""},
    )
    assert done.stdout.strip() == "<div>©</div>"


def test_a_rule_that_counts_lines_from_zero_still_reports(
    tmp_path: Path,
) -> None:
    config = load_config(_project(tmp_path, "0:0"), profile="django")
    (finding,) = [
        x for x in lint_text(config, "<div>text</div>") if x.code == "T9001"
    ]
    assert (finding.line, finding.end_line) == (0, 0)


def test_a_rule_can_import_a_sibling_while_it_runs(tmp_path: Path) -> None:
    project = _project(tmp_path)
    (project / "project_sibling.py").write_text(
        "LINE = '1:2'\n", encoding="utf-8"
    )
    (project / "project_rule.py").write_text(
        """\
def run(rule, config, html, filepath, line_ends, *args, **kwargs):
    from project_sibling import LINE

    return [{
        "code": rule["name"],
        "line": LINE,
        "match": "",
        "message": rule["message"],
    }]
""",
        encoding="utf-8",
    )
    config = load_config(project, profile="django")
    sys.modules.pop("project_sibling", None)
    (finding,) = [
        x for x in lint_text(config, "<div>text</div>") if x.code == "T9001"
    ]
    assert finding.column == 2


def test_an_installed_rule_keeps_the_standard_library(tmp_path: Path) -> None:
    """A project's calendar.py doesn't reach an installed rule's import."""
    project = _project(tmp_path)
    (project / "calendar.py").write_text(
        "raise RuntimeError\n", encoding="utf-8"
    )
    (project / "project_rule.py").write_text(
        "import calendar\n\n" + _MODULE.format(line="1:1"), encoding="utf-8"
    )
    sys.modules.pop("calendar", None)
    config = load_config(project, profile="django")
    assert "T9001" in {x.code for x in lint_text(config, "<div>text</div>")}


@pytest.mark.parametrize("line", ["-1:0", "1", "x", "1:x", ":1", "", 1, None])
def test_a_made_up_position_names_the_rule(
    tmp_path: Path, line: object
) -> None:
    config = load_config(_project(tmp_path, line), profile="django")
    with pytest.raises(AssertionError, match="T9001"):
        lint_text(config, "<div>text</div>")
