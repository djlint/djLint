"""Test what the docs gave before: the imports of a custom rule, and the calls of djlint.api.

uv run pytest tests/test_deprecated.py
"""

from __future__ import annotations

import re
import sys
from typing import TYPE_CHECKING

import pytest

from djlint import _helpers, _lint, settings
from djlint.api import Config, format_text, is_excluded, lint_text, load_config

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from djlint.api import Finding

_HTML = "{# djlint:off H025 #}<p>{# djlint:on #}"
_LINE_ENDS = ({"start": 0, "end": len(_HTML)},)


def test_get_line() -> None:
    from djlint.lint import get_line  # noqa: PLC0415

    with pytest.warns(FutureWarning, match=r"Import get_line from djlint.api") as record:
        # The old functions still take their arguments by keyword.
        assert get_line(start=3, line_ends=_LINE_ENDS) == _lint.get_line(3, _LINE_ENDS)

    assert record[0].filename == __file__


def test_inside_ignored_rule() -> None:
    from djlint.helpers import inside_ignored_rule  # noqa: PLC0415

    config = load_config()
    match = re.search(r"<p>", _HTML)
    assert match is not None

    with pytest.warns(FutureWarning, match=r"Import inside_ignored_rule from djlint.api"):
        ignored = inside_ignored_rule(config=config, html=_HTML, match=match, rule="H025")

    assert ignored is _helpers.inside_ignored_rule(config, _HTML, match, "H025")


def test_inside_ignored_linter_block() -> None:
    from djlint.helpers import inside_ignored_linter_block  # noqa: PLC0415

    config = load_config()
    match = re.search(r"<p>", _HTML)
    assert match is not None

    with pytest.warns(FutureWarning, match=r"Import inside_ignored_linter_block from djlint.api"):
        ignored = inside_ignored_linter_block(config, _HTML, match)

    assert ignored is _helpers.inside_ignored_linter_block(config, _HTML, match)


def test_config() -> None:
    with pytest.warns(FutureWarning, match=r"import Config from djlint.api") as record:
        from djlint.settings import Config as OldConfig  # noqa: PLC0415

    assert OldConfig is Config
    assert record[0].filename == __file__


def test_settings_has_nothing_else() -> None:
    with pytest.raises(AttributeError, match=r"module 'djlint.settings' has no attribute 'x'"):
        settings.x  # noqa: B018


_OLD_RULE = """\
from djlint.helpers import inside_ignored_rule
from djlint.lint import get_line


def run(rule, config, html, filepath, line_ends, *args, **kwargs):
    return [
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group(),
            "message": rule["message"],
        }
        for match in __import__("re").finditer("bad", html)
        if not inside_ignored_rule(config, html, match, rule["name"])
    ]
"""


def test_a_custom_rule_written_for_the_old_imports_still_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.delitem(sys.modules, "old_rule", raising=False)
    (tmp_path / "djlint.toml").write_text("", encoding="utf-8")
    (tmp_path / ".djlint_rules.yaml").write_text(
        "- rule:\n    name: T9001\n    message: Bad\n    python_module: old_rule\n",
        encoding="utf-8",
    )
    (tmp_path / "old_rule.py").write_text(_OLD_RULE, encoding="utf-8")
    config = load_config(tmp_path, profile="django")

    with pytest.warns(FutureWarning, match=r"from djlint.api"):
        findings = lint_text(config, "<p>bad</p>")

    assert [(finding.code, finding.line, finding.column) for finding in findings] == [
        ("T9001", 1, 3)
    ]


def test_load_config_with_folder_by_keyword(tmp_path: Path) -> None:
    (tmp_path / "djlint.toml").write_text("", encoding="utf-8")

    with pytest.warns(FutureWarning, match=r"Pass folder to load_config by position") as record:
        config = load_config(folder=tmp_path, indent=2)  # type: ignore[deprecated]

    assert record[0].filename == __file__
    assert config.project_root == tmp_path
    assert config.indent == "  "


_SOURCE = "<div><img><p>hi</p></div>"
_FORMATTED = "<div>\n    <img>\n    <p>hi</p>\n</div>\n"


def _codes(findings: list[Finding]) -> list[str]:
    return [finding.code for finding in findings]


@pytest.mark.parametrize(
    ("call", "expected", "message"),
    [
        pytest.param(
            lambda config: format_text(config=config, text=_SOURCE),  # type: ignore[deprecated]
            _FORMATTED,
            "Pass config and text to format_text by position",
            id="format_text-by-keyword",
        ),
        pytest.param(
            lambda config: format_text(config, text=_SOURCE),  # type: ignore[deprecated]
            _FORMATTED,
            "Pass config and text to format_text by position",
            id="format_text-text-by-keyword",
        ),
        pytest.param(
            lambda config: _codes(lint_text(config, _SOURCE, "emails/a.html")),  # type: ignore[deprecated]
            [],
            "Pass config and text to lint_text by position, and filename by keyword",
            id="lint_text-filename-by-position",
        ),
        pytest.param(
            lambda config: _codes(lint_text(config=config, text=_SOURCE)),  # type: ignore[deprecated]
            ["H013"],
            "Pass config and text to lint_text by position, and filename by keyword",
            id="lint_text-by-keyword",
        ),
        pytest.param(
            lambda config: is_excluded(config, path=config.project_root / "vendor" / "a.html"),  # type: ignore[deprecated]
            True,
            "Pass config and path to is_excluded by position",
            id="is_excluded-path-by-keyword",
        ),
    ],
)
def test_a_call_from_before_the_api_was_stricter(
    tmp_path: Path, call: Callable[[Config], object], expected: object, message: str
) -> None:
    (tmp_path / "djlint.toml").write_text(
        'exclude = "vendor"\nper-file-ignores = { "emails/*" = "H013" }\n', encoding="utf-8"
    )
    config = load_config(tmp_path)

    with pytest.warns(FutureWarning, match=re.escape(message)) as record:
        assert call(config) == expected

    assert len(record) == 1
    assert record[0].filename == __file__
    # The line of the lambda, rather than the line above that calls it.
    assert record[0].lineno == call.__code__.co_firstlineno


def test_a_call_no_signature_takes_raises_without_a_warning() -> None:
    config = load_config()

    with pytest.raises(TypeError, match=r"multiple values for argument 'filename'"):
        lint_text(config, "", "a.html", filename="b.html")  # type: ignore[call-overload]
