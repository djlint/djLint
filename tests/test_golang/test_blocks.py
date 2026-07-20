"""Test golang block indentation.

uv run pytest tests/test_golang/test_blocks.py
"""

from __future__ import annotations

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        # https://github.com/djlint/djLint/issues/734
        (
            '{{ define "main" }}\n'
            "{{ if .Page }}\n"
            "{{ .Page.Title }}\n"
            "{{ end }}\n"
            "{{ end }}\n"
        ),
        (
            '{{ define "main" }}\n'
            "    {{ if .Page }}\n"
            "        {{ .Page.Title }}\n"
            "    {{ end }}\n"
            "{{ end }}\n"
        ),
        id="issue_734_define_if_blocks_indent",
    ),
    pytest.param(
        ("{{ range .Items }}\n<li>{{ .Name }}</li>\n{{ end }}\n<p>after</p>\n"),
        (
            "{{ range .Items }}\n    <li>{{ .Name }}</li>\n{{ end }}\n"
            "<p>after</p>\n"
        ),
        id="range_block",
    ),
    pytest.param(
        (
            "{{ if .A }}\n<p>a</p>\n{{ else if .B }}\n<p>b</p>\n"
            "{{ else }}\n<p>c</p>\n{{ end }}\n"
        ),
        (
            "{{ if .A }}\n    <p>a</p>\n{{ else if .B }}\n    <p>b</p>\n"
            "{{ else }}\n    <p>c</p>\n{{ end }}\n"
        ),
        id="else_and_else_if_branches",
    ),
    pytest.param(
        (
            "{{ with .User }}\n{{ .Name }}\n{{ end }}\n"
            '{{ block "sidebar" . }}\n<p>x</p>\n{{ end }}\n'
        ),
        (
            "{{ with .User }}\n    {{ .Name }}\n{{ end }}\n"
            '{{ block "sidebar" . }}\n    <p>x</p>\n{{ end }}\n'
        ),
        id="with_and_block_pairs",
    ),
    pytest.param(
        (
            "{{ if .Ok }}yes{{ end }}\n<p>after</p>\n"
            "{{ with .User }}{{ .Name }}{{ end }}\n<p>tail</p>\n"
        ),
        (
            "{{ if .Ok }}yes{{ end }}\n<p>after</p>\n"
            "{{ with .User }}{{ .Name }}{{ end }}\n<p>tail</p>\n"
        ),
        id="single_line_pairs_do_not_leak_indent",
    ),
    pytest.param(
        ("{{- if .Page }}\n<p>x</p>\n{{- end }}\n"),
        ("{{- if .Page }}\n    <p>x</p>\n{{- end }}\n"),
        id="whitespace_control_blocks",
    ),
    pytest.param(
        ('{{ template "footer" . }}\n{{ .Title }}\n{{ .end }}\n{{ ends }}\n'),
        ('{{ template "footer" . }}\n{{ .Title }}\n{{ .end }}\n{{ ends }}\n'),
        id="single_tags_and_end_lookalikes_untouched",
    ),
    pytest.param(
        (
            "{{ with .U }}\n{{ if .A }}\n<p>a</p>\n{{ end }}{{ if .B }}\n"
            "<p>b</p>\n{{ end }}\n{{ end }}\n"
        ),
        (
            "{{ with .U }}\n    {{ if .A }}\n        <p>a</p>\n"
            "    {{ end }}{{ if .B }}\n        <p>b</p>\n    {{ end }}\n"
            "{{ end }}\n"
        ),
        id="glued_end_and_opener_keep_stack_in_sync",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_formatter(source: str, expected: str) -> None:
    output = formatter(config_builder({"profile": "golang"}), source)

    printer(expected, source, output)
    assert expected == output
