/** @import { PyCallable } from "pyodide/ffi" */
/** @import { WorkerReply, WorkerRequest } from "../../../src/scripts/demo-worker" */

// Not a static import: a module worker's static imports load under the page's Content Security
// Policy, which allows no CDN, and a dynamic one under the worker's own.
const { loadPyodide } = await import("https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.mjs");

/**
 * Sends the page an answer.
 * @param {WorkerReply} reply - The answer.
 */
function answer(reply) {
  globalThis.postMessage(reply);
}

/**
 * Loads djLint. The page shows its own message when that fails: the error is for the console.
 * @returns {Promise<PyCallable>} The function that formats and lints a template.
 */
async function loadDjlint() {
  try {
    // The demo-lock.mjs script builds djLint from the checkout the site is built from, and the
    // lock file names its dependencies, so they all load at once.
    const pyodide = await loadPyodide({
      lockFileURL: new URL("/static/py/pyodide-lock.json", globalThis.location.href).href,
    });
    await pyodide.loadPackage("djlint");
    /** @type {unknown} */
    const version = await pyodide.runPythonAsync(`
from importlib import metadata

metadata.version("djlint")
`);
    if (typeof version !== "string") {
      throw new TypeError("djLint has no version");
    }
    answer({ message: version, type: "version" });
    // The answer goes back as a plain object, with no proxies left to free: a value with no JS
    // counterpart fails the conversion instead.
    /** @type {unknown} */
    const run = await pyodide.runPythonAsync(`
from js import Object
from pyodide.ffi import to_js

from djlint.api import format_text, lint_text, load_config

def _djlint_run(html, options):
    # Every edit is a run of its own, so it gets every warning, not only the
    # ones this process hasn't printed yet.
    warnings = []
    config = load_config(**options.to_py(), on_warning=warnings.append)
    findings = [finding._asdict() for finding in lint_text(config, html)]
    return to_js(
        {"findings": findings, "html": format_text(config, html).rstrip(), "warnings": warnings},
        create_pyproxies=False,
        dict_converter=Object.fromEntries,
    )

_djlint_run
`);
    if (!(run instanceof pyodide.ffi.PyCallable)) {
      throw new TypeError("_djlint_run is not callable");
    }
    return run;
  } catch (e) {
    answer({ message: "error", type: "status" });
    throw e;
  }
}

const run = await loadDjlint();

/**
 * Whether Python answered with every field of a result.
 * @param {unknown} value - What djLint's run returned.
 * @returns {value is Omit<Extract<WorkerReply, { type: "result" }>, "id" | "type">} The check.
 */
function isResult(value) {
  return (
    typeof value === "object" &&
    value !== null &&
    "findings" in value &&
    Array.isArray(value.findings) &&
    "html" in value &&
    typeof value.html === "string" &&
    "warnings" in value &&
    Array.isArray(value.warnings)
  );
}

// The page sends djlint.api.load_config's keyword arguments, with numbers as numbers, and
// gets back the formatted text, the findings on the original and what djLint warned about the
// settings.
globalThis.addEventListener(
  "message",
  /**
   * @param {MessageEvent<WorkerRequest>} event - The template and the settings to run djLint with.
   */
  ({ data: { html, id, options } }) => {
    try {
      /** @type {unknown} */
      const result = run(html, options);
      if (!isResult(result)) {
        throw new TypeError("djLint's answer lacks a field");
      }
      answer({ ...result, id, type: "result" });
    } catch (e) {
      answer({ id, message: e instanceof Error ? e.message : String(e), type: "error" });
    }
  },
);
answer({ message: "ready", type: "status" });
