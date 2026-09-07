"""Test linter code H055.

uv run pytest tests/test_linter/test_h055.py
"""

from __future__ import annotations

import time

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
    pytest.param(
        ('<html lang="  ">'), (True), id="a value that is only whitespace"
    ),
    pytest.param(('<html lang="\n">'), (True), id="a value that is a newline"),
    pytest.param(
        ('<html lang="$LANG">'),
        (True),
        id="a value starting with a bare dollar sign",
    ),
    pytest.param(
        ('<html lang="{english}">'),
        (True),
        id="a value starting with a bare brace",
    ),
    pytest.param(
        ('<html {% if a > b %}dir="rtl"{% endif %} lang="english">'),
        (True),
        id="a greater than sign inside a template tag before the value",
    ),
    pytest.param(
        ('<html {{ "rtl" if a > b }} lang="en_US">'),
        (True),
        id="a greater than sign inside an output tag before the value",
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
        ('<html lang="${LANG}">'),
        (False),
        id="a value written by a shell style substitution",
    ),
    pytest.param(
        ('<html lang="<?= $lang ?>">'),
        (False),
        id="a value written by a php short echo tag",
    ),
    pytest.param(
        ('<html lang="<? echo $l; ?>">'),
        (False),
        id="a value written by a php short open tag",
    ),
    pytest.param(
        ('<html lang=" en ">'),
        (False),
        id="whitespace around a tag is not part of it",
    ),
    pytest.param(
        ('<html lang="en'), (False), id="a tag whose closing quote is missing"
    ),
    pytest.param(
        ("<html lang=en"), (False), id="an unquoted tag at the end of the file"
    ),
    pytest.param(
        ('<html {% if a > b %}dir="rtl"{% endif %} lang="pt-BR">'),
        (False),
        id="a tag read past a template tag holding a greater than sign",
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


def test_h055_walks_unclosed_tags_once() -> None:
    """A tag left open must not send the scan over the rest of the file."""
    config = Config("test.html", profile="django")
    pattern = next(
        entry["rule"]["compiled_patterns"][0]
        for entry in config.linter_rules
        if entry["rule"]["name"] == "H055"
    )
    source = '<html a="b" ' * 3000

    start = time.perf_counter()
    match = pattern.search(source)

    assert match is None
    assert time.perf_counter() - start < 2
