// Not a static import: a module worker's static imports load under the page's Content Security
// Policy, which allows no CDN, and a dynamic one under the worker's own.
const { loadPyodide } = await import("https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.mjs");

/** @import { PyCallable } from "pyodide/ffi" */

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
    // The answer goes back as a plain object, with no proxies left to free.
    /** @type {unknown} */
    const run = await pyodide.runPythonAsync(`
from importlib import metadata

from js import Object, postMessage
from pyodide.ffi import to_js

from djlint.api import format_text, lint_text, load_config

version = metadata.version("djlint")
postMessage(to_js({"message": version, "type": "version"}, dict_converter=Object.fromEntries))

def _djlint_run(html, options):
    # Every edit is a run of its own, so it gets every warning, not only the
    # ones this process hasn't printed yet.
    warnings = []
    config = load_config(**options.to_py(), on_warning=warnings.append)
    findings = [finding._asdict() for finding in lint_text(config, html)]
    return to_js(
        {"findings": findings, "html": format_text(config, html).rstrip(), "warnings": warnings},
        dict_converter=Object.fromEntries,
    )

_djlint_run
`);
    if (!(run instanceof pyodide.ffi.PyCallable)) {
      throw new TypeError("_djlint_run is not callable");
    }
    return run;
  } catch (e) {
    globalThis.postMessage({ message: "error", type: "status" });
    throw e;
  }
}

const run = await loadDjlint();

// The page sends djlint.api.load_config's keyword arguments, with numbers as numbers, and
// gets back the formatted text, the findings on the original and what djLint warned about the
// settings.
globalThis.addEventListener(
  "message",
  /**
   * @param {MessageEvent<{ html: string, id: number, options: Record<string, unknown> }>} event
   *   The template and the settings to run djLint with.
   */
  ({ data: { html, id, options } }) => {
    try {
      globalThis.postMessage({ ...run(html, options), id, type: "result" });
    } catch (e) {
      globalThis.postMessage({
        id,
        message: e instanceof Error ? e.message : String(e),
        type: "error",
      });
    }
  },
);
globalThis.postMessage({ message: "ready", type: "status" });
