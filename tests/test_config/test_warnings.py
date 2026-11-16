"""Test the warnings about settings that would not do what they look like.

uv run pytest tests/test_config/test_warnings.py
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from click import UsageError

from djlint.settings import _SETTINGS, Config, _warn_once  # noqa: PLC2701

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any


@pytest.fixture(autouse=True)
def _fresh_warnings() -> None:
    _warn_once.cache_clear()


def _warnings(capsys: pytest.CaptureFixture[str]) -> list[str]:
    return [line.removeprefix("Warning: ") for line in capsys.readouterr().err.splitlines()]


def _settings_read() -> set[str]:
    """The names Config reads from a configuration file, from its source."""
    source = Path("src/djlint/settings.py").read_text(encoding="utf-8")
    return {
        str(node.args[0].value)
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call)
        and ast.unparse(node.func) in {"djlint_settings.get", "setting_bool", "setting_int"}
        and isinstance(node.args[0], ast.Constant)
    }


def test_the_known_settings_are_the_ones_djlint_reads() -> None:
    assert _settings_read() == _SETTINGS


@pytest.mark.parametrize(
    ("settings", "expected"),
    [
        pytest.param(
            '{"max_line_lenght": 100}',
            ".djlintrc sets max_line_lenght, which is not a djLint setting."
            " Did you mean max_line_length?",
            id="misspelled",
        ),
        pytest.param(
            '{"max-line-length": 100}',
            ".djlintrc sets max-line-length, which is not a djLint setting."
            " Did you mean max_line_length?",
            id="dashes",
        ),
        pytest.param(
            '{"per_file_ignores": {}}',
            ".djlintrc sets per_file_ignores, which is not a djLint setting."
            " Did you mean per-file-ignores?",
            id="underscores",
        ),
        pytest.param(
            '{"colour": true}',
            ".djlintrc sets colour, which is not a djLint setting.",
            id="nothing close",
        ),
    ],
)
def test_a_setting_djlint_does_not_know(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], settings: str, expected: str
) -> None:
    (tmp_path / ".djlintrc").write_text(settings, encoding="utf-8")

    Config(str(tmp_path))

    assert _warnings(capsys) == [expected]


def test_a_misspelled_setting_names_its_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[tool.djlint]\nignore_cases = true\n", encoding="utf-8"
    )

    Config(str(tmp_path))

    assert _warnings(capsys) == [
        "pyproject.toml sets ignore_cases, which is not a djLint setting. Did you mean ignore_case?"
    ]


def test_well_formed_settings_say_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / ".djlintrc").write_text(
        """{
          "profile": "django",
          "ignore": ["H006", "T027"],
          "include": "H017",
          "format_css": true,
          "css": {"indent_size": 2},
          "per-file-ignores": {"base.html": ["H030", "H025"]}
        }""",
        encoding="utf-8",
    )

    Config(str(tmp_path))

    assert not capsys.readouterr().err


@pytest.mark.parametrize(
    ("options", "expected"),
    [
        pytest.param(
            {"ignore": "H006,H999"}, ["ignore names H999, which is not a linter rule."], id="ignore"
        ),
        pytest.param(
            {"include": "h017"},
            ["include names h017, which is not a linter rule. Did you mean H017?"],
            id="lowercase",
        ),
        pytest.param(
            {"per_file_ignores": (("base.html", "H030,X1"),)},
            ["per-file-ignores names X1, which is not a linter rule."],
            id="per-file-ignores",
        ),
        pytest.param(
            {"ignore": "H006", "include": "H006"},
            ["H006 is in both ignore and include, so it stays off."],
            id="ignored and included",
        ),
        pytest.param(
            {"profile": "django", "include": "T028"},
            ["include names T028, which never runs under the django profile."],
            id="included but left out by the profile",
        ),
    ],
)
def test_rule_codes_that_would_do_nothing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    options: Mapping[str, Any],
    expected: list[str],
) -> None:
    Config(str(tmp_path), **options)

    assert _warnings(capsys) == expected


def test_a_custom_rule_is_a_known_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / ".djlint_rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: Mine\n    patterns: ['x']\n", encoding="utf-8"
    )

    Config(str(tmp_path), ignore="X001")

    assert not capsys.readouterr().err


@pytest.mark.parametrize(
    ("options", "settings", "expected"),
    [
        pytest.param(
            {"indent_css": 2},
            "{}",
            "--indent-css and the css settings have no effect without format_css.",
            id="indent_css",
        ),
        pytest.param(
            {},
            '{"js": {"indent_size": 2}}',
            "--indent-js and the js settings have no effect without format_js.",
            id="js table",
        ),
        pytest.param(
            {"format_attribute_js_json_min_props": 3},
            "{}",
            "format_attribute_js_json_min_props has no effect without format_attribute_js_json.",
            id="min props",
        ),
        pytest.param(
            {},
            '{"format_attribute_js_json_pattern": "^x-", "format_attribute_js_json_min_props": 3}',
            "format_attribute_js_json_pattern and format_attribute_js_json_min_props have"
            " no effect without format_attribute_js_json.",
            id="both",
        ),
    ],
)
def test_settings_without_the_switch_they_need(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    options: Mapping[str, Any],
    settings: str,
    expected: str,
) -> None:
    (tmp_path / ".djlintrc").write_text(settings, encoding="utf-8")

    Config(str(tmp_path), **options)

    assert _warnings(capsys) == [expected]


def test_the_switch_they_need_silences_them(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    Config(
        str(tmp_path),
        format_css=True,
        indent_css=2,
        format_attribute_js_json=True,
        format_attribute_js_json_min_props=3,
    )

    assert not capsys.readouterr().err


@pytest.mark.parametrize(
    ("output_format", "message"),
    [
        pytest.param(
            "{code} {lin}",
            "Invalid linter_output_format '{code} {lin}': {lin} is not one of"
            " {code}, {end}, {filename}, {line}, {match}, {message}.",
            id="unknown field",
        ),
        pytest.param(
            "{} {code}",
            "Invalid linter_output_format '{} {code}': {} is not one of",
            id="positional",
        ),
        pytest.param("{code", "Invalid linter_output_format '{code':", id="unclosed"),
        pytest.param(
            "{message:{lin}}",
            "Invalid linter_output_format '{message:{lin}}': {lin} is not one of",
            id="in a format spec",
        ),
    ],
)
def test_an_output_format_that_would_fail(tmp_path: Path, output_format: str, message: str) -> None:
    with pytest.raises(UsageError, match=re.escape(message)):
        Config(str(tmp_path), linter_output_format=output_format)


def test_per_file_ignores_take_a_list(tmp_path: Path) -> None:
    (tmp_path / ".djlintrc").write_text(
        '{"per-file-ignores": {"base.html": ["H030", "H025"]}}', encoding="utf-8"
    )

    assert Config(str(tmp_path)).per_file_ignores == {"base.html": "H030,H025"}


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("true", True, id="true"),
        pytest.param('"true"', True, id="text true"),
        pytest.param('"Yes"', True, id="yes"),
        pytest.param('" on "', True, id="on"),
        pytest.param('"1"', True, id="text 1"),
        pytest.param("1", True, id="1"),
        pytest.param("false", False, id="false"),
        pytest.param('"false"', False, id="text false"),
        pytest.param('"NO"', False, id="no"),
        pytest.param('"off"', False, id="off"),
        pytest.param("0", False, id="0"),
    ],
)
def test_a_switch_takes_the_words_for_true_and_false(
    tmp_path: Path, value: str, expected: bool
) -> None:
    (tmp_path / ".djlintrc").write_text(
        f'{{"format_css": {value}, "require_pragma": {value}}}', encoding="utf-8"
    )

    config = Config(str(tmp_path))

    assert config.format_css is expected
    assert config.require_pragma is expected


@pytest.mark.parametrize("value", ['"maybe"', "2", '""', "[]", "null"])
def test_a_switch_refuses_other_values(tmp_path: Path, value: str) -> None:
    (tmp_path / ".djlintrc").write_text(f'{{"format_css": {value}}}', encoding="utf-8")

    with pytest.raises(
        UsageError, match=r"Invalid \.djlintrc format_css value .* It must be true or false\."
    ):
        Config(str(tmp_path))


@pytest.mark.parametrize(("value", "expected"), [("100", 100), ('"100"', 100), ("100.0", 100)])
def test_a_number_takes_a_whole_number_in_any_form(
    tmp_path: Path, value: str, expected: int
) -> None:
    (tmp_path / ".djlintrc").write_text(f'{{"max_line_length": {value}}}', encoding="utf-8")

    assert Config(str(tmp_path)).max_line_length == expected


@pytest.mark.parametrize("value", ["true", "100.5", '"100.5"', '"wide"'])
def test_a_number_refuses_other_values(tmp_path: Path, value: str) -> None:
    (tmp_path / ".djlintrc").write_text(f'{{"max_line_length": {value}}}', encoding="utf-8")

    with pytest.raises(UsageError, match="It must be a whole number"):
        Config(str(tmp_path))


def test_an_output_format_can_look_into_its_fields(tmp_path: Path) -> None:
    output_format = "{code[0]} {line:>4} {message.upper} {match!r:{line}}"

    assert Config(str(tmp_path), linter_output_format=output_format).linter_output_format == (
        output_format
    )
