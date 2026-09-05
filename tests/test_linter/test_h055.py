"""Test linter code H055.

uv run pytest tests/test_linter/test_h055.py
"""

from __future__ import annotations

import pytest

from djlint.lint import linter
from djlint.settings import Config

test_data = [
    pytest.param(
        ('<html lang="english">'),
        (True),
        id="a language name rather than a tag",
    ),
    pytest.param(
        ('<html lang="en_US">'),
        (True),
        id="an underscore where a hyphen belongs",
    ),
    pytest.param(('<html lang="e">'), (True), id="a single letter"),
    pytest.param(('<html lang="en-">'), (True), id="a trailing hyphen"),
    pytest.param(
        ("<html lang='English (US)'>"),
        (True),
        id="a single quoted language name",
    ),
    pytest.param(
        ("<html lang=eng-lish-x-toolongsubtag9>"),
        (True),
        id="an unquoted value with a subtag over eight characters",
    ),
    pytest.param(
        ('<html class="a" lang="en--US">'),
        (True),
        id="an empty subtag after another attribute",
    ),
    pytest.param(('<html lang="en">'), (False), id="a two letter tag"),
    pytest.param(
        ('<html lang="EN">'), (False), id="the tag is read whatever its case"
    ),
    pytest.param(('<html lang="pt-BR">'), (False), id="a region subtag"),
    pytest.param(
        ('<html lang="zh-Hant-TW">'), (False), id="a script and a region subtag"
    ),
    pytest.param(('<html lang="es-419">'), (False), id="a numeric region"),
    pytest.param(('<html lang="sr-Latn">'), (False), id="a script subtag"),
    pytest.param(
        ('<html lang="{{ LANGUAGE_CODE }}">'),
        (False),
        id="a value written by a template variable",
    ),
    pytest.param(
        ('<html lang="{% get_current_language as l %}{{ l }}">'),
        (False),
        id="a value written by a template tag",
    ),
    pytest.param(
        ('<html lang="">'), (False), id="an empty value is left to H005"
    ),
    pytest.param(("<html>"), (False), id="no lang at all is left to H005"),
    pytest.param(
        ('<html xml:lang="english" lang="en">'),
        (False),
        id="xml:lang is not read as lang",
    ),
    pytest.param(
        ('<div lang="english">'), (False), id="only the html tag is checked"
    ),
    pytest.param(
        ('<p title="<html lang=bad>">'),
        (False),
        id="markup inside an attribute value is text",
    ),
]


@pytest.mark.parametrize(("source", "reported"), test_data)
def test_h055(source: str, reported: bool) -> None:
    filename = "test.html"
    config = Config(filename, profile="django")

    findings = linter(config, source, filename, filename)[filename]
    codes = [error["code"] for error in findings]

    assert ("H055" in codes) is reported
