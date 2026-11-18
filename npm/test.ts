// Installs djlint and the package for this platform, which npm/build.py packed into npm/dist, and runs djLint through them:
//     DJLINT_PLATFORM=linux-x64-gnu node --test npm/test.ts
import assert from "node:assert/strict";
import { execSync, spawn, spawnSync } from "node:child_process";
import type { SpawnSyncOptionsWithStringEncoding, SpawnSyncReturns } from "node:child_process";
import { mkdirSync, mkdtempSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { after, before, test } from "node:test";

interface Message {
  id?: unknown;
  result?: { capabilities?: unknown };
}

const dist = path.join(import.meta.dirname, "dist");
const project = mkdtempSync(path.join(tmpdir(), "djlint-npm-"));
const launcher = path.join(project, "node_modules", "djlint", "djlint.mjs");
const windows = process.platform === "win32";
// On GitHub Actions, djLint reports as annotations.
const { GITHUB_ACTIONS: _, ...env } = process.env;
// The oldest Node in the engines of the package, which the CI tries it with on one platform.
const oldestNode = process.env["DJLINT_OLDEST_NODE"];

function djlint(
  args: readonly string[],
  options: Partial<SpawnSyncOptionsWithStringEncoding> = {},
): SpawnSyncReturns<string> {
  return spawnSync(process.execPath, [launcher, ...args], {
    cwd: project,
    encoding: "utf8",
    env,
    ...options,
  });
}

function frame(message: object): string {
  const body = JSON.stringify({ jsonrpc: "2.0", ...message });
  return `Content-Length: ${Buffer.byteLength(body)}\r\n\r\n${body}`;
}

function isObject(value: unknown): value is object {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

before(() => {
  // Only the package for this platform, as npm refuses one for another.
  const platform = process.env["DJLINT_PLATFORM"];
  assert.ok(platform, "set DJLINT_PLATFORM to the platform to test");
  const names = new RegExp(String.raw`^djlint-(${platform}-)?\d.*\.tgz$`, "u");
  const packages = readdirSync(dist).filter((name) => names.test(name));
  assert.equal(packages.length, 2, `npm/dist has ${packages.join(", ")}`);
  writeFileSync(path.join(project, "package.json"), '{ "private": true }\n');
  const paths = packages.map((name) => JSON.stringify(path.join(dist, name)));
  execSync(`npm install --no-audit --no-fund ${paths.join(" ")}`, {
    cwd: project,
    stdio: "inherit",
  });
});

after(() => {
  rmSync(project, { force: true, recursive: true });
});

test("npm links the command", () => {
  const output = execSync("npx --no-install djlint --version", { cwd: project, encoding: "utf8" });
  assert.match(output, /^djlint, version \d+\.\d+\.\d+/u);
});

test("runs on the oldest Node it supports", { skip: !oldestNode }, () => {
  assert.ok(oldestNode);
  const result = spawnSync(oldestNode, [launcher, "--version"], {
    cwd: project,
    encoding: "utf8",
    env,
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /^djlint, version \d+\.\d+\.\d+/u);
});

test("lints what comes in on stdin", () => {
  const result = djlint(["-", "--lint"], { input: '<div><img src="a"></div>\n' });
  assert.equal(result.status, 1, result.stderr);
  assert.match(result.stdout, /H013 1:5 Img tag should have an alt attribute/u);
});

test("formats files in more than one process", () => {
  // Enough text for djLint to start a pool of workers.
  const templates = path.join(project, "templates");
  mkdirSync(templates);
  for (let i = 0; i < 4; i += 1) {
    writeFileSync(path.join(templates, `${i}.html`), "<div><p>text</p></div>\n".repeat(3000));
  }
  const result = djlint(["templates", "--reformat"]);
  assert.equal(result.status, 1, result.stderr);
  assert.match(result.stdout, /4 files were updated/u);
  assert.equal(djlint(["templates", "--check"]).status, 0);
});

test("passes the exit code on", () => {
  const result = djlint(["--no-such-option"]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /No such option '--no-such-option'/u);
});

test("keeps the settings of another Python out", () => {
  const result = djlint(["--version"], {
    env: { ...env, PYTHONHOME: project, PYTHONPATH: project },
  });
  assert.equal(result.status, 0, result.stderr);
});

test("runs the language server", async () => {
  const server = spawn(process.execPath, [launcher, "--lsp"], { cwd: project });
  let output = "";
  server.stdout.setEncoding("utf8");
  server.stdout.on("data", (chunk: string) => {
    output += chunk;
  });
  server.stdin.write(frame({ id: 1, method: "initialize", params: { capabilities: {} } }));
  server.stdin.write(frame({ id: 2, method: "shutdown" }));
  server.stdin.end(frame({ method: "exit" }));
  const code = await new Promise((resolve) => {
    server.on("close", resolve);
  });
  assert.equal(code, 0);
  const answers = output
    .split(/Content-Length: \d+\r\n\r\n/u)
    .filter(Boolean)
    .map((body): Message => {
      const message: unknown = JSON.parse(body);
      assert.ok(isObject(message), body);
      return message;
    })
    .filter((message) => "id" in message);
  assert.deepEqual(
    answers.map((answer) => answer.id),
    [1, 2],
  );
  assert.ok(isObject(answers[0]?.result?.capabilities));
});

// Windows has no signals to send.
test("ends as djLint does when a signal stops it", { skip: windows }, async () => {
  const server = spawn(process.execPath, [launcher, "--lsp"], { cwd: project });
  // Once djLint is up, which its answer to initialize shows.
  server.stdin.write(frame({ id: 1, method: "initialize", params: { capabilities: {} } }));
  await new Promise((resolve) => {
    server.stdout.once("data", resolve);
  });
  server.kill("SIGTERM");
  const signal = await new Promise((resolve) => {
    server.on("close", (_code, received) => {
      resolve(received);
    });
  });
  assert.equal(signal, "SIGTERM");
});
