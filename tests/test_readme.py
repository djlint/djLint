"""Test that the readme's example still shows what djLint does.

uv run pytest tests/test_readme.py
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import printer

_README = Path("README.md")
_DJANGO_BLOCK_PATTERN = re.compile(r"```django\n(.*?)\n```", re.DOTALL)


def _blocks() -> list[str]:
    blocks = _DJANGO_BLOCK_PATTERN.findall(_README.read_text(encoding="utf-8"))
    assert len(blocks) == 3, f"expected a before, an after and a flag block in {_README}"
    return [f"{block}\n" for block in blocks]


def test_readme_example_is_what_the_formatter_writes() -> None:
    source, expected, _ = _blocks()
    output = formatter(Config("dummy/source.html"), source)

    printer(expected, source, output)
    assert output == expected


def test_readme_flag_example_is_the_tag_the_flag_writes() -> None:
    # The readme shows only the <a>, as --single-attribute-per-line lays it out.
    source, _, expected = _blocks()
    output = formatter(Config("dummy/source.html", single_attribute_per_line=True), source)
    lines = output.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.strip() == "<a")
    end = next(i for i in range(start, len(lines)) if lines[i].rstrip().endswith("</a>"))

    assert dedent("".join(lines[start : end + 1])) == expected
