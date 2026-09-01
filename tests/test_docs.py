"""Test that the docs show what djLint actually does.

uv run pytest tests/test_docs.py
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import yaml

from djlint.lint import linter
from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import printer

if TYPE_CHECKING:
    from typing_extensions import Any

_LINTER_DOCS = Path("docs/src/docs/linter.md")
_FORMATTER_DOCS = tuple(sorted(Path("docs/src").rglob("formatter.md")))
_RULES_FILE = Path("src/djlint/rules.yaml")
_RULE_SECTION_PATTERN = re.compile(r"^#### ([A-Z]\d{3})\s*$", re.MULTILINE)
_EXAMPLE_LABEL_PATTERN = re.compile(r"^(Don't|Do):\s*$", re.MULTILINE)
_CODE_BLOCK_PATTERN = re.compile(r"```\w*\n(.*?)```", re.DOTALL)
_SHOWN_OUTPUT_PATTERN = re.compile(
    r"<!-- prettier-ignore -->\n```html\n(.*?)```", re.DOTALL
)
_PROFILE_BY_LETTER = {
    "D": "django",
    "J": "jinja",
    "M": "handlebars",
    "N": "nunjucks",
}
_PROFILES = (
    "django",
    "jinja",
    "nunjucks",
    "handlebars",
    "golang",
    "liquid",
    "html",
)


def _rules() -> dict[str, Any]:
    return {
        entry["rule"]["name"]: entry["rule"]
        for entry in yaml.safe_load(_RULES_FILE.read_text(encoding="utf-8"))
    }


def _rule_profile(rule: dict[str, Any]) -> str:
    """A profile the rule runs under, preferring the one it is named for."""
    excluded = set(rule.get("exclude") or ())
    named = _PROFILE_BY_LETTER.get(rule["name"][0])
    if named and named not in excluded:
        return named
    return next(profile for profile in _PROFILES if profile not in excluded)


def _documented_examples() -> list[tuple[str, str, str, str]]:
    rules = _rules()
    sections = _RULE_SECTION_PATTERN.split(
        _LINTER_DOCS.read_text(encoding="utf-8")
    )[1:]
    examples = []
    for code, body in zip(sections[::2], sections[1::2], strict=True):
        profile = _rule_profile(rules[code])
        parts = _EXAMPLE_LABEL_PATTERN.split(body)
        for label, chunk in zip(parts[1::2], parts[2::2], strict=True):
            block = _CODE_BLOCK_PATTERN.search(chunk)
            if block:
                examples.append((code, profile, label, block.group(1)))
    return examples


examples = _documented_examples()


def test_every_rule_is_documented() -> None:
    assert {code for code, _, _, _ in examples} == set(_rules())


@pytest.mark.parametrize(
    ("code", "profile", "label", "sample"),
    examples,
    ids=[f"{code}-{label}" for code, _, label, _ in examples],
)
def test_documented_example(
    code: str, profile: str, label: str, sample: str
) -> None:
    config = Config("dummy/source.html", profile=profile, include=code)
    reported = any(
        finding["code"] == code
        for findings in linter(
            config, sample, "dummy/source.html", "source.html"
        ).values()
        for finding in findings
    )

    assert reported == (label == "Don't"), (
        f"{_LINTER_DOCS} shows this under {label!r} for {code}:\n{sample}"
    )


@pytest.mark.parametrize(
    "path",
    _FORMATTER_DOCS,
    ids=[path.parent.as_posix() for path in _FORMATTER_DOCS],
)
def test_formatter_example(path: Path) -> None:
    """The page's first block, formatted, has to give each block below it."""
    source, *outputs = _SHOWN_OUTPUT_PATTERN.findall(
        path.read_text(encoding="utf-8")
    )

    for expected, one_per_line in zip(outputs, (False, True), strict=True):
        config = Config(
            "dummy/source.html",
            profile="django",
            single_attribute_per_line=one_per_line,
        )
        output = formatter(config, source)

        printer(expected, source, output)
        assert output == expected
