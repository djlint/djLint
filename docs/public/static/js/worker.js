const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";
const { loadPyodide } = await import(`${PYODIDE_URL}pyodide.mjs`);

let pyodide;
let run;

async function loadPyodideAndPackages() {
  // demo-lock.mjs builds djLint from the checkout the site is built from, and
  // the lock file names its dependencies, so they all load at once.
  pyodide = await loadPyodide({
    indexURL: PYODIDE_URL,
    lockFileURL: new URL("/static/py/pyodide-lock.json", self.location).href,
  });
  self.postMessage({ type: "status", message: "installing" });
  await pyodide.loadPackage("djlint");
  const versions = await pyodide.runPythonAsync(`
import platform
from importlib import metadata

[platform.python_version(), metadata.version("djlint")]
`);
  const [python, djlint] = versions.toJs();
  versions.destroy();
  self.postMessage({ type: "version", message: { python, djlint } });
  run = await pyodide.runPythonAsync(`
from djlint.api import format_text, lint_text, load_config

def _djlint_run(html, options):
    config = load_config(**options)
    findings = [finding._asdict() for finding in lint_text(config, html)]
    return format_text(config, html).rstrip(), findings

_djlint_run
`);
  self.postMessage({ type: "status", message: "ready" });
}

// The page shows its own message: the error is for the console.
const pyodideReadyPromise = loadPyodideAndPackages().catch((error) => {
  self.postMessage({ type: "status", message: "error" });
  throw error;
});

// The page sends djlint.api.load_config's keyword arguments, with numbers as
// numbers, and gets back the formatted text and the findings on the original.
self.onmessage = async ({ data: { id, options, html } }) => {
  await pyodideReadyPromise;

  const pyOptions = pyodide.toPy(options);
  try {
    const result = run(html, pyOptions);
    const [formatted, findings] = result.toJs({ dict_converter: Object.fromEntries });
    result.destroy();
    self.postMessage({ type: "result", id, html: formatted, findings });
  } catch (err) {
    self.postMessage({ type: "error", id, message: err.message });
  } finally {
    pyOptions.destroy();
  }
};
