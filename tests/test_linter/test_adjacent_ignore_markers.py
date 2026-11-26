"""Test that an empty djlint:off region hides nothing after it.

uv run pytest tests/test_linter/test_adjacent_ignore_markers.py
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from djlint.reformat import formatter
from djlint.settings import Config
from tests.conftest import linter

if TYPE_CHECKING:
    import pytest

_MARKERS = "<!-- djlint:off --><!-- djlint:on -->\n"


def test_the_linter_checks_the_code_after_the_markers() -> None:
    config = Config("dummy/source.html")
    html = f'{_MARKERS}<img src="a.png">\n'

    errors = linter(config, html, "dummy/source.html", "dummy/source.html")["dummy/source.html"]

    assert "H013" in {error["code"] for error in errors}


def test_the_formatter_formats_the_code_after_the_markers() -> None:
    config = Config("dummy/source.html")

    output = formatter(config, f"{_MARKERS}<div><p>y</p></div>\n")

    assert output == f"{_MARKERS}<div>\n    <p>y</p>\n</div>\n"


def test_an_editorconfig_that_cannot_be_read_is_left_out(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".editorconfig").write_text("[*]\nindent_size = 2\n", encoding="utf-8")
    read_text = Path.read_text

    def refuse(self: Path, encoding: str | None = None, errors: str | None = None) -> str:
        if self.name == ".editorconfig":
            raise PermissionError(self)
        return read_text(self, encoding=encoding, errors=errors)

    monkeypatch.setattr(Path, "read_text", refuse)

    assert Config(str(tmp_path)).indent_size == 4
