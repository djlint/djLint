"""Test that each file gets the .editorconfig settings of its own path.

uv run pytest tests/test_config/test_editorconfig_per_file.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import regex as re

from djlint._cli import main as djlint  # noqa: PLC2701
from djlint.settings import Config, _editorconfig_regex  # noqa: PLC2701

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


@pytest.fixture
def project(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".editorconfig").write_text("[*]\nindent_size = 3\n", encoding="utf-8")
    (tmp_path / "web" / "pages").mkdir(parents=True)
    (tmp_path / "web" / ".editorconfig").write_text(
        "[*.html]\nindent_size = 2\n\n[pages/*.html]\nindent_size = 6\nmax_line_length = 80\n",
        encoding="utf-8",
    )
    return tmp_path


def test_a_run_from_the_root_gives_each_file_its_own(project: Path) -> None:
    config = Config(str(project))

    assert config.for_file(project / "index.html").indent_size == 3
    assert config.for_file(project / "web" / "index.html").indent_size == 2
    nested = config.for_file(project / "web" / "pages" / "index.html")
    assert (nested.indent_size, nested.max_line_length) == (6, 80)


def test_the_command_line_and_the_configuration_win(project: Path) -> None:
    file = project / "web" / "pages" / "index.html"

    assert Config(str(project), indent=5).for_file(file).indent_size == 5
    (project / "djlint.toml").write_text("max_line_length = 100\n", encoding="utf-8")
    config = Config(str(project)).for_file(file)
    assert (config.indent_size, config.max_line_length) == (6, 100)


def test_a_file_with_the_settings_of_the_run_is_the_same_config(project: Path) -> None:
    config = Config(str(project))

    assert config.for_file(project / "other.html") is config


def test_a_directory_run_formats_each_file_by_its_editorconfig(
    runner: CliRunner, project: Path
) -> None:
    for file in (project / "index.html", project / "web" / "pages" / "index.html"):
        file.write_text("<div>\n<p>x</p>\n</div>\n", encoding="utf-8")

    runner.invoke(djlint, [str(project), "--reformat", "--quiet"])

    assert (project / "index.html").read_text(encoding="utf-8") == ("<div>\n   <p>x</p>\n</div>\n")
    assert (project / "web" / "pages" / "index.html").read_text(encoding="utf-8") == (
        "<div>\n      <p>x</p>\n</div>\n"
    )


def test_stdin_takes_the_editorconfig_of_its_filename(runner: CliRunner, project: Path) -> None:
    result = runner.invoke(
        djlint,
        ["-", "--reformat", "--stdin-filename", str(project / "web" / "index.html")],
        input="<div>\n<p>x</p>\n</div>\n",
    )

    assert result.stdout.startswith("<div>\n  <p>x</p>\n</div>")


@pytest.mark.parametrize(
    ("glob", "matches", "misses"),
    [
        ("*", ["a.html", "x/a.html"], []),
        ("*.html", ["a.html", "x/y/a.html"], ["a.jinja"]),
        ("pages/*.html", ["pages/a.html"], ["a.html", "x/pages/a.html", "pages/x/a.html"]),
        ("/pages/*.html", ["pages/a.html"], ["x/pages/a.html"]),
        ("pages/**.html", ["pages/x/y/a.html"], ["a.html"]),
        ("*.{html,jinja}", ["a.html", "a.jinja"], ["a.txt"]),
        ("a{1..3}.html", ["a1.html", "a3.html"], ["a4.html"]),
        ("[!b]*.html", ["a.html"], ["b.html"]),
        ("[ab].html", ["a.html", "b.html"], ["c.html"]),
        ("{single}.html", ["{single}.html"], ["single.html"]),
        ("a\\*.html", ["a*.html"], ["ab.html"]),
        ("?.html", ["a.html"], ["ab.html", "/.html"]),
    ],
)
def test_section_globs_follow_the_editorconfig_specification(
    glob: str, matches: list[str], misses: list[str]
) -> None:
    pattern = re.compile(_editorconfig_regex(glob))

    assert [path for path in matches if not pattern.fullmatch(path)] == []
    assert [path for path in misses if pattern.fullmatch(path)] == []


def test_a_later_section_wins_within_a_file(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".editorconfig").write_text(
        "[*.html]\nindent_size = 2\n\n[*]\nindent_size = 3\n", encoding="utf-8"
    )

    assert Config(str(tmp_path)).for_file(tmp_path / "a.html").indent_size == 3
