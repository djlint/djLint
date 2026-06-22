from typing import type_check_only

from typing_extensions import Protocol, TypedDict

@type_check_only
class LintError(TypedDict):
    code: str
    line: str
    match: str
    message: str

@type_check_only
class ProcessResult(TypedDict, total=False):
    format_message: dict[str, tuple[str, ...]]
    lint_message: dict[str, list[LintError]]

@type_check_only
class SpanMatch(Protocol):
    def span(self) -> tuple[int, int]: ...
