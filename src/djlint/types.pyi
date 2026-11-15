import sys
from typing import NotRequired, type_check_only

from typing_extensions import TypedDict

if sys.version_info >= (3, 14):
    from typing import Protocol
else:
    from typing_extensions import Protocol

@type_check_only
class LintError(TypedDict):
    code: str
    line: str
    end: NotRequired[str]
    match: str
    message: str

@type_check_only
class ProcessResult(TypedDict, total=False):
    format_message: dict[str, tuple[str, ...]]
    lint_message: dict[str, list[LintError]]

@type_check_only
class SpanMatch(Protocol):
    def span(self) -> tuple[int, int]: ...
