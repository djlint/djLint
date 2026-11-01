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
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse
from urllib.request import url2pathname

from djlint.api import format_text, is_excluded, lint_text, load_config

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

_SYNC_INCREMENTAL: Final = 2
_SEVERITY_WARNING: Final = 2

# Above this, a character takes two UTF-16 units.
_LAST_BMP: Final = 0xFFFF

# How long typing has to pause before an open document is linted.
_DEBOUNCE_SECONDS: Final = 0.2
_CLIENT_TIMEOUT_SECONDS: Final = 5

_CONFIG_FILES: Final = (
    "pyproject.toml",
    "djlint.toml",
    ".djlint.toml",
    ".djlintrc",
    ".gitignore",
)

# Options of the command line that aren't about a template.
_NOT_SETTINGS: Final = frozenset({
    "allow_empty_input",
    "check",
    "github_output",
    "lint",
    "lsp",
    "quiet",
    "reformat",
    "sarif",
    "src",
    "statistics",
    "stdin_filename",
    "warn",
})

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
    "jinja2": "jinja",
    "liquid": "liquid",
    "mustache": "handlebars",
    "njk": "nunjucks",
    "nunjucks": "nunjucks",
    "tera": "tera",
    "tera-html": "tera",
}

_LINE_END: Final = re.compile(r"\r\n|\r|\n")
_RULE_CODE: Final = re.compile(r"[A-Z]\d{3}")
_CAMEL_HUMP: Final = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def _setting_name(name: str) -> str:
    return _CAMEL_HUMP.sub("_", name).replace("-", "_").lower()


def _option_value(value: Any) -> Any:
    """Put a value of a setting in the form of the command line."""
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    if isinstance(value, dict):
        return tuple(value.items())
    return value


def _line_starts(text: str) -> list[int]:
    return [0, *(match.end() for match in _LINE_END.finditer(text))]


def _line_text(text: str, starts: list[int], line: int) -> str:
    """Return a line without its line ending."""
    end = starts[line + 1] if line + 1 < len(starts) else len(text)
    return text[starts[line] : end].rstrip("\r\n")


def _utf16_length(text: str) -> int:
    if text.isascii():
        return len(text)
    return len(text) + sum(ord(char) > _LAST_BMP for char in text)


def _offset(text: str, starts: list[int], position: Json) -> int:
    """Turn a position of the protocol, in UTF-16 units, into an index."""
    line: int = position["line"]
    if line >= len(starts):
        return len(text)
    content = _line_text(text, starts, line)
    units: int = position["character"]
    if content.isascii():
        return starts[line] + min(units, len(content))
    seen = 0
    for index, char in enumerate(content):
        if seen >= units:
            return starts[line] + index
        seen += 2 if ord(char) > _LAST_BMP else 1
    return starts[line] + len(content)


def _position(text: str, starts: list[int], line: int, column: int) -> Json:
    """Turn a line from 1 and a column in characters into a position."""
    index = min(line, len(starts)) - 1
    index = max(index, 0)
    content = _line_text(text, starts, index)
    return {
        "line": index,
        "character": _utf16_length(content[: max(column, 0)]),
    }


def _diagnostic(text: str, starts: list[int], finding: Finding) -> Json:
    diagnostic: Json = {
        "range": {
            "start": _position(text, starts, finding.line, finding.column),
            "end": _position(
                text, starts, finding.end_line, finding.end_column
            ),
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


class _Document:
    __slots__ = ("language", "starts", "text", "version")

    def __init__(self, text: str, language: str, doc_version: int) -> None:
        self.text = text
        self.language = language
        self.version = doc_version
        self.starts = _line_starts(text)

    def apply(self, change: Json) -> None:
        change_range = change.get("range")
        if change_range is None:
            self.text = change["text"]
        else:
            start = _offset(self.text, self.starts, change_range["start"])
            end = _offset(self.text, self.starts, change_range["end"])
            self.text = self.text[:start] + change["text"] + self.text[end:]
        self.starts = _line_starts(self.text)


class _Pending:
    """A request of the server that the client has yet to answer."""

    __slots__ = ("answered", "result")

    def __init__(self) -> None:
        self.answered = threading.Event()
        self.result: Any = None


class Server:
    """A language server on two binary streams."""

    def __init__(self, reader: BinaryIO, writer: BinaryIO) -> None:
        self._reader = reader
        self._writer = writer
        self._write_lock = threading.Lock()
        self._inbox: queue.Queue[Json | None] = queue.Queue()
        self._cancelled: set[int | str | None] = set()
        self._pending: dict[int, _Pending] = {}
        self._next_id = 0
        self._capabilities: Json = {}
        self._initialized = False
        self._shutting_down = False
        self._exit_code: int | None = None
        self._folders: list[Path] = []
        self._documents: dict[str, _Document] = {}
        self._stale: set[str] = set()
        self._init_settings: Json = {}
        self._settings: dict[str, Json] = {}
        self._configs: dict[tuple[str, str, str], Config] = {}
        self._reported: set[str] = set()
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
                self._lint_stale()
                continue
            if message is None:
                # The client is gone.
                return 0 if self._shutting_down else 1
            self._handle(message)
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
        if length is None:
            return b""
        body = self._reader.read(length)
        return body if len(body) == length else None

    def _read_forever(self) -> None:
        """Take messages in as they come, so one can cancel what's waiting."""
        while (body := self._read_message()) is not None:
            try:
                message = json.loads(body)
            except ValueError:
                self._log(_LOG_ERROR, "Dropped a message that isn't JSON.")
                self._write({
                    "id": None,
                    "error": {"code": _PARSE_ERROR, "message": "Parse error"},
                })
                continue
            if not isinstance(message, dict):
                continue
            if message.get("method") == "$/cancelRequest":
                self._cancelled.add((message.get("params") or {}).get("id"))
            elif "method" not in message and "id" in message:
                self._take_answer(message)
            else:
                self._inbox.put(message)
        self._inbox.put(None)

    def _take_answer(self, message: Json) -> None:
        pending = self._pending.pop(message["id"], None)
        if pending is not None:
            pending.result = message.get("result")
            pending.answered.set()

    def _write(self, message: Json) -> None:
        message["jsonrpc"] = "2.0"
        body = json.dumps(message, separators=(",", ":")).encode("utf-8")
        with self._write_lock:
            self._writer.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
            self._writer.flush()

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
            return
        if "id" not in message:
            try:
                self._handle_notification(method, message.get("params") or {})
            except (KeyError, TypeError) as error:
                self._log(_LOG_ERROR, f"Malformed {method}: {error!r}")
            return
        request_id = message["id"]
        if request_id in self._cancelled:
            self._cancelled.discard(request_id)
            self._respond_error(
                request_id, _REQUEST_CANCELLED, "Request cancelled"
            )
            return
        if method == "initialize":
            self._write({
                "id": request_id,
                "result": self._initialize(message.get("params") or {}),
            })
            return
        if not self._initialized:
            self._respond_error(
                request_id, _SERVER_NOT_INITIALIZED, "Not initialized"
            )
            return
        if self._shutting_down:
            self._respond_error(request_id, _INVALID_REQUEST, "Shutting down")
            return
        handler = self._request_handler(method)
        if handler is None:
            self._respond_error(
                request_id, _METHOD_NOT_FOUND, f"Unknown method {method}"
            )
            return
        try:
            result = handler(message.get("params") or {})
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
            document = params["textDocument"]
            self._documents[document["uri"]] = _Document(
                document["text"], document["languageId"], document["version"]
            )
            self._stale.add(document["uri"])
        elif method == "textDocument/didChange":
            self._did_change(params)
        elif method == "textDocument/didSave":
            self._stale.add(params["textDocument"]["uri"])
        elif method == "textDocument/didClose":
            self._did_close(params["textDocument"]["uri"])
        elif method == "workspace/didChangeConfiguration":
            self._settings.clear()
            self._configuration_changed()
        elif method == "workspace/didChangeWatchedFiles":
            self._configuration_changed()
        elif method == "workspace/didChangeWorkspaceFolders":
            self._did_change_folders(params["event"])

    def _initialize(self, params: Json) -> Json:
        self._capabilities = params.get("capabilities") or {}
        self._init_settings = params.get("initializationOptions") or {}
        folders = params.get("workspaceFolders") or []
        self._folders = [
            path
            for path in (_path(folder["uri"]) for folder in folders)
            if path is not None
        ]
        if not self._folders and (root := params.get("rootUri")):
            path = _path(root)
            self._folders = [] if path is None else [path]
        self._initialized = True
        capabilities: Json = {
            "positionEncoding": "utf-16",
            "textDocumentSync": {
                "openClose": True,
                "change": _SYNC_INCREMENTAL,
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
            capabilities["diagnosticProvider"] = {
                "identifier": "djlint",
                "interFileDependencies": False,
                "workspaceDiagnostics": False,
            }
        return {
            "capabilities": capabilities,
            "serverInfo": {"name": "djLint", "version": version("djlint")},
        }

    @property
    def _pulls_diagnostics(self) -> bool:
        return "diagnostic" in (self._capabilities.get("textDocument") or {})

    def _workspace_capability(self, *keys: str) -> bool:
        capability: Any = self._capabilities.get("workspace") or {}
        for key in keys:
            if not isinstance(capability, dict):
                return False
            capability = capability.get(key)
        return bool(capability)

    def _watch_configuration(self) -> None:
        if not self._workspace_capability(
            "didChangeWatchedFiles", "dynamicRegistration"
        ):
            return
        self._send_request(
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

    def _did_change(self, params: Json) -> None:
        document = self._documents.get(params["textDocument"]["uri"])
        if document is None:
            return
        for change in params["contentChanges"]:
            document.apply(change)
        document.version = params["textDocument"]["version"]
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
        self._configuration_changed()

    def _configuration_changed(self) -> None:
        self._generation += 1
        self._configs.clear()
        self._reported.clear()
        if self._pulls_diagnostics:
            if self._workspace_capability("diagnostics", "refreshSupport"):
                self._send_request("workspace/diagnostic/refresh", {})
        else:
            self._stale.update(self._documents)

    def _settings_for(self, uri: str) -> Json:
        """Ask the client for the settings of a document, once."""
        settings = self._settings.get(uri)
        if settings is not None:
            return settings
        settings = dict(self._init_settings)
        if self._workspace_capability("configuration"):
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
        self._settings[uri] = settings
        return settings

    def _options(self, settings: Json) -> Json:
        from djlint import main  # noqa: PLC0415

        known = {parameter.name for parameter in main.params} - _NOT_SETTINGS
        known.add("python_rules")
        options: Json = {}
        for name, value in settings.items():
            option = _setting_name(name)
            if option == "use_editor_indentation":
                continue
            if option not in known:
                self._log(_LOG_WARNING, f"Ignoring the setting {name}.")
            elif value is not None and value not in ("", []):
                options[option] = _option_value(value)
        return options

    def _config(
        self, uri: str, document: _Document, indent: int | None = None
    ) -> Config:
        options = self._options(self._settings_for(uri))
        if indent is not None:
            options["indent"] = indent
        path = _path(uri)
        folder = str(
            path.parent if path is not None else self._default_folder()
        )
        key = (folder, json.dumps(options, sort_keys=True), document.language)
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

    def _default_folder(self) -> Path:
        return self._folders[0] if self._folders else Path.cwd()

    def _lint(self, uri: str, document: _Document) -> list[Json]:
        config = self._config(uri, document)
        path = _path(uri)
        if path is not None and is_excluded(config, path):
            return []
        findings = lint_text(
            config, document.text, "-" if path is None else path.as_posix()
        )
        return [
            _diagnostic(document.text, document.starts, finding)
            for finding in findings
        ]

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
        if path is not None and is_excluded(config, path):
            return None
        return _edits(document.text, format_text(config, document.text))


def _path(uri: str) -> Path | None:
    """Return the path of a file: URI, and None for any other scheme."""
    parsed = urlparse(uri)
    if parsed.scheme != "file":
        return None
    if parsed.netloc not in {"", "localhost"}:
        return Path(url2pathname(f"//{parsed.netloc}{parsed.path}"))
    return Path(url2pathname(parsed.path))


def serve() -> NoReturn:
    """Run the server on stdio, until the client ends it."""
    reader = sys.stdin.buffer
    writer = sys.stdout.buffer
    # Anything printed on the way must not end up in the protocol's stream.
    sys.stdout = sys.stderr
    code = Server(reader, writer).serve()
    writer.flush()
    sys.stderr.flush()
    # Python can crash at exit on a thread blocked in a read of stdin.
    os._exit(code)
