"""The language server, driven as an editor does: over stdio, in a process.

uv run pytest tests/test_server.py
"""

from __future__ import annotations

import json
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from djlint.api import format_text, load_config
from djlint.server import _path  # noqa: PLC2701

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any

TIMEOUT_SECONDS = 30
DEBOUNCE_SECONDS = 0.5

UNFORMATTED = "<div><p>hi</p>\n</div>\n"
FORMATTED = "<div>\n    <p>hi</p>\n</div>\n"
FINDING = '<img src="x">\n'
ONE_FINDING_RANGE = {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 13}}
PUSH_CAPABILITIES: dict[str, Any] = {}
PULL_CAPABILITIES: dict[str, Any] = {"textDocument": {"diagnostic": {}}}


class Client:
    """What an editor does, and nothing of the server's code."""

    __slots__ = ("ignored", "messages", "next_id", "process", "settings")

    def __init__(self) -> None:
        self.process = subprocess.Popen(
            [sys.executable, "-m", "djlint", "--lsp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        self.next_id = 0
        self.messages: queue.Queue[dict[str, Any] | None] = queue.Queue()
        self.settings: Any = None
        self.ignored: list[dict[str, Any]] = []
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self) -> None:
        stream = self.process.stdout
        assert stream is not None
        while True:
            line = stream.readline()
            if not line:
                self.messages.put(None)
                return
            length = int(line.split(b":")[1])
            stream.readline()
            self.messages.put(json.loads(stream.read(length)))

    def write(self, message: dict[str, Any]) -> None:
        message["jsonrpc"] = "2.0"
        body = json.dumps(message).encode()
        stdin = self.process.stdin
        assert stdin is not None
        stdin.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
        stdin.flush()

    def notify(self, method: str, params: dict[str, Any]) -> None:
        self.write({"method": method, "params": params})

    def send(self, method: str, params: dict[str, Any]) -> int:
        self.next_id += 1
        self.write({"id": self.next_id, "method": method, "params": params})
        return self.next_id

    def next_message(self) -> dict[str, Any]:
        message = self.messages.get(timeout=TIMEOUT_SECONDS)
        assert message is not None, "the server is gone"
        if "method" in message and "id" in message:
            result = [self.settings] if message["method"] == "workspace/configuration" else None
            self.write({"id": message["id"], "result": result})
        return message

    def response(self, request_id: int) -> dict[str, Any]:
        while True:
            message = self.next_message()
            if message.get("id") == request_id and "method" not in message:
                return message
            self.ignored.append(message)

    def request(self, method: str, params: dict[str, Any]) -> Any:
        response = self.response(self.send(method, params))
        assert "error" not in response, response
        return response["result"]

    def notification(self, method: str) -> dict[str, Any]:
        for index, message in enumerate(self.ignored):
            if message.get("method") == method:
                del self.ignored[index]
                params: dict[str, Any] = message["params"]
                return params
        while True:
            message = self.next_message()
            if message.get("method") == method:
                found: dict[str, Any] = message["params"]
                return found
            self.ignored.append(message)

    def notification_or_request(self, method: str) -> dict[str, Any]:
        """Wait for a message of the server, answered if it needs it."""
        return self.notification(method)

    def start(
        self,
        root: Path | None = None,
        capabilities: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result: dict[str, Any] = self.request(
            "initialize",
            {
                "capabilities": capabilities or {},
                "initializationOptions": options,
                "workspaceFolders": None
                if root is None
                else [{"uri": root.as_uri(), "name": "root"}],
            },
        )
        self.notify("initialized", {})
        return result

    def open(self, uri: str, text: str, language: str = "html", version: int = 1) -> None:
        self.notify(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": uri,
                    "languageId": language,
                    "version": version,
                    "text": text,
                }
            },
        )

    def diagnostics(self, uri: str) -> list[dict[str, Any]]:
        while True:
            params = self.notification("textDocument/publishDiagnostics")
            if params["uri"] == uri:
                found: list[dict[str, Any]] = params["diagnostics"]
                return found

    def format(self, uri: str, tab_size: int = 2) -> Any:
        return self.request(
            "textDocument/formatting",
            {"textDocument": {"uri": uri}, "options": {"tabSize": tab_size, "insertSpaces": True}},
        )

    def stop(self) -> int:
        self.request("shutdown", {})
        self.notify("exit", {})
        return self.process.wait(TIMEOUT_SECONDS)


@pytest.fixture
def client() -> Iterator[Client]:
    started = Client()
    yield started
    started.process.kill()
    started.process.wait(TIMEOUT_SECONDS)
    for stream in (started.process.stdin, started.process.stdout):
        assert stream is not None
        stream.close()


def apply(text: str, edits: list[dict[str, Any]]) -> str:
    """Apply edits on whole lines, which is what the server sends."""
    lines = text.splitlines(keepends=True)
    if text.endswith(("\n", "\r")):
        lines.append("")
    for edit in reversed(edits):
        start = edit["range"]["start"]
        end = edit["range"]["end"]
        assert start["character"] == 0
        before = "".join(lines[: start["line"]])
        tail = lines[end["line"] :]
        rest = "".join(tail)[end["character"] :]
        text = before + edit["newText"] + rest
        lines = text.splitlines(keepends=True)
    return text


def test_says_what_it_can_do(client: Client, tmp_path: Path) -> None:
    result = client.start(tmp_path)
    assert result["serverInfo"]["name"] == "djLint"
    assert result["capabilities"]["positionEncoding"] == "utf-16"
    assert result["capabilities"]["documentFormattingProvider"] is True
    assert "diagnosticProvider" not in result["capabilities"]


def test_offers_pull_to_a_client_that_has_it(client: Client, tmp_path: Path) -> None:
    result = client.start(tmp_path, PULL_CAPABILITIES)
    assert result["capabilities"]["diagnosticProvider"] == {
        "identifier": "djlint",
        "interFileDependencies": False,
        "workspaceDiagnostics": False,
    }


def test_publishes_findings(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri) == [
        {
            "range": ONE_FINDING_RANGE,
            "severity": 2,
            "code": "H013",
            "source": "djLint",
            "message": "Img tag should have an alt attribute.",
            "codeDescription": {"href": "https://djlint.com/docs/linter/#h013"},
        }
    ]


def test_counts_columns_in_utf16(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, '<p>😀é</p><img src="x">\n')
    [finding] = client.diagnostics(uri)
    assert finding["range"]["start"] == {"line": 0, "character": 10}
    assert finding["range"]["end"] == {"line": 0, "character": 23}


def test_takes_a_whole_document_as_a_change(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    client.diagnostics(uri)
    client.notify(
        "textDocument/didChange",
        {"textDocument": {"uri": uri, "version": 2}, "contentChanges": [{"text": "<p>fine</p>\n"}]},
    )
    assert client.diagnostics(uri) == []


def test_clears_findings_on_close(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri)
    client.notify("textDocument/didClose", {"textDocument": {"uri": uri}})
    assert client.diagnostics(uri) == []


def test_answers_a_pull(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, PULL_CAPABILITIES)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    params = {"textDocument": {"uri": uri}}
    report = client.request("textDocument/diagnostic", params)
    assert report["kind"] == "full"
    assert [item["code"] for item in report["items"]] == ["H013"]
    assert client.request(
        "textDocument/diagnostic", {**params, "previousResultId": report["resultId"]}
    ) == {"kind": "unchanged", "resultId": report["resultId"]}


def test_does_not_push_to_a_client_that_pulls(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, PULL_CAPABILITIES)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    time.sleep(DEBOUNCE_SECONDS)
    client.format(uri)
    assert not any(
        message.get("method") == "textDocument/publishDiagnostics" for message in client.ignored
    )


@pytest.mark.parametrize(
    "text",
    [
        UNFORMATTED,
        UNFORMATTED.replace("\n", "\r\n"),
        f"<p>same</p>\n{UNFORMATTED}<p>same</p>\n",
        "😀<div><p>hi</p></div>",
    ],
)
def test_formats_as_the_api_does(client: Client, tmp_path: Path, text: str) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, text)
    assert apply(text, client.format(uri)) == format_text(load_config(tmp_path), text)


def test_replaces_only_the_lines_that_differ(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, f"<p>same</p>\n{UNFORMATTED}<p>same</p>\n")
    [edit] = client.format(uri)
    assert edit["range"] == {
        "start": {"line": 1, "character": 0},
        "end": {"line": 2, "character": 0},
    }
    assert edit["newText"] == "<div>\n    <p>hi</p>\n"


def test_has_nothing_to_change_on_formatted_text(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FORMATTED)
    assert client.format(uri) == []


def test_reads_the_project_of_each_file(client: Client, tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    (project / ".djlintrc").write_text('{"indent": 2}', encoding="utf-8")
    client.start(tmp_path)
    uri = (project / "a.html").as_uri()
    client.open(uri, UNFORMATTED)
    [edit] = client.format(uri)
    assert "\n  <p>hi</p>\n" in edit["newText"]


def test_ignores_the_tab_size_of_the_editor(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, UNFORMATTED)
    [edit] = client.format(uri, tab_size=8)
    assert "\n    <p>hi</p>\n" in edit["newText"]


def test_can_follow_the_tab_size_of_the_editor(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, options={"useEditorIndentation": True})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, UNFORMATTED)
    [edit] = client.format(uri, tab_size=2)
    assert "\n  <p>hi</p>\n" in edit["newText"]


def test_takes_settings_from_the_start(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, options={"ignore": ["H013"]})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri) == []


def test_asks_the_client_for_settings(client: Client, tmp_path: Path) -> None:
    client.settings = {"ignore": "H013"}
    client.start(tmp_path, {"workspace": {"configuration": True}})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri) == []


def test_asks_again_after_a_change_of_settings(client: Client, tmp_path: Path) -> None:
    client.settings = {"ignore": "H013"}
    client.start(tmp_path, {"workspace": {"configuration": True}})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri) == []
    client.settings = {}
    client.notify("workspace/didChangeConfiguration", {"settings": None})
    assert [item["code"] for item in client.diagnostics(uri)] == ["H013"]


@pytest.mark.parametrize("text", ['a\r<img src="x">\rb\r', 'a\n\r\n<img src="x">\n'])
def test_counts_lines_as_the_protocol_does(client: Client, tmp_path: Path, text: str) -> None:
    client.start(tmp_path, options={"ignore": "H014,H025"})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, text)
    [finding] = [item for item in client.diagnostics(uri) if item["code"] == "H013"]
    line = 1 if "\r<" in text else 2
    assert finding["range"] == {
        "start": {"line": line, "character": 0},
        "end": {"line": line, "character": 13},
    }


def test_replaces_a_text_with_lone_cr_whole(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, "<div>\r<p>x</p></div>\r<p>y</p>\n")
    [edit] = client.format(uri)
    assert edit["range"]["start"] == {"line": 0, "character": 0}
    assert edit["range"]["end"]["line"] >= 3


def test_finds_blank_lines_with_crlf(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, "<p>a</p>\r\n\r\n\r\n\r\n<p>b</p>\r\n")
    assert "H014" in [item["code"] for item in client.diagnostics(uri)]


@pytest.mark.skipif(sys.platform != "win32", reason="a Windows path")
def test_reads_an_encoded_drive_letter() -> None:
    assert _path("file:///c%3A/x/a.html") == Path("c:/x/a.html")


@pytest.mark.parametrize(
    ("uri", "expected"),
    [
        ("file:///x/a%20b.html", "/x/a b.html"),
        ("file://localhost/x/a.html", "/x/a.html"),
        ("file://wsl%24/x/a.html", "//wsl$/x/a.html"),
    ],
)
def test_reads_a_uri(uri: str, expected: str) -> None:
    assert _path(uri) == Path(expected)


@pytest.mark.parametrize("uri", ["untitled:a", "file://[bad", None, 1])
def test_has_no_path_for_what_is_no_file(uri: object) -> None:
    assert _path(uri) is None


def test_takes_a_relative_rules_file(client: Client, tmp_path: Path) -> None:
    (tmp_path / "rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: found\n    patterns:\n      - needle\n",
        encoding="utf-8",
    )
    client.start(tmp_path, options={"rules": "rules.yaml"})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, "<p>needle</p>\n")
    assert "X001" in [item["code"] for item in client.diagnostics(uri)]


def test_keeps_rule_modules_of_two_projects_apart(client: Client, tmp_path: Path) -> None:
    uris = []
    for name in ("one", "two"):
        project = tmp_path / name
        project.mkdir()
        (project / "pyproject.toml").write_text("", encoding="utf-8")
        (project / "same_name.py").write_text(
            "def run(rule, **_):\n"
            f"    return [{{'code': '{name}', 'line': '1:0',"
            " 'match': 'x', 'message': 'm'}]\n",
            encoding="utf-8",
        )
        (project / ".djlint_rules.yaml").write_text(
            "- rule:\n    name: X001\n    message: x\n    python_module: same_name\n",
            encoding="utf-8",
        )
        uris.append((project / "a.html").as_uri())
    client.start(tmp_path)
    for uri, name in zip(uris, ("one", "two"), strict=True):
        client.open(uri, "<p>x</p>\n")
        assert name in [item["code"] for item in client.diagnostics(uri)]


def test_reads_an_edited_configuration_without_a_watcher(client: Client, tmp_path: Path) -> None:
    config = tmp_path / ".djlintrc"
    config.write_text("{}", encoding="utf-8")
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri)
    config.write_text('{"ignore": "H013"}', encoding="utf-8")
    client.notify("textDocument/didSave", {"textDocument": {"uri": uri}})
    assert client.diagnostics(uri) == []


def test_takes_settings_pushed_by_the_client(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri)
    client.notify("workspace/didChangeConfiguration", {"settings": {"djlint": {"ignore": "H013"}}})
    assert client.diagnostics(uri) == []


def test_exits_during_a_rule_that_never_ends(client: Client, tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    marker = tmp_path / "started"
    (tmp_path / "endless.py").write_text(
        "from pathlib import Path\n"
        "def run(**_):\n"
        f"    Path({str(marker)!r}).touch()\n"
        "    while True:\n"
        "        pass\n",
        encoding="utf-8",
    )
    (tmp_path / ".djlint_rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: x\n    python_module: endless\n", encoding="utf-8"
    )
    client.start(tmp_path)
    client.open((tmp_path / "a.html").as_uri(), "<p>x</p>\n")
    deadline = time.monotonic() + TIMEOUT_SECONDS
    while not marker.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert marker.exists()
    client.notify("exit", {})
    assert client.process.wait(TIMEOUT_SECONDS) == 1


def test_keeps_the_protocol_from_a_rule_that_prints(client: Client, tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    (tmp_path / "noisy.py").write_text(
        "import os, subprocess, sys\n"
        "def run(**_):\n"
        "    print('noise')\n"
        "    os.write(1, b'noise')\n"
        "    subprocess.run([sys.executable, '-c', 'print(1)'], check=True)\n"
        "    return []\n",
        encoding="utf-8",
    )
    (tmp_path / ".djlint_rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: x\n    python_module: noisy\n", encoding="utf-8"
    )
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, "<p>x</p>\n")
    assert client.diagnostics(uri) == []
    assert client.stop() == 0


def test_answers_what_was_sent_before_exit(tmp_path: Path) -> None:
    uri = (tmp_path / "a.html").as_uri()
    messages: list[dict[str, Any]] = [
        {"id": 1, "method": "initialize", "params": {"capabilities": {}}},
        {"method": "initialized", "params": {}},
        {
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": uri,
                    "languageId": "html",
                    "version": 1,
                    "text": UNFORMATTED,
                }
            },
        },
        {
            "id": 2,
            "method": "textDocument/formatting",
            "params": {
                "textDocument": {"uri": uri},
                "options": {"tabSize": 4, "insertSpaces": True},
            },
        },
        {"id": 3, "method": "shutdown"},
        {"method": "exit"},
    ]
    bodies = [json.dumps({"jsonrpc": "2.0", **m}).encode() for m in messages]
    done = subprocess.run(
        [sys.executable, "-m", "djlint", "--lsp"],
        input=b"".join(b"Content-Length: %d\r\n\r\n%s" % (len(body), body) for body in bodies),
        capture_output=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    assert done.returncode == 0
    assert b'"id":2,"result":[' in done.stdout
    assert b'"id":3,"result":null' in done.stdout


def test_leaves_installed_packages_imported(client: Client, tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    other = tmp_path / "other"
    other.mkdir()
    (other / "pyproject.toml").write_text("", encoding="utf-8")
    client.start(tmp_path)
    first = (tmp_path / "a.html").as_uri()
    second = (other / "a.html").as_uri()
    client.open(first, FINDING)
    assert client.diagnostics(first)
    client.open(second, FINDING)
    assert client.diagnostics(second)
    client.notify("workspace/didChangeConfiguration", {"settings": None})
    assert client.diagnostics(first)


def test_takes_relative_settings_from_the_folder_of_the_document(
    client: Client, tmp_path: Path
) -> None:
    folders = [tmp_path / "one", tmp_path / "two"]
    for folder in folders:
        folder.mkdir()
    (folders[1] / "rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: found\n    patterns:\n      - needle\n",
        encoding="utf-8",
    )
    client.request(
        "initialize",
        {
            "capabilities": {},
            "initializationOptions": {"rules": "rules.yaml"},
            "workspaceFolders": [
                {"uri": folder.as_uri(), "name": folder.name} for folder in folders
            ],
        },
    )
    uri = (folders[1] / "a.html").as_uri()
    client.open(uri, "<p>needle</p>\n")
    assert "X001" in [item["code"] for item in client.diagnostics(uri)]


def test_lives_through_a_uri_that_makes_no_sense(client: Client, tmp_path: Path) -> None:
    client.request("initialize", {"capabilities": {}, "rootUri": "file://[bad"})
    client.notify(
        "textDocument/didOpen",
        {"textDocument": {"uri": 1, "languageId": "html", "version": 1, "text": ""}},
    )
    assert tmp_path.is_dir()
    assert client.stop() == 0


def test_asks_for_settings_again_after_a_late_answer(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, {"workspace": {"configuration": True}})
    uri = (tmp_path / "a.html").as_uri()
    client.settings = {"indent": 7}
    client.open(uri, UNFORMATTED)
    request_id = client.send(
        "textDocument/formatting",
        {"textDocument": {"uri": uri}, "options": {"tabSize": 2, "insertSpaces": True}},
    )
    while True:
        asked = client.messages.get(timeout=TIMEOUT_SECONDS)
        assert asked is not None
        if asked.get("method") == "workspace/configuration":
            break
    [edit] = client.response(request_id)["result"]
    assert "\n       <p>" not in edit["newText"]

    client.write({"id": asked["id"], "result": [client.settings]})
    [edit] = client.format(uri)
    assert "\n       <p>" in edit["newText"]


def test_a_late_answer_changes_what_a_pull_finds(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, {**PULL_CAPABILITIES, "workspace": {"configuration": True}})
    uri = (tmp_path / "a.html").as_uri()
    client.settings = {"ignore": "H013"}
    client.open(uri, FINDING)
    params = {"textDocument": {"uri": uri}}
    request_id = client.send("textDocument/diagnostic", params)
    while True:
        asked = client.messages.get(timeout=TIMEOUT_SECONDS)
        assert asked is not None
        if asked.get("method") == "workspace/configuration":
            break
    report = client.response(request_id)["result"]
    assert [item["code"] for item in report["items"]] == ["H013"]

    client.write({"id": asked["id"], "result": [client.settings]})
    assert (
        client.request(
            "textDocument/diagnostic", {**params, "previousResultId": report["resultId"]}
        )["items"]
        == []
    )


def test_refreshes_findings_once_a_late_answer_arrives(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, {"workspace": {"configuration": True}})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    while True:
        asked = client.messages.get(timeout=TIMEOUT_SECONDS)
        assert asked is not None
        if asked.get("method") == "workspace/configuration":
            break
    found = client.notification("textDocument/publishDiagnostics")
    assert [item["code"] for item in found["diagnostics"]] == ["H013"]

    client.settings = {"ignore": "H013"}
    client.write({"id": asked["id"], "result": [client.settings]})
    assert client.notification("textDocument/publishDiagnostics") == {
        "uri": uri,
        "version": 1,
        "diagnostics": [],
    }


def test_registers_for_changes_of_settings(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, {"workspace": {"didChangeConfiguration": {"dynamicRegistration": True}}})
    params = client.notification("client/registerCapability")
    assert params["registrations"] == [
        {"id": "djlint-settings", "method": "workspace/didChangeConfiguration"}
    ]


@pytest.mark.parametrize("pushed", [{}, {"html": {"format": True}}], ids=["empty", "other server"])
def test_keeps_settings_on_a_push_for_nothing_of_djlint(
    client: Client, tmp_path: Path, pushed: dict[str, Any]
) -> None:
    client.start(tmp_path, PUSH_CAPABILITIES, {"ignore": "H013"})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]
    client.notify("workspace/didChangeConfiguration", {"settings": pushed})
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]


def test_takes_flat_settings_of_a_push(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, PUSH_CAPABILITIES)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.notification("textDocument/publishDiagnostics")["diagnostics"]
    client.notify("workspace/didChangeConfiguration", {"settings": {"ignore": "H013"}})
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]


def test_excludes_from_the_workspace_folder(client: Client, tmp_path: Path) -> None:
    (tmp_path / "vendor").mkdir()
    client.start(tmp_path, PUSH_CAPABILITIES, {"exclude": "vendor"})
    uri = (tmp_path / "vendor" / "a.html").as_uri()
    client.open(uri, FINDING)
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]
    assert (
        client.request(
            "textDocument/formatting",
            {"textDocument": {"uri": uri}, "options": {"tabSize": 4, "insertSpaces": True}},
        )
        is None
    )


def test_excludes_past_a_nested_project(client: Client, tmp_path: Path) -> None:
    (tmp_path / ".djlintrc").write_text('{"exclude": "vendor"}', "utf-8")
    nested = tmp_path / "vendor" / "lib"
    nested.mkdir(parents=True)
    (nested / "pyproject.toml").write_text("", "utf-8")
    client.start(tmp_path, PUSH_CAPABILITIES, {"exclude": "vendor"})
    client.open((nested / "a.html").as_uri(), FINDING)
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]


def test_reads_a_named_configuration_again_with_a_watcher(client: Client, tmp_path: Path) -> None:
    named = tmp_path / "my.json"
    named.write_text("{}", "utf-8")
    client.settings = {"configuration": str(named)}
    client.start(
        tmp_path,
        {
            "workspace": {
                "configuration": True,
                "didChangeWatchedFiles": {"dynamicRegistration": True},
            }
        },
    )
    client.notification("client/registerCapability")
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.notification("textDocument/publishDiagnostics")["diagnostics"]
    named.write_text('{"ignore": "H013"}', "utf-8")
    client.notify("textDocument/didSave", {"textDocument": {"uri": uri}})
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]


def test_reads_the_configuration_again_after_a_rejected_watch(
    client: Client, tmp_path: Path
) -> None:
    client.start(tmp_path, {"workspace": {"didChangeWatchedFiles": {"dynamicRegistration": True}}})
    while True:
        asked = client.messages.get(timeout=TIMEOUT_SECONDS)
        assert asked is not None
        if asked.get("method") == "client/registerCapability":
            break
    client.write({"id": asked["id"], "error": {"code": -32601, "message": "No"}})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.notification("textDocument/publishDiagnostics")["diagnostics"]
    (tmp_path / ".djlintrc").write_text('{"ignore": "H013"}', "utf-8")
    client.notify("textDocument/didSave", {"textDocument": {"uri": uri}})
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]


def test_a_save_without_a_watcher_updates_every_document(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, PUSH_CAPABILITIES)
    first = (tmp_path / "a.html").as_uri()
    second = (tmp_path / "b.html").as_uri()
    client.open(first, FINDING)
    client.open(second, FINDING)
    client.notification("textDocument/publishDiagnostics")
    client.notification("textDocument/publishDiagnostics")
    (tmp_path / ".djlintrc").write_text('{"ignore": "H013"}', "utf-8")
    client.notify("textDocument/didSave", {"textDocument": {"uri": first}})
    published = [client.notification("textDocument/publishDiagnostics") for _ in range(2)]
    assert {item["uri"] for item in published} == {first, second}
    assert not any(item["diagnostics"] for item in published)


def test_a_save_without_a_watcher_refreshes_a_pulling_editor(
    client: Client, tmp_path: Path
) -> None:
    client.start(
        tmp_path, {**PULL_CAPABILITIES, "workspace": {"diagnostics": {"refreshSupport": True}}}
    )
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    client.notify("textDocument/didSave", {"textDocument": {"uri": uri}})
    assert client.notification("workspace/diagnostic/refresh") == {}


def test_asks_for_settings_again_when_folders_change(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, {"workspace": {"configuration": True}})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.notification("textDocument/publishDiagnostics")["diagnostics"]
    client.settings = {"ignore": "H013"}
    client.notify("workspace/didChangeWorkspaceFolders", {"event": {"added": [], "removed": []}})
    assert not client.notification("textDocument/publishDiagnostics")["diagnostics"]


@pytest.mark.parametrize("length", [99999999999999999999999, 1099511627776000], ids=["big", "huge"])
def test_lives_through_a_length_it_cannot_read(client: Client, length: int) -> None:
    stdin = client.process.stdin
    assert stdin is not None
    stdin.write(b"Content-Length: %d\r\n\r\n" % length)
    stdin.flush()
    client.start()


def test_a_uri_that_is_no_string_leaves_other_documents(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, PUSH_CAPABILITIES)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    client.notify(
        "textDocument/didOpen",
        {"textDocument": {"uri": 1, "languageId": "html", "version": 1, "text": FINDING}},
    )
    assert client.notification("textDocument/publishDiagnostics")["uri"] == uri


def test_a_text_with_lone_cr_is_replaced_up_to_its_last_line(
    client: Client, tmp_path: Path
) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, "<div>\r<p>x</p>")
    edits = client.request(
        "textDocument/formatting",
        {"textDocument": {"uri": uri}, "options": {"tabSize": 4, "insertSpaces": True}},
    )
    assert edits[0]["range"]["end"] == {"line": 1, "character": 8}


def test_exits_on_an_exit_with_an_id(client: Client) -> None:
    client.request("initialize", {"capabilities": {}})
    client.request("shutdown", {})
    client.send("exit", {})
    assert client.process.wait(TIMEOUT_SECONDS) == 0


def test_answers_a_request_with_a_method_that_is_no_method(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    client.write({"id": 7, "method": 1})
    assert client.response(7)["error"]["code"] == -32600


def test_rejects_a_second_initialize(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    response = client.response(client.send("initialize", {}))
    assert response["error"]["code"] == -32600


@pytest.mark.parametrize(
    "message",
    [
        {"method": "textDocument/didOpen", "params": []},
        {"method": "textDocument/didChange", "params": {"contentChanges": [1]}},
        {"method": "$/cancelRequest", "params": [1]},
    ],
)
def test_lives_through_malformed_params(
    client: Client, tmp_path: Path, message: dict[str, Any]
) -> None:
    client.start(tmp_path)
    client.write(message)
    assert client.stop() == 0


@pytest.mark.parametrize(
    "params",
    [{"capabilities": [], "rootUri": 1}, {"capabilities": {"textDocument": 1, "workspace": 2}}],
)
def test_starts_with_nonsense(client: Client, params: dict[str, Any]) -> None:
    client.request("initialize", params)
    assert client.stop() == 0


def test_passes_over_an_unknown_setting(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, options={"nonsense": True})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri)
    assert "nonsense" in client.notification("window/logMessage")["message"]


def test_picks_the_profile_from_the_language(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    text = '<a href="/about">x</a>\n'
    client.open(uri, text)
    assert client.diagnostics(uri) == []
    client.notify("textDocument/didClose", {"textDocument": {"uri": uri}})
    client.diagnostics(uri)
    client.open(uri, text, language="htmldjango")
    assert [item["code"] for item in client.diagnostics(uri)] == ["D018"]


def test_lets_the_project_choose_the_profile(client: Client, tmp_path: Path) -> None:
    (tmp_path / ".djlintrc").write_text('{"profile": "jinja"}', encoding="utf-8")
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, '<a href="/about">x</a>\n', language="htmldjango")
    assert "D018" not in [item["code"] for item in client.diagnostics(uri)]


def test_leaves_out_an_excluded_file(client: Client, tmp_path: Path) -> None:
    (tmp_path / ".djlintrc").write_text('{"exclude": "vendor"}', encoding="utf-8")
    vendor = tmp_path / "vendor"
    vendor.mkdir()
    client.start(tmp_path)
    uri = (vendor / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri) == []
    assert client.format(uri) is None


def test_respects_the_pragma_requirement(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, options={"requirePragma": True})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri) == []
    assert client.format(uri) == []


def test_watches_the_configuration(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, {"workspace": {"didChangeWatchedFiles": {"dynamicRegistration": True}}})
    registration = client.notification_or_request("client/registerCapability")
    watchers = registration["registrations"][0]["registerOptions"]["watchers"]
    assert {"globPattern": "**/.djlintrc"} in watchers
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri)
    config = tmp_path / ".djlintrc"
    config.write_text('{"ignore": "H013"}', encoding="utf-8")
    client.notify(
        "workspace/didChangeWatchedFiles", {"changes": [{"uri": config.as_uri(), "type": 1}]}
    )
    assert client.diagnostics(uri) == []


def test_asks_a_pulling_client_to_refresh(client: Client, tmp_path: Path) -> None:
    client.start(
        tmp_path, {**PULL_CAPABILITIES, "workspace": {"diagnostics": {"refreshSupport": True}}}
    )
    client.notify("workspace/didChangeConfiguration", {"settings": None})
    client.notification_or_request("workspace/diagnostic/refresh")


def test_handles_a_document_with_no_file(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    uri = "untitled:Untitled-1"
    client.open(uri, FINDING)
    assert client.diagnostics(uri)
    assert client.format(uri) == []


def test_finds_a_path_with_spaces_and_escapes(client: Client, tmp_path: Path) -> None:
    folder = tmp_path / "a b#c"
    folder.mkdir()
    (folder / ".djlintrc").write_text('{"indent": 2}', encoding="utf-8")
    client.start(tmp_path)
    uri = (folder / "é.html").as_uri()
    client.open(uri, UNFORMATTED)
    [edit] = client.format(uri)
    assert "\n  <p>hi</p>\n" in edit["newText"]


def test_lives_through_a_broken_configuration(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, options={"rules": str(tmp_path / "missing.yaml")})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    client.diagnostics(uri)
    assert client.stop() == 0


def test_lives_through_a_rule_that_fails(client: Client, tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    (tmp_path / "broken_rule.py").write_text(
        "def run(**_):\n    raise ValueError('nope')\n", encoding="utf-8"
    )
    (tmp_path / ".djlint_rules.yaml").write_text(
        "- rule:\n    name: X001\n    message: x\n    python_module: broken_rule\n",
        encoding="utf-8",
    )
    client.start(tmp_path)
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, "<p>x</p>\n")
    assert client.diagnostics(uri) == []
    assert "nope" in client.notification("window/showMessage")["message"]
    assert client.stop() == 0


def test_rejects_a_request_before_initialize(client: Client) -> None:
    response = client.response(client.send("textDocument/formatting", {}))
    assert response["error"]["code"] == -32002


@pytest.mark.parametrize("request_id", [None, 1.5, [1], {"a": 1}, True])
def test_rejects_an_id_that_is_no_id(client: Client, tmp_path: Path, request_id: object) -> None:
    client.start(tmp_path)
    client.write({"id": request_id, "method": "shutdown"})
    while (message := client.next_message()).get("id") is not None:
        pass
    assert message["error"]["code"] == -32600
    assert client.stop() == 0


@pytest.mark.parametrize("request_id", [None, [1], {"a": 1}])
def test_passes_over_a_cancel_of_nothing(
    client: Client, tmp_path: Path, request_id: object
) -> None:
    client.start(tmp_path)
    client.notify("$/cancelRequest", {"id": request_id})
    assert client.stop() == 0


def test_starts_with_folders_that_make_no_sense(client: Client) -> None:
    client.request("initialize", {"capabilities": {}, "workspaceFolders": [{"uri": None}, None]})
    assert client.stop() == 0


def test_rejects_an_unknown_method(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    response = client.response(client.send("textDocument/hover", {}))
    assert response["error"]["code"] == -32601


def test_ignores_an_unknown_notification(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    client.notify("$/setTrace", {"value": "off"})
    assert client.stop() == 0


def test_cancels_a_waiting_request(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    client.next_id += 1
    client.notify("$/cancelRequest", {"id": client.next_id})
    client.write({"id": client.next_id, "method": "textDocument/formatting", "params": {}})
    assert client.response(client.next_id)["error"]["code"] == -32800


def test_lives_through_a_message_that_is_not_json(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    stdin = client.process.stdin
    assert stdin is not None
    stdin.write(b"Content-Length: 1\r\n\r\n{")
    stdin.flush()
    assert client.stop() == 0


def test_rejects_requests_after_shutdown(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path)
    client.request("shutdown", {})
    response = client.response(client.send("textDocument/formatting", {}))
    assert response["error"]["code"] == -32600
    client.notify("exit", {})
    assert client.process.wait(TIMEOUT_SECONDS) == 0


def test_exits_with_an_error_without_a_shutdown(client: Client) -> None:
    client.notify("exit", {})
    assert client.process.wait(TIMEOUT_SECONDS) == 1


def test_takes_settings_that_are_not_template_options(client: Client, tmp_path: Path) -> None:
    client.start(tmp_path, options={"version": True})
    uri = (tmp_path / "a.html").as_uri()
    client.open(uri, FINDING)
    assert client.diagnostics(uri)


def test_exits_when_the_client_goes_away(client: Client) -> None:
    stdin = client.process.stdin
    assert stdin is not None
    stdin.close()
    assert client.process.wait(TIMEOUT_SECONDS) == 1
