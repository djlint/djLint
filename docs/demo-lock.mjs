// Builds what the demo installs: a wheel of djLint from this checkout and a
// Pyodide lock file that names it and its dependencies, into src/static/py/.
// With the lock file the demo loads every package at once, in parallel, which
// takes about a second less than resolving them in the browser with micropip.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { loadPyodide, version } from "pyodide";

const DOCS = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.dirname(DOCS);
const OUT = path.join(DOCS, "src/static/py");
const CDN = `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;

// The worker loads Pyodide from the CDN, and a lock file only works with the
// Pyodide it was made by.
const worker = readFileSync(path.join(DOCS, "src/static/js/worker.js"), "utf8");
if (!worker.includes(CDN)) {
  throw new Error(`src/static/js/worker.js must load Pyodide ${version} from ${CDN}`);
}

/** @returns {string} The commit, which the demo shows next to the version. */
function commit() {
  const sha = process.env.CF_PAGES_COMMIT_SHA ?? process.env.GITHUB_SHA;
  if (sha) {
    return sha.slice(0, 7);
  }
  try {
    return execFileSync("git", ["rev-parse", "--short=7", "HEAD"], {
      cwd: REPO,
      encoding: "utf8",
    }).trim();
  } catch {
    return "";
  }
}

const pyodide = await loadPyodide();
await pyodide.loadPackage("micropip");

// The checkout is copied rather than mounted, so the build reads no
// __pycache__ or compiled module, and writes nothing into it.
const BUILD = "/build";
pyodide.FS.mkdirTree(BUILD);
for (const name of ["pyproject.toml", "README.md", "LICENSE", "LICENSE-THIRD-PARTY"]) {
  pyodide.FS.writeFile(`${BUILD}/${name}`, readFileSync(path.join(REPO, name)));
}
for (const entry of readdirSync(path.join(REPO, "src/djlint"), {
  recursive: true,
  withFileTypes: true,
})) {
  const relative = path.relative(REPO, path.join(entry.parentPath, entry.name));
  if (!entry.isFile() || /__pycache__|\.(pyc|pyd|so)$/u.test(relative)) {
    continue;
  }
  const target = `${BUILD}/${relative.replaceAll("\\", "/")}`;
  pyodide.FS.mkdirTree(path.posix.dirname(target));
  pyodide.FS.writeFile(target, readFileSync(path.join(REPO, relative)));
}

pyodide.globals.set("COMMIT", commit());
const wheelPath = await pyodide.runPythonAsync(`
import os
import re

import micropip

await micropip.install("hatchling")
from hatchling.build import build_wheel

os.chdir("${BUILD}")
if COMMIT:
    with open("pyproject.toml", encoding="utf-8") as f:
        pyproject = f.read()
    pyproject = re.sub(r'(?m)^version = "([^"]+)"$', rf'version = "\\1+g{COMMIT}"', pyproject, count=1)
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject)
"/dist/" + build_wheel("/dist")
`);
await pyodide.runPythonAsync(`
import micropip

await micropip.install("emfs:${wheelPath}")
`);

/** @type {{ info: object, packages: Record<string, { file_name: string, sha256: string, depends: string[] }> }} */
const frozen = JSON.parse(pyodide.runPython("import micropip; micropip.freeze()"));
const wheel = pyodide.FS.readFile(wheelPath);
const wheelName = path.posix.basename(wheelPath);

// Only djLint and what it depends on, not all of Pyodide's packages.
/** @type {typeof frozen.packages} */
const packages = {};
const queue = ["djlint"];
for (const name of queue) {
  if (name in packages) {
    continue;
  }
  const entry = frozen.packages[name];
  if (!entry) {
    throw new Error(`micropip.freeze() left out ${name}`);
  }
  packages[name] = entry;
  queue.push(...entry.depends);
}
// Relative to the lock file, which is served next to the wheel.
packages.djlint.file_name = wheelName;
packages.djlint.sha256 = createHash("sha256").update(wheel).digest("hex");
for (const [name, entry] of Object.entries(packages)) {
  if (name !== "djlint" && !/^https:\/\//u.test(entry.file_name)) {
    entry.file_name = CDN + path.posix.basename(entry.file_name);
  }
}

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });
writeFileSync(path.join(OUT, wheelName), wheel);
writeFileSync(path.join(OUT, "pyodide-lock.json"), JSON.stringify({ info: frozen.info, packages }));
console.log(`Demo: ${wheelName} with ${Object.keys(packages).length - 1} dependencies`);
