"""Test that each file gets the .editorconfig settings of its own path.

uv run pytest tests/test_config/test_editorconfig_per_file.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint._cli import main as djlint  # noqa: PLC2701
from djlint.settings import Config, _EditorConfigGlob  # noqa: PLC2701

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


def test_a_file_s_config_does_not_read_the_current_folder(
    project: Path, tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = Config(str(project))
    elsewhere = tmp_path_factory.mktemp("elsewhere")
    (elsewhere / ".git").mkdir()
    (elsewhere / "djlint.toml").write_text("indent = [\n", encoding="utf-8")
    monkeypatch.chdir(elsewhere)

    assert config.for_file(project / "web" / "index.html").indent_size == 2


def test_a_file_of_another_project_reads_that_project_s_editorconfig(
    project: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    other = tmp_path_factory.mktemp("other")
    (other / ".git").mkdir()
    (other / ".editorconfig").write_text("[*]\nindent_size = 2\n", encoding="utf-8")
    (other / "templates").mkdir()

    config = Config(str(project))

    assert config.for_file(other / "templates" / "index.html").indent_size == 2


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
        ("pages/**/*.html", ["pages/a.html", "pages/x/y/a.html"], ["a.html", "x/pages/a.html"]),
        ("**/a.html", ["a.html", "x/y/a.html"], ["b.html"]),
        ("*.{html,jinja}", ["a.html", "a.jinja"], ["a.txt"]),
        ("a{1..3}.html", ["a1.html", "a3.html", "a+2.html"], ["a4.html", "a0.html"]),
        ("a{-3..-1}.html", ["a-2.html"], ["a-4.html", "a1.html"]),
        (
            "page{1000..9999}.html",
            ["page1000.html", "page9999.html"],
            ["page10.html", "page10000.html", "page01000.html"],
        ),
        ("{{1..3},index}.html", ["2.html", "index.html"], ["4.html", "{index}.html"]),
        ("{a,{b}}.html", ["a.html", "{b}.html"], ["b.html"]),
        (r"{a\,b}.html", ["{a,b}.html"], ["a,b.html"]),
        ("{[a,b]}.html", ["{a}.html", "{,}.html"], ["a.html"]),
        ("a[*/]b.html", ["a[*/]b.html"], ["a[xyz/]b.html", "a*b.html"]),
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
    section = _EditorConfigGlob(glob)

    assert [path for path in matches if not section.matches(path)] == []
    assert [path for path in misses if section.matches(path)] == []


def test_a_later_section_wins_within_a_file(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".editorconfig").write_text(
        "[*.html]\nindent_size = 2\n\n[*]\nindent_size = 3\n", encoding="utf-8"
    )

    assert Config(str(tmp_path)).for_file(tmp_path / "a.html").indent_size == 3


# The glob tests of the EditorConfig core libraries, from
# https://github.com/editorconfig/editorconfig-core-test/tree/master/glob:
# each file's sections, then the keys a file name gets from them.
_CORE_FILES = {
    "star": [("a*e.c", "key"), ("Bar/*", "keyb"), ("*", "keyc")],
    "question": [("som?.c", "key")],
    "brackets": [
        ("[ab].a", "choice"),
        ("[!ab].b", "choice=false"),
        ("[d-g].c", "range"),
        ("[!d-g].d", "range=false"),
        ("[abd-g].e", "range_and_choice"),
        ("[-ab].f", "choice_with_dash"),
        (r"[\]ab].g", "close_inside"),
        ("[ab]].g", "close_outside"),
        (r"[!\]ab].g", "close_inside=false"),
        ("[!ab]].g", "close_outside=false"),
        ("ab[e/]cd.i", "slash_inside"),
        ("ab[/c", "slash_half_open"),
    ],
    "braces": [
        ("*.{py,js,html}", "choice"),
        ("{single}.b", "choice=single"),
        ("{}.c", "empty=all"),
        ("a{b,c,}.d", "empty=word"),
        ("a{,b,,c,}.e", "empty=words"),
        ("{.f", "closing=false"),
        ("{word,{also},this}.g", "nested"),
        ("{{a,b},c}.k", "nested_start"),
        ("{a,{b,c}}.l", "nested_end"),
        ("{},b}.h", "closing=inside"),
        ("{{,b,c{d}.i", "unmatched"),
        (r"{a\,b,cd}.txt", "comma"),
        (r"{e,\},f}.txt", "closing"),
        (r"{g,\\,i}.txt", "backslash"),
        ("{some,a{*c,b}[ef]}.j", "patterns"),
        ("{3..120}", "number"),
        ("{aardvark..antelope}", "words"),
    ],
    "star_star": [
        ("a**z.c", "key1"),
        ("b/**z.c", "key2"),
        ("c**/z.c", "key3"),
        ("d/**/z.c", "key4"),
    ],
    "utf8char": [("中文.txt", "key")],
}
_CORE_CASES = [
    ("star", "ace.c", {"key", "keyc"}),
    ("star", "ae.c", {"key", "keyc"}),
    ("star", "abcde.c", {"key", "keyc"}),
    ("star", "a/e.c", {"keyc"}),
    ("star", "Bar/foo.txt", {"keyb", "keyc"}),
    ("star", "Bar/.editorconfig", {"keyb", "keyc"}),
    ("star", ".editorconfig", {"keyc"}),
    ("star", "bat/Bar/foo.txt", {"keyc"}),
    ("star", "bat/Bar/.editorconfig", {"keyc"}),
    ("question", "some.c", {"key"}),
    ("question", "som.c", set()),
    ("question", "something.c", set()),
    ("question", "som/.c", set()),
    ("brackets", "].g", {"close_inside"}),
    ("brackets", "b].g", {"close_outside"}),
    ("brackets", "c.g", {"close_inside=false"}),
    ("brackets", "c].g", {"close_outside=false"}),
    ("brackets", "a.a", {"choice"}),
    ("brackets", "c.a", set()),
    ("brackets", "c.b", {"choice=false"}),
    ("brackets", "a.b", set()),
    ("brackets", "f.c", {"range"}),
    ("brackets", "h.c", set()),
    ("brackets", "h.d", {"range=false"}),
    ("brackets", "f.d", set()),
    ("brackets", "e.e", {"range_and_choice"}),
    ("brackets", "-.f", {"choice_with_dash"}),
    ("brackets", "ab/cd.i", set()),
    ("brackets", "abecd.i", set()),
    ("brackets", "ab[e/]cd.i", {"slash_inside"}),
    ("brackets", "ab[/c", {"slash_half_open"}),
    ("braces", "test.py", {"choice"}),
    ("braces", "test.js", {"choice"}),
    ("braces", "test.html", {"choice"}),
    ("braces", "test.pyc", set()),
    ("braces", "{single}.b", {"choice=single"}),
    ("braces", ".b", set()),
    ("braces", "{}.c", {"empty=all"}),
    ("braces", ".c", set()),
    ("braces", "a.d", {"empty=word"}),
    ("braces", "ab.d", {"empty=word"}),
    ("braces", "ac.d", {"empty=word"}),
    ("braces", "a,.d", set()),
    ("braces", "a.e", {"empty=words"}),
    ("braces", "ab.e", {"empty=words"}),
    ("braces", "ac.e", {"empty=words"}),
    ("braces", "a,.e", set()),
    ("braces", "{.f", {"closing=false"}),
    ("braces", ".f", set()),
    ("braces", "word,this}.g", set()),
    ("braces", "{also,this}.g", set()),
    ("braces", "word.g", {"nested"}),
    ("braces", "{also}.g", {"nested"}),
    ("braces", "this.g", {"nested"}),
    ("braces", "{{a,b},c}.k", set()),
    ("braces", "{a,b}.k", set()),
    ("braces", "a.k", {"nested_start"}),
    ("braces", "b.k", {"nested_start"}),
    ("braces", "c.k", {"nested_start"}),
    ("braces", "{a,{b,c}}.l", set()),
    ("braces", "{b,c}.l", set()),
    ("braces", "a.l", {"nested_end"}),
    ("braces", "b.l", {"nested_end"}),
    ("braces", "c.l", {"nested_end"}),
    ("braces", "{},b}.h", {"closing=inside"}),
    ("braces", "{{,b,c{d}.i", {"unmatched"}),
    ("braces", "{.i", set()),
    ("braces", "b.i", set()),
    ("braces", "c{d.i", set()),
    ("braces", ".i", set()),
    ("braces", "a,b.txt", {"comma"}),
    ("braces", "a.txt", set()),
    ("braces", "cd.txt", {"comma"}),
    ("braces", "e.txt", {"closing"}),
    ("braces", "}.txt", {"closing"}),
    ("braces", "f.txt", {"closing"}),
    ("braces", "g.txt", {"backslash"}),
    ("braces", r"\.txt", {"backslash"}),
    ("braces", "i.txt", {"backslash"}),
    ("braces", "some.j", {"patterns"}),
    ("braces", "abe.j", {"patterns"}),
    ("braces", "abf.j", {"patterns"}),
    ("braces", "abg.j", set()),
    ("braces", "ace.j", {"patterns"}),
    ("braces", "acf.j", {"patterns"}),
    ("braces", "acg.j", set()),
    ("braces", "abce.j", {"patterns"}),
    ("braces", "abcf.j", {"patterns"}),
    ("braces", "abcg.j", set()),
    ("braces", "ae.j", set()),
    ("braces", ".j", set()),
    ("braces", "1", set()),
    ("braces", "3", {"number"}),
    ("braces", "15", {"number"}),
    ("braces", "60", {"number"}),
    ("braces", "5a", set()),
    ("braces", "120", {"number"}),
    ("braces", "121", set()),
    ("braces", "060", set()),
    ("braces", "{aardvark..antelope}", {"words"}),
    ("braces", "a", set()),
    ("braces", "aardvark", set()),
    ("braces", "agreement", set()),
    ("braces", "antelope", set()),
    ("braces", "antimatter", set()),
    ("utf8char", "中文.txt", {"key"}),
    *(
        ("star_star", name, {"key1"})
        for name in ("a/z.c", "amnz.c", "am/nz.c", "a/mnz.c", "amn/z.c", "a/mn/z.c")
    ),
    *(("star_star", name, {"key2"}) for name in ("b/z.c", "b/mnz.c", "b/mn/z.c")),
    *(("star_star", name, set()) for name in ("bmnz.c", "bm/nz.c", "bmn/z.c")),
    *(("star_star", name, {"key3"}) for name in ("c/z.c", "cmn/z.c", "c/mn/z.c")),
    *(("star_star", name, set()) for name in ("cmnz.c", "cm/nz.c", "c/mnz.c")),
    *(("star_star", name, {"key4"}) for name in ("d/z.c", "d/mn/z.c")),
    *(("star_star", name, set()) for name in ("dmnz.c", "dm/nz.c", "d/mnz.c", "dmn/z.c")),
]


@pytest.mark.parametrize(("file", "name", "keys"), _CORE_CASES)
def test_the_globs_pass_the_editorconfig_core_tests(file: str, name: str, keys: set[str]) -> None:
    found = {key for glob, key in _CORE_FILES[file] if _EditorConfigGlob(glob).matches(name)}

    assert found == keys
