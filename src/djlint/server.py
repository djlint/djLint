"""A language server for editors, over stdio: `djlint --lsp`.

It speaks the Language Server Protocol 3.17 with no dependencies, because
what a server of a linter and a formatter needs of the protocol is small: keep
the open documents, report their findings, and format them.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import queue
import re
import sys
import threading
from bisect import bisect_right
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING, Any, final
from urllib.parse import unquote, urlparse

from djlint.api import format_text, lint_text, load_config
from djlint.src import is_excluded

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import BinaryIO, Final, NoReturn

    from djlint.api import Finding
    from djlint.settings import Config

Json = dict[str, Any]

_PARSE_ERROR: Final = -32700
_METHOD_NOT_FOUND: Final = -32601
_INVALID_REQUEST: Final = -32600
_SERVER_NOT_INITIALIZED: Final = -32002
_REQUEST_FAILED: Final = -32803
_REQUEST_CANCELLED: Final = -32800

_LOG_ERROR: Final = 1
_LOG_WARNING: Final = 2

_SYNC_FULL: Final = 1
_SEVERITY_WARNING: Final = 2

# Above this, a character takes two UTF-16 units.
_LAST_BMP: Final = 0xFFFF

# How long typing has to pause before an open document is linted.
_DEBOUNCE_SECONDS: Final = 0.2
_CLIENT_TIMEOUT_SECONDS: Final = 5
# Cancels of requests that have finished have nothing to clear them.
_MAX_CANCELLED: Final = 1000
# How long what's still queued gets once the client has said to exit or left,
# since a lint that doesn't end must not keep the process around.
_EXIT_GRACE_SECONDS: Final = 5
_LINT_STALE: Final[Json] = {}
_LATE_ANSWER: Final[Json] = {}

_CONFIG_FILES: Final = (
    "pyproject.toml",
    "djlint.toml",
    ".djlint.toml",
    ".djlintrc",
    ".djlint_rules.yaml",
    ".editorconfig",
    ".gitignore",
)

# Options of the command line that aren't about a template.
_NOT_SETTINGS: Final = frozenset({
    "allow_empty_input",
    "check",
    "github_output",
    "lint",
    "lsp",
    "prefer_configuration",
    "quiet",
    "reformat",
    "sarif",
    "src",
    "statistics",
    "stdin_filename",
    "version",
    "warn",
})

_PATH_SETTINGS: Final = frozenset({"configuration", "rules"})

_PROFILES: Final = {
    "angular": "angular",
    "askama": "askama",
    "askama-html": "askama",
    "django": "django",
    "django-html": "django",
    "django-txt": "django",
    "go-template": "golang",
    "go-tmpl": "golang",
    "gohtml": "golang",
    "gohtmltmpl": "golang",
    "gotmpl": "golang",
    "handlebars": "handlebars",
    "hbs": "handlebars",
    "html-nunjucks": "nunjucks",
    "html.handlebars": "handlebars",
    "htmldjango": "django",
    "hugo-html": "golang",
    "jekyll": "liquid",
    "jinja": "jinja",
    "jinja-html": "jinja",
    "jinja.html": "jinja",
    "jinja2": "jinja",
    "liquid": "liquid",
    "mustache": "handlebars",
    "njk": "nunjucks",
    "nunjucks": "nunjucks",
    "tera": "tera",
    "tera-html": "tera",
}

_LINE_END: Final = re.compile(r"\r\n|\r|\n")
_FINDING_LINE_END: Final = re.compile(r"\r?\n")
_LONE_CR: Final = re.compile(r"\r(?!\n)")
_WINDOWS_DRIVE: Final = re.compile(r"/[A-Za-z]:")
_RULE_CODE: Final = re.compile(r"[A-Z]\d{3}")
_CAMEL_HUMP: Final = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def _is_id(value: object) -> bool:
    """Tell an id of a request, which only a number or a string can be."""
    return isinstance(value, str) or (
        isinstance(value, int) and not isinstance(value, bool)
    )


def _setting_name(name: str) -> str:
    return _CAMEL_HUMP.sub("_", name).replace("-", "_").lower()


def _option_value(value: Any) -> Any:
    """Put a value of a setting in the form of the command line."""
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    if isinstance(value, dict):
        return tuple((key, _option_value(item)) for key, item in value.items())
    return value


def _line_starts(text: str) -> list[int]:
    return [0, *(match.end() for match in _LINE_END.finditer(text))]


def _finding_starts(text: str) -> list[int]:
    return [0, *(match.end() for match in _FINDING_LINE_END.finditer(text))]


def _line_text(text: str, starts: list[int], line: int) -> str:
    """Return a line without its line ending."""
    end = starts[line + 1] if line + 1 < len(starts) else len(text)
    return text[starts[line] : end].rstrip("\r\n")


def _utf16_length(text: str) -> int:
    if text.isascii():
        return len(text)
    return len(text) + sum(ord(char) > _LAST_BMP for char in text)


def _position(document: _Document, line: int, column: int) -> Json:
    """Turn a line of djLint and a column in characters into a position.

    djLint counts lines by line feeds, and the protocol by a lone CR as well.
    """
    finding_starts = document.finding_starts
    index = max(min(line, len(finding_starts)) - 1, 0)
    offset = min(finding_starts[index] + max(column, 0), len(document.text))
    line_index = bisect_right(document.starts, offset) - 1
    content = _line_text(document.text, document.starts, line_index)
    start = document.starts[line_index]
    return {
        "line": line_index,
        "character": _utf16_length(content[: offset - start]),
    }


def _diagnostic(document: _Document, finding: Finding) -> Json:
    diagnostic: Json = {
        "range": {
            "start": _position(document, finding.line, finding.column),
            "end": _position(document, finding.end_line, finding.end_column),
        },
        "severity": _SEVERITY_WARNING,
        "code": finding.code,
        "source": "djLint",
        "message": finding.message,
    }
    if _RULE_CODE.fullmatch(finding.code):
        diagnostic["codeDescription"] = {
            "href": f"https://djlint.com/docs/linter/#{finding.code.lower()}"
        }
    return diagnostic


def _edits(old: str, new: str) -> list[Json]:
    """Replace only the lines that differ, which keeps the cursor in place."""
    if old == new:
        return []
    old_starts = _line_starts(old)
    if _LONE_CR.search(old):
        return [
            {
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {
                        "line": len(old_starts) - 1,
                        "character": _utf16_length(old[old_starts[-1] :]),
                    },
                },
                "newText": new,
            }
        ]
    new_starts = _line_starts(new)
    old_lines = [
        old[start:end]
        for start, end in zip(
            old_starts, [*old_starts[1:], len(old)], strict=True
        )
    ]
    new_lines = [
        new[start:end]
        for start, end in zip(
            new_starts, [*new_starts[1:], len(new)], strict=True
        )
    ]
    limit = min(len(old_lines), len(new_lines))
    first = 0
    while first < limit and old_lines[first] == new_lines[first]:
        first += 1
    last = 0
    while last < limit - first and old_lines[-1 - last] == new_lines[-1 - last]:
        last += 1
    end_line = len(old_lines) - last
    if last == 0:
        end_line -= 1
        end = {
            "line": end_line,
            "character": _utf16_length(old_lines[end_line]),
        }
    else:
        end = {"line": end_line, "character": 0}
    return [
        {
            "range": {"start": {"line": first, "character": 0}, "end": end},
            "newText": "".join(new_lines[first : len(new_lines) - last]),
        }
    ]


@final
class _Document:
    __slots__ = ("finding_starts", "language", "starts", "text", "version")

    def __init__(self, text: str, language: str, doc_version: int) -> None:
        self.text = text
        self.language = language
        self.version = doc_version
        self.starts = _line_starts(text)
        self.finding_starts = _finding_starts(text)

    def replace(self, text: str, doc_version: int) -> None:
        self.text = text
        self.version = doc_version
        self.starts = _line_starts(text)
        self.finding_starts = _finding_starts(text)


class _Pending:
    """A request of the server that the client has yet to answer."""

    __slots__ = ("answered", "failed", "result")

    def __init__(self) -> None:
        self.answered = threading.Event()
        self.failed = False
        self.result: Any = None


@final
class Server:
    """A language server on two binary streams."""

    __slots__ = (
        "_asks_settings",
        "_cancelled",
        "_capabilities",
        "_configs",
        "_documents",
        "_exit_code",
        "_folders",
        "_generation",
        "_inbox",
        "_init_settings",
        "_initialized",
        "_next_id",
        "_pending",
        "_reader",
        "_reported",
        "_rule_modules",
        "_rule_path",
        "_rule_root",
        "_settings",
        "_shutdown_requested",
        "_shutting_down",
        "_stale",
        "_unanswered",
        "_watching",
        "_write_lock",
        "_writer",
    )

    def __init__(self, reader: BinaryIO, writer: BinaryIO) -> None:
        self._reader = reader
        self._writer = writer
        self._write_lock = threading.Lock()
        self._inbox: queue.Queue[Json | None] = queue.Queue()
        self._cancelled: set[int | str | None] = set()
        self._pending: dict[int, _Pending] = {}
        self._next_id = 0
        self._capabilities: Json = {}
        self._asks_settings = False
        self._initialized = False
        self._shutting_down = False
        self._shutdown_requested = False
        self._exit_code: int | None = None
        self._folders: list[Path] = []
        self._documents: dict[str, _Document] = {}
        self._stale: set[str] = set()
        self._init_settings: Json = {}
        self._settings: dict[str, Json] = {}
        self._unanswered: _Pending | None = None
        self._watching: _Pending | None = None
        self._configs: dict[tuple[str, str, str], Config] = {}
        self._reported: set[str] = set()
        self._rule_modules: set[str] = set()
        self._rule_path: str | None = None
        self._rule_root: str | None = None
        # Goes up with every change that can change a finding of an unchanged
        # document, to tell a client that asks if it has the latest.
        self._generation = 0

    def serve(self) -> int:
        """Answer the client until it tells the server to exit."""
        thread = threading.Thread(target=self._read_forever, daemon=True)
        thread.start()
        while self._exit_code is None:
            timeout = _DEBOUNCE_SECONDS if self._stale else None
            try:
                message = self._inbox.get(timeout=timeout)
            except queue.Empty:
                message = _LINT_STALE
            if message is None:
                # The client is gone.
                return 0 if self._shutting_down else 1
            try:
                if message is _LINT_STALE:
                    self._lint_stale()
                elif message is _LATE_ANSWER:
                    self._take_late_settings()
                else:
                    self._handle(message)
            except Exception as error:
                self._log(_LOG_ERROR, f"Dropped a message: {error!r}")
        return self._exit_code

    def _read_message(self) -> bytes | None:
        length: int | None = None
        while True:
            line = self._reader.readline()
            if not line:
                return None
            line = line.strip()
            if not line:
                break
            name, _, value = line.partition(b":")
            if name.strip().lower() == b"content-length":
                with contextlib.suppress(ValueError):
                    length = int(value)
        if length is None or length < 0:
            return b""
        try:
            body = self._reader.read(length)
        except (MemoryError, OverflowError):
            return b""
        return body if len(body) == length else None

    def _read_forever(self) -> None:
        """Take messages in as they come, so one can cancel what's waiting."""
        try:
            self._read_messages()
        finally:
            self._inbox.put(None)
            self._exit_soon()

    def _exit_soon(self) -> None:
        timer = threading.Timer(_EXIT_GRACE_SECONDS, self._exit_now)
        timer.daemon = True
        timer.start()

    def _exit_now(self) -> None:
        os._exit(0 if self._shutdown_requested else 1)

    def _read_messages(self) -> None:
        while (body := self._read_message()) is not None:
            try:
                message = json.loads(body)
            except (RecursionError, ValueError):
                self._log(_LOG_ERROR, "Dropped a message that isn't JSON.")
                self._write({
                    "id": None,
                    "error": {"code": _PARSE_ERROR, "message": "Parse error"},
                })
                continue
            if not isinstance(message, dict):
                self._log(_LOG_ERROR, "Dropped a message that isn't an object.")
            elif message.get("method") == "$/cancelRequest":
                self._take_cancel(message.get("params"))
            elif "method" not in message:
                self._take_answer(message)
            else:
                if message.get("method") == "exit":
                    self._exit_soon()
                elif message.get("method") == "shutdown":
                    self._shutdown_requested = True
                self._inbox.put(message)

    def _take_cancel(self, params: object) -> None:
        if isinstance(params, dict):
            request_id = params.get("id")
            if _is_id(request_id):
                self._cancelled.add(request_id)

    def _take_answer(self, message: Json) -> None:
        request_id = message.get("id")
        if not isinstance(request_id, int):
            return
        pending = self._pending.pop(request_id, None)
        if pending is not None:
            pending.result = message.get("result")
            pending.failed = "error" in message
            pending.answered.set()
            if pending is self._unanswered:
                self._inbox.put(_LATE_ANSWER)

    def _write(self, message: Json) -> None:
        message["jsonrpc"] = "2.0"
        body = json.dumps(message, separators=(",", ":")).encode("utf-8")
        with self._write_lock:
            try:
                self._writer.write(
                    b"Content-Length: %d\r\n\r\n" % len(body) + body
                )
                self._writer.flush()
            except OSError:
                # The client is gone, with nobody left to tell.
                os._exit(1)

    def _notify(self, method: str, params: Json) -> None:
        self._write({"method": method, "params": params})

    def _send_request(self, method: str, params: Json) -> _Pending:
        self._next_id += 1
        pending = _Pending()
        self._pending[self._next_id] = pending
        self._write({"id": self._next_id, "method": method, "params": params})
        return pending

    def _log(self, level: int, message: str) -> None:
        self._notify("window/logMessage", {"type": level, "message": message})

    def _report_once(self, message: str) -> None:
        """Show a problem with a setup, which every run would run into."""
        self._log(_LOG_ERROR, message)
        if message not in self._reported:
            self._reported.add(message)
            self._notify(
                "window/showMessage", {"type": _LOG_ERROR, "message": message}
            )

    def _handle(self, message: Json) -> None:
        method = message.get("method")
        if not isinstance(method, str):
            if "id" in message:
                self._write({
                    "id": message["id"] if _is_id(message["id"]) else None,
                    "error": {
                        "code": _INVALID_REQUEST,
                        "message": "Invalid method",
                    },
                })
            return
        raw_params = message.get("params")
        params: Json = raw_params if isinstance(raw_params, dict) else {}
        if "id" not in message or method == "exit":
            self._handle_notification(method, params)
            return
        request_id = message["id"]
        if len(self._cancelled) > _MAX_CANCELLED:
            self._cancelled.clear()
        if not _is_id(request_id):
            self._write({
                "id": None,
                "error": {"code": _INVALID_REQUEST, "message": "Invalid id"},
            })
            return
        if request_id in self._cancelled:
            self._cancelled.discard(request_id)
            self._respond_error(
                request_id, _REQUEST_CANCELLED, "Request cancelled"
            )
            return
        if method == "initialize" and not self._initialized:
            self._write({"id": request_id, "result": self._initialize(params)})
            return
        if not self._initialized:
            self._respond_error(
                request_id, _SERVER_NOT_INITIALIZED, "Not initialized"
            )
            return
        if self._shutting_down or method == "initialize":
            self._respond_error(
                request_id, _INVALID_REQUEST, "Not at this point"
            )
            return
        handler = self._request_handler(method)
        if handler is None:
            self._respond_error(
                request_id, _METHOD_NOT_FOUND, f"Unknown method {method}"
            )
            return
        try:
            result = handler(params)
        except Exception as error:
            self._respond_error(request_id, _REQUEST_FAILED, str(error))
        except SystemExit:
            self._respond_error(
                request_id, _REQUEST_FAILED, "djLint could not go on."
            )
        else:
            self._write({"id": request_id, "result": result})

    def _request_handler(self, method: str) -> Callable[[Json], Any] | None:
        if method == "shutdown":
            return self._shutdown
        if method == "textDocument/formatting":
            return self._format
        if method == "textDocument/diagnostic":
            return self._pull_diagnostics
        return None

    def _respond_error(
        self, request_id: int | str, code: int, message: str
    ) -> None:
        self._write({
            "id": request_id,
            "error": {"code": code, "message": message},
        })

    def _handle_notification(self, method: str, params: Json) -> None:
        if method == "exit":
            self._exit_code = 0 if self._shutting_down else 1
        elif not self._initialized:
            return
        elif method == "initialized":
            self._watch_configuration()
        elif method == "textDocument/didOpen":
            self._did_open(params["textDocument"])
        elif method == "textDocument/didChange":
            self._did_change(params)
        elif method == "textDocument/didSave":
            self._did_save(params["textDocument"]["uri"])
        elif method == "textDocument/didClose":
            self._did_close(params["textDocument"]["uri"])
        elif method == "workspace/didChangeConfiguration":
            self._take_pushed_settings(params.get("settings"))
            self._settings.clear()
            self._asks_settings = self._workspace_capability("configuration")
            self._configuration_changed()
        elif method == "workspace/didChangeWatchedFiles":
            self._configuration_changed()
        elif method == "workspace/didChangeWorkspaceFolders":
            self._did_change_folders(params["event"])

    def _initialize(self, params: Json) -> Json:
        capabilities = params.get("capabilities")
        self._capabilities = (
            capabilities if isinstance(capabilities, dict) else {}
        )
        options = params.get("initializationOptions")
        self._init_settings = options if isinstance(options, dict) else {}
        self._asks_settings = self._workspace_capability("configuration")
        folders = params.get("workspaceFolders")
        self._folders = [
            path
            for path in (
                _path(folder.get("uri"))
                for folder in (folders if isinstance(folders, list) else ())
                if isinstance(folder, dict)
            )
            if path is not None
        ]
        root = _path(params.get("rootUri"))
        if not self._folders and root is not None:
            self._folders = [root]
        self._initialized = True
        offered: Json = {
            "positionEncoding": "utf-16",
            "textDocumentSync": {
                "openClose": True,
                "change": _SYNC_FULL,
                "save": {"includeText": False},
            },
            "documentFormattingProvider": True,
            "workspace": {
                "workspaceFolders": {
                    "supported": True,
                    "changeNotifications": True,
                }
            },
        }
        if self._pulls_diagnostics:
            offered["diagnosticProvider"] = {
                "identifier": "djlint",
                "interFileDependencies": False,
                "workspaceDiagnostics": False,
            }
        return {
            "capabilities": offered,
            "serverInfo": {"name": "djLint", "version": version("djlint")},
        }

    @property
    def _pulls_diagnostics(self) -> bool:
        text_document = self._capabilities.get("textDocument")
        return isinstance(text_document, dict) and "diagnostic" in text_document

    def _workspace_capability(self, *keys: str) -> bool:
        capability: Any = self._capabilities.get("workspace") or {}
        for key in keys:
            if not isinstance(capability, dict):
                return False
            capability = capability.get(key)
        return bool(capability)

    def _watch_configuration(self) -> None:
        if self._workspace_capability(
            "didChangeConfiguration", "dynamicRegistration"
        ):
            self._send_request(
                "client/registerCapability",
                {
                    "registrations": [
                        {
                            "id": "djlint-settings",
                            "method": "workspace/didChangeConfiguration",
                        }
                    ]
                },
            )
        if not self._workspace_capability(
            "didChangeWatchedFiles", "dynamicRegistration"
        ):
            return
        self._watching = self._send_request(
            "client/registerCapability",
            {
                "registrations": [
                    {
                        "id": "djlint-configuration",
                        "method": "workspace/didChangeWatchedFiles",
                        "registerOptions": {
                            "watchers": [
                                {"globPattern": f"**/{name}"}
                                for name in _CONFIG_FILES
                            ]
                        },
                    }
                ]
            },
        )

    def _shutdown(self, _params: Json) -> None:
        self._shutting_down = True

    def _did_open(self, document: Json) -> None:
        uri = document["uri"]
        if not isinstance(uri, str):
            return
        self._documents[uri] = _Document(
            document["text"],
            document.get("languageId", ""),
            document["version"],
        )
        self._stale.add(uri)
        if self._reads_configuration_again:
            self._forget_configuration()

    def _did_save(self, uri: str) -> None:
        if uri in self._documents:
            self._stale.add(uri)
        if self._reads_configuration_again:
            self._forget_configuration()
            self._refresh_diagnostics()

    def _did_change(self, params: Json) -> None:
        document = self._documents.get(params["textDocument"]["uri"])
        if document is None:
            return
        document.replace(
            params["contentChanges"][-1]["text"],
            params["textDocument"]["version"],
        )
        self._stale.add(params["textDocument"]["uri"])

    def _did_close(self, uri: str) -> None:
        self._documents.pop(uri, None)
        self._stale.discard(uri)
        self._settings.pop(uri, None)
        if not self._pulls_diagnostics:
            self._notify(
                "textDocument/publishDiagnostics",
                {"uri": uri, "diagnostics": []},
            )

    def _did_change_folders(self, event: Json) -> None:
        removed = {_path(folder["uri"]) for folder in event["removed"]}
        self._folders = [
            folder for folder in self._folders if folder not in removed
        ]
        for folder in event["added"]:
            path = _path(folder["uri"])
            if path is not None:
                self._folders.append(path)
        self._settings.clear()
        self._configuration_changed()

    @property
    def _reads_configuration_again(self) -> bool:
        """Tell if nothing would say that the configuration changed."""
        watching = self._watching
        return (
            watching is None
            or not watching.answered.is_set()
            or watching.failed
            or any(
                _setting_name(name) in _PATH_SETTINGS
                for settings in self._settings.values()
                for name in settings
            )
        )

    def _forget_configuration(self) -> None:
        self._generation += 1
        self._configs.clear()

    def _configuration_changed(self) -> None:
        self._generation += 1
        self._configs.clear()
        self._forget_rule_modules()
        self._reported.clear()
        self._refresh_diagnostics()

    def _refresh_diagnostics(self) -> None:
        if self._pulls_diagnostics:
            if self._workspace_capability("diagnostics", "refreshSupport"):
                self._send_request("workspace/diagnostic/refresh", {})
        else:
            self._stale.update(self._documents)

    def _forget_rule_modules(self) -> None:
        """Let the next lint import the modules of custom rules anew."""
        for name in self._rule_modules:
            sys.modules.pop(name, None)
        self._rule_modules.clear()
        if self._rule_path is not None:
            with contextlib.suppress(ValueError):
                sys.path.remove(self._rule_path)
            self._rule_path = None
        self._rule_root = None

    def _use_rule_modules_of(self, config: Config) -> None:
        """Keep the same-named rule modules of two projects apart."""
        root = str(config.project_root)
        if root != self._rule_root:
            self._forget_rule_modules()
            self._rule_root = root

    def _note_rule_modules(
        self, config: Config, modules: set[str], path: set[str]
    ) -> None:
        """Remember what a lint added, of all it imported from the project."""
        root = str(config.project_root)
        if root not in path and root in sys.path:
            self._rule_path = root
        for name in sys.modules.keys() - modules:
            # From the module's own dict: an attribute can run code.
            filename = getattr(sys.modules[name], "__dict__", {}).get(
                "__file__"
            )
            if isinstance(filename, str):
                path = Path(filename)
                if path.is_relative_to(root) and (
                    "site-packages" not in path.parts
                ):
                    self._rule_modules.add(name)

    def _take_late_settings(self) -> None:
        """Ask again, if an editor that took too long has answered."""
        if self._unanswered is not None and self._unanswered.answered.is_set():
            self._unanswered = None
            self._asks_settings = True
            self._settings.clear()
            self._configuration_changed()

    def _take_pushed_settings(self, pushed: object) -> None:
        """Keep the settings of a push, which may be for other servers."""
        if not isinstance(pushed, dict):
            return
        section = pushed.get("djlint")
        if isinstance(section, dict):
            self._init_settings = section
        elif "djlint" in pushed:
            self._init_settings = {}
        elif any(_setting_name(name) in _known_settings() for name in pushed):
            self._init_settings = pushed

    def _settings_for(self, uri: str) -> Json:
        """Ask the client for the settings of a document, once."""
        self._take_late_settings()
        settings = self._settings.get(uri)
        if settings is not None:
            return settings
        settings = dict(self._init_settings)
        if self._asks_settings:
            pending = self._send_request(
                "workspace/configuration",
                {"items": [{"scopeUri": uri, "section": "djlint"}]},
            )
            if pending.answered.wait(_CLIENT_TIMEOUT_SECONDS):
                answer = pending.result
                if (
                    isinstance(answer, list)
                    and answer
                    and isinstance(answer[0], dict)
                ):
                    settings.update(answer[0])
            else:
                self._asks_settings = False
                self._unanswered = pending
                if pending.answered.is_set():
                    self._inbox.put(_LATE_ANSWER)
                self._log(
                    _LOG_WARNING,
                    "The editor didn't answer workspace/configuration.",
                )
                return settings
        self._settings[uri] = settings
        return settings

    def _options(self, settings: Json, path: Path | None) -> Json:
        known = _known_settings()
        options: Json = {}
        for name, value in settings.items():
            option = _setting_name(name)
            if option == "use_editor_indentation":
                continue
            if option not in known:
                self._log(_LOG_WARNING, f"Ignoring the setting {name}.")
            elif option in _PATH_SETTINGS:
                if value:
                    options[option] = self._resolve(str(value), path)
            elif option == "python_rules":
                options[option] = value is not False
            elif value is not None and value not in ("", []):
                options[option] = _option_value(value)
        return options

    def _resolve(self, value: str, document: Path | None) -> Path:
        path = Path(value).expanduser()
        return path if path.is_absolute() else self._folder_of(document) / path

    def _folder_of(self, document: Path | None) -> Path:
        """Return the workspace folder of a document, the nearest if nested."""
        if document is not None:
            parents = [
                folder
                for folder in self._folders
                if document.is_relative_to(folder)
            ]
            if parents:
                return max(parents, key=lambda folder: len(folder.parts))
        return self._folders[0] if self._folders else Path.cwd()

    def _is_excluded(self, config: Config, path: Path) -> bool:
        """Check from the workspace folder too, as a run on it would."""
        return is_excluded(config, path, self._folder_of(path))

    def _config(
        self, uri: str, document: _Document, indent: int | None = None
    ) -> Config:
        path = _path(uri)
        options = self._options(self._settings_for(uri), path)
        if indent is not None:
            options["indent"] = indent
        folder = str(self._folder_of(None) if path is None else path.parent)
        key = (
            folder,
            json.dumps(options, sort_keys=True, default=str),
            document.language,
        )
        config = self._configs.get(key)
        if config is None:
            config = load_config(folder, **options)
            profile = _PROFILES.get(document.language)
            if (
                profile is not None
                and "profile" not in options
                and not config.has_profile
            ):
                config = load_config(folder, **options, profile=profile)
            self._configs[key] = config
        return config

    def _lint(self, uri: str, document: _Document) -> list[Json]:
        config = self._config(uri, document)
        path = _path(uri)
        if path is not None and self._is_excluded(config, path):
            return []
        self._use_rule_modules_of(config)
        modules = set(sys.modules)
        search_path = set(sys.path)
        try:
            findings = lint_text(
                config, document.text, "-" if path is None else path.as_posix()
            )
        finally:
            self._note_rule_modules(config, modules, search_path)
        return [_diagnostic(document, finding) for finding in findings]

    def _safe_lint(self, uri: str, document: _Document) -> list[Json]:
        """Lint, reporting what stops djLint instead of ending the server."""
        try:
            return self._lint(uri, document)
        except Exception as error:
            self._report_once(f"djLint failed: {error}")
        except SystemExit:
            self._report_once(
                "djLint could not go on, usually because of its configuration."
            )
        return []

    def _lint_stale(self) -> None:
        stale, self._stale = self._stale, set()
        if self._pulls_diagnostics:
            return
        for uri in stale:
            document = self._documents.get(uri)
            if document is not None:
                self._notify(
                    "textDocument/publishDiagnostics",
                    {
                        "uri": uri,
                        "version": document.version,
                        "diagnostics": self._safe_lint(uri, document),
                    },
                )

    def _pull_diagnostics(self, params: Json) -> Json:
        uri = params["textDocument"]["uri"]
        document = self._documents.get(uri)
        if document is None:
            return {"kind": "full", "items": []}
        self._take_late_settings()
        digest = hashlib.sha256(document.text.encode("utf-8", "replace"))
        result_id = f"{self._generation}-{digest.hexdigest()}"
        if params.get("previousResultId") == result_id:
            return {"kind": "unchanged", "resultId": result_id}
        return {
            "kind": "full",
            "resultId": result_id,
            "items": self._safe_lint(uri, document),
        }

    def _format(self, params: Json) -> list[Json] | None:
        uri = params["textDocument"]["uri"]
        document = self._documents.get(uri)
        if document is None:
            return None
        settings = self._settings_for(uri)
        uses_editor_indent = any(
            value and _setting_name(name) == "use_editor_indentation"
            for name, value in settings.items()
        )
        config = self._config(
            uri,
            document,
            params["options"]["tabSize"] if uses_editor_indent else None,
        )
        path = _path(uri)
        if path is not None and self._is_excluded(config, path):
            return None
        return _edits(document.text, format_text(config, document.text))


def _known_settings() -> set[str]:
    from djlint import main  # noqa: PLC0415

    known = {parameter.name for parameter in main.params} - _NOT_SETTINGS
    known.update(("python_rules", "use_editor_indentation"))
    return known


def _path(uri: object) -> Path | None:
    """Return the path of a file: URI, and None for anything else."""
    if not isinstance(uri, str):
        return None
    try:
        parsed = urlparse(uri)
    except ValueError:
        return None
    if parsed.scheme != "file":
        return None
    path = unquote(parsed.path)
    if parsed.netloc not in {"", "localhost"}:
        return Path(f"//{unquote(parsed.netloc)}{path}")
    if sys.platform == "win32" and _WINDOWS_DRIVE.match(path):
        path = path[1:]
    return Path(path)


def serve() -> NoReturn:
    """Run the server on stdio, until the client ends it."""
    sys.stdout.flush()
    # `python -m` puts the folder it starts in on the path, where a rule module
    # of that project would stand in for another project's.
    sys.path[:] = [
        path for path in sys.path if path not in {"", str(Path.cwd())}
    ]
    reader = os.fdopen(os.dup(sys.stdin.fileno()), "rb")
    writer = os.fdopen(os.dup(sys.stdout.fileno()), "wb")
    # Whatever prints or starts a process on the way, such as a custom rule,
    # gets stderr and no input instead of the protocol's streams.
    os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
    with Path(os.devnull).open("rb") as null:
        os.dup2(null.fileno(), sys.stdin.fileno())
    code = Server(reader, writer).serve()
    writer.flush()
    sys.stderr.flush()
    # Python can crash at exit on a thread blocked in a read of stdin.
    os._exit(code)
