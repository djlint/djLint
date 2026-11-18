#!/usr/bin/env node
// Runs djLint on the Python of the package for this platform, one of the optional dependencies, of which npm installs the one whose os, cpu and libc match.
// Built by npm/build.py with esbuild, for the oldest Node in the engines of the package.
import { spawn } from "node:child_process";
import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";

// What djLint's console script does, with the command named as it is there.
const MAIN = "import sys; from djlint._cli import main; sys.argv[0] = 'djlint'; sys.exit(main())";
const INSTALL = "https://djlint.com/docs/getting-started/#installation";

function fail(message: string): never {
  process.stderr.write(`djlint: ${message}\n`);
  process.exit(1);
}

async function readManifest(file: string): Promise<Record<string, unknown>> {
  const manifest: unknown = JSON.parse(await readFile(file, "utf8"));
  if (typeof manifest !== "object" || manifest === null) {
    throw new TypeError(`${file} holds no object`);
  }
  return { ...manifest };
}

type Libc = "gnu" | "musl" | undefined;

function isMuslObject(file: unknown): boolean {
  return typeof file === "string" && (file.includes("libc.musl-") || file.includes("ld-musl-"));
}

// Node reports the glibc it runs on, and the shared objects it loaded, musl's among them.
function reportedLibc(): Libc {
  // Reverse DNS lookups of open sockets, which the libc doesn't need, can stall the report.
  Object.assign(process.report ?? {}, { excludeNetwork: true });
  // The types of Node 16 have the report as a string, which it isn't.
  const report: unknown = process.report?.getReport();
  if (typeof report !== "object" || report === null) {
    return void 0;
  }
  const header: unknown = "header" in report ? report.header : null;
  if (typeof header === "object" && header !== null && "glibcVersionRuntime" in header) {
    return "gnu";
  }
  const objects: unknown = "sharedObjects" in report ? report.sharedObjects : null;
  return Array.isArray(objects) && objects.some((file) => isMuslObject(file)) ? "musl" : void 0;
}

// How npm tells the libc apart when it picks the optional dependency to install.
// The ldd script names musl or the GNU C Library; only without it does the report decide.
async function libc(): Promise<Libc> {
  const ldd = await readFile("/usr/bin/ldd", "latin1").catch(() => null);
  if (ldd === null) {
    return reportedLibc();
  }
  if (ldd.includes("musl")) {
    return "musl";
  }
  return ldd.includes("GNU C Library") ? "gnu" : void 0;
}

async function platform(): Promise<string> {
  if (process.platform !== "linux") {
    return `${process.platform}-${process.arch}`;
  }
  const family = await libc();
  if (!family) {
    fail(
      `can't tell the libc of this Linux, and neither can npm, so it installed no Python for it. Install djLint from PyPI: ${INSTALL}`,
    );
  }
  return `linux-${process.arch}-${family}`;
}

const require = createRequire(import.meta.url);
const { optionalDependencies } = await readManifest(require.resolve("./package.json"));
if (typeof optionalDependencies !== "object" || optionalDependencies === null) {
  throw new TypeError("package.json has no optionalDependencies");
}
const name = `@djlint/${await platform()}`;
if (!Object.hasOwn(optionalDependencies, name)) {
  fail(`the npm package has no build for ${name.slice(8)}. Install djLint from PyPI: ${INSTALL}`);
}
let python = "";
try {
  const manifest = require.resolve(`${name}/package.json`);
  const { python: interpreter } = await readManifest(manifest);
  if (typeof interpreter !== "string" || !interpreter) {
    throw new TypeError(`${manifest} names no Python`);
  }
  python = path.join(path.dirname(manifest), interpreter);
} catch {
  fail(
    `${name} isn't installed. npm leaves this optional dependency out with --omit=optional, and so does a lock file made without it. Reinstall djlint.`,
  );
}

// -I keeps the settings, packages and folder of some other Python out of this one.
const child = spawn(python, ["-I", "-c", MAIN, ...process.argv.slice(2)], { stdio: "inherit" });

process.on("SIGINT", () => {
  // Ctrl+C in a terminal reaches djLint too, which stops on its own. Passing it on as well would interrupt djLint again while it handles the first one.
});
for (const signal of ["SIGHUP", "SIGTERM"] as const) {
  process.on(signal, () => {
    child.kill(signal);
  });
}
child.on("error", (error) => {
  fail(`could not run ${python}: ${error.message}`);
});
child.on("exit", (code, signal) => {
  if (signal == null) {
    process.exitCode = code ?? 1;
  } else {
    // Ends the same way, for whatever waits on it.
    process.removeAllListeners(signal);
    process.kill(process.pid, signal);
  }
});
