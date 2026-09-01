"""Test that the readme's example still shows what djLint does.

uv run pytest tests/test_readme.py
"""

from __future__ import annotations

import re
from pathlib import Path

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import printer

_README = Path("README.md")
_DJANGO_BLOCK_PATTERN = re.compile(r"```django\n(.*?)\n```", re.DOTALL)


def test_readme_example_is_what_the_formatter_writes() -> None:
    blocks = _DJANGO_BLOCK_PATTERN.findall(_README.read_text(encoding="utf-8"))
    assert len(blocks) == 2, (
        f"expected a before and an after block in {_README}"
    )

    source, expected = (f"{block}\n" for block in blocks)
    config = Config("dummy/source.html", single_attribute_per_line=True)
    output = formatter(config, source)

    printer(expected, source, output)
    assert output == expected
