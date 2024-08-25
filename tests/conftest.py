"""Djlint test config."""

from __future__ import annotations

import difflib
import shutil
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
import regex as re
from _pytest.terminal import TerminalReporter  # noqa: PLC2701
from click.testing import CliRunner
from colorama import Fore, Style

from src.djlint import main as djlint
from src.djlint.settings import Config

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    import os
    from typing import Iterator, Mapping, TextIO

    from _pytest.reports import BaseReport
    from typing_extensions import Any

    from src.djlint.lint import LintError


class MyReporter(TerminalReporter):  # type: ignore[misc]
    """Override default reporter to print more interesting details."""

    @override
    def short_test_summary(self) -> None:
        """Override summary."""
        failed = self.stats.get("failed", ())

        if failed:
            self.write_sep("=", "Short Test Summary")
            for rep in failed:
                self.write_line(f"failed {rep.nodeid}")

    @override
    def summary_failures(self) -> None:
        """Override failure printer."""
        if self.config.option.tbstyle != "no":
            reports: list[BaseReport] = self.getreports("failed")
            if not reports:
                return
            self.write_sep("=", "FAILURES")
            if self.config.option.tbstyle == "line":
                for rep in reports:
                    line: str = self._getcrashline(rep)  # type: ignore[no-untyped-call]
                    self.write_line(line)
            else:
                for rep in reports:
                    msg: str | None = self._getfailureheadline(rep)  # type: ignore[no-untyped-call]
                    self.write_sep("_", msg, red=True, bold=True)
                    # modified version of _outrep_summary()
                    # only show error if not assertion error,
                    # otherwise our print function shows the diff better.
                    if not re.search(r"AssertionError:", rep.longreprtext):
                        rep.toterminal(self._tw)
                    showcapture = self.config.option.showcapture
                    if showcapture == "no":
                        return
                    for secname, content in rep.sections:
                        if showcapture != "all" and showcapture not in secname:
                            continue
                        # self._tw.sep("-", secname)  # noqa: ERA001
                        line_content = content
                        if content[-1:] == "\n":
                            line_content = content[:-1]
                        self._tw.line(line_content)
                    # continue original code
                    self._handle_teardown_sections(rep.nodeid)


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    vanilla_reporter = config.pluginmanager.getplugin("terminalreporter")
    my_reporter = MyReporter(config)
    config.pluginmanager.unregister(vanilla_reporter)
    config.pluginmanager.register(my_reporter, "terminalreporter")


@pytest.fixture
def runner() -> CliRunner:
    """Click runner for djlint tests."""
    return CliRunner()


@pytest.fixture
def tmp_file() -> Iterator[tempfile._TemporaryFileWrapper[bytes]]:
    """Create a temp file for formatting."""
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        with tmp:
            yield tmp
    finally:
        Path(tmp.name).unlink(missing_ok=True)


def printer(expected: str, source: str, actual: str) -> None:
    width, _ = shutil.get_terminal_size()

    expected_text = "Expected"
    actual_text = "Actual"
    diff_text = "Diff"
    source_text = "Source"

    expected_width = (width - len(expected_text) - 2) // 2
    actual_width = (width - len(actual_text) - 2) // 2
    diff_width = (width - len(diff_text) - 2) // 2
    source_width = (width - len(source_text) - 2) // 2

    color = {"-": Fore.YELLOW, "+": Fore.GREEN, "@": Style.BRIGHT + Fore.BLUE}

    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * source_width} {source_text} {'─' * source_width}{Style.RESET_ALL}"
    )
    print()
    print(source)
    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * expected_width} {expected_text} {'─' * expected_width}{Style.RESET_ALL}"
    )
    print()
    print(expected)
    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * actual_width} {actual_text} {'─' * actual_width}{Style.RESET_ALL}"
    )
    print()
    print(actual)
    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * diff_width} {diff_text} {'─' * diff_width}{Style.RESET_ALL}"
    )
    print()
    for diff in tuple(
        difflib.unified_diff(expected.split("\n"), actual.split("\n"))
    )[2:]:
        print(f"{color.get(diff[:1], Style.RESET_ALL)}{diff}{Style.RESET_ALL}")


def lint_printer(
    source: str, expected: list[LintError], actual: list[LintError]
) -> None:
    width, _ = shutil.get_terminal_size()

    expected_text = "Expected Rules"
    actual_text = "Actual"
    source_text = "Source"

    expected_width = (width - len(expected_text) - 2) // 2
    actual_width = (width - len(actual_text) - 2) // 2
    source_width = (width - len(source_text) - 2) // 2

    print()
    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * source_width} {source_text} {'─' * source_width}{Style.RESET_ALL}"
    )
    print()
    print(source)
    print()

    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * expected_width} {expected_text} {'─' * expected_width}{Style.RESET_ALL}"
    )
    print()
    for x in expected:
        print(
            f"{Fore.RED}{Style.BRIGHT}{x['code']}{Style.RESET_ALL} {x['line']} {x['match']}"
        )
        print(f'     {x["message"]}')
        print()

    print(
        f"{Fore.BLUE}{Style.BRIGHT}{'─' * actual_width} {actual_text} {'─' * actual_width}{Style.RESET_ALL}"
    )
    print()

    for x in actual:
        print(
            f"{Fore.RED}{Style.BRIGHT}{x['code']}{Style.RESET_ALL} {x['line']} {x['match']}"
        )
        print(f'     {x["message"]}')
        print()
    if not actual:
        print(f"{Fore.YELLOW}No codes found.{Style.RESET_ALL}")
        print()

    else:
        print(f"{Fore.YELLOW}{actual}{Style.RESET_ALL}")
        print()


def write_to_file(the_file: str | os.PathLike[str], the_text: bytes) -> None:
    """Shortcode for write some bytes to a file."""
    Path(the_file).write_bytes(the_text)


def reformat(
    the_file: TextIO, runner: CliRunner, the_text: bytes, profile: str = "html"
) -> SimpleNamespace:
    write_to_file(the_file.name, the_text)
    result = runner.invoke(
        djlint, (the_file.name, "--profile", profile, "--reformat")
    )
    return SimpleNamespace(
        text=Path(the_file.name).read_text(encoding="utf-8"),
        exit_code=result.exit_code,
    )


def config_builder(args: Mapping[str, Any] | None = None) -> Config:
    if args:
        return Config("dummy/source.html", **args)
    return Config("dummy/source.html")


@pytest.fixture
def basic_config() -> Config:
    """Return a config object with default basic options."""
    return Config("dummy/source.html")


@pytest.fixture
def django_config() -> Config:
    """Return a config object with django profile."""
    return Config("dummy/source.html", profile="django")


@pytest.fixture
def jinja_config() -> Config:
    """Return a config object with jinja."""
    return Config("dummy/source.html", profile="jinja")


@pytest.fixture
def handlebars_config() -> Config:
    """Return a config object with handlebars."""
    return Config("dummy/source.html", profile="handlebars")


@pytest.fixture
def nunjucks_config() -> Config:
    """Return a config object with nunjucks."""
    return Config("dummy/source.html", profile="nunjucks")
