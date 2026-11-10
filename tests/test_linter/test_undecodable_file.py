"""A file that is not valid UTF-8 is reported, not a crash.

uv run pytest tests/test_linter/test_undecodable_file.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from djlint._cli import main as djlint  # noqa: PLC2701

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


def test_lint_reports_non_utf8_file_instead_of_crashing(
    runner: CliRunner, tmp_path: Path
) -> None:
    bad = tmp_path / "bad.html"
    bad.write_bytes(b"<div>\xff\xfe not utf-8</div>\n")
    result = runner.invoke(djlint, (str(bad), "--lint"))
    assert result.exit_code == 1
    assert "Traceback" not in result.output
    assert "UTF-8" in result.output
