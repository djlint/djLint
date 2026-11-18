#!/usr/bin/env node
// Runs djLint on the Python of the package for this platform, one of the
// optional dependencies, of which npm installs the one whose os, cpu and libc
// match.
import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import path from "node:path";

const require = createRequire(import.meta.url);
const { optionalDependencies } = require("./package.json");

// What djLint's console script does, with the command named as it is there.
const MAIN = "import sys; from djlint._cli import main; sys.argv[0] = 'djlint'; sys.exit(main())";
const INSTALL = "https://djlint.com/docs/getting-started/#installation";

function fail(message) {
  console.error(`djlint: ${message}`);
  process.exit(1);
}

function platform() {
  if (process.platform !== "linux") {
    return `${process.platform}-${process.arch}`;
  }
  // Node reports the version of glibc it runs on, and nothing on musl.
  process.report.excludeNetwork = true;
  const libc = process.report.getReport().header.glibcVersionRuntime ? "gnu" : "musl";
  return `linux-${process.arch}-${libc}`;
}

const name = `@djlint/${platform()}`;
if (!Object.hasOwn(optionalDependencies, name)) {
  fail(`the npm package has no build for ${name.slice(8)}. Install djLint from PyPI: ${INSTALL}`);
}
let python;
try {
  const manifest = require.resolve(`${name}/package.json`);
  python = path.join(path.dirname(manifest), require(manifest).python);
} catch {
  fail(
    `${name} isn't installed. npm leaves this optional dependency out with --omit=optional, and so does a lock file made without it. Reinstall djlint.`,
  );
}

// -I keeps the settings, packages and folder of some other Python out of this one.
const child = spawn(python, ["-I", "-c", MAIN, ...process.argv.slice(2)], { stdio: "inherit" });

// Ctrl+C in a terminal reaches djLint too, which stops on its own. Passing it
// on as well would interrupt djLint again while it handles the first one.
process.on("SIGINT", () => {});
for (const signal of ["SIGHUP", "SIGTERM"]) {
  process.on(signal, () => {
    child.kill(signal);
  });
}
child.on("error", (error) => {
  fail(`could not run ${python}: ${error.message}`);
});
child.on("exit", (code, signal) => {
  if (signal) {
    // Ends the same way, for whatever waits on it.
    process.removeAllListeners(signal);
    process.kill(process.pid, signal);
  } else {
    process.exitCode = code;
  }
});
