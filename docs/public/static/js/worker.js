const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";
const { loadPyodide } = await import(`${PYODIDE_URL}pyodide.mjs`);

// The page sends the options under their Python names, all as strings or
// booleans; these ones are numbers.
const NUMBERS = new Set([
  "indent",
  "indent_css",
  "indent_js",
  "max_attribute_length",
  "max_blank_lines",
  "max_line_length",
  "format_attribute_js_json_min_props",
]);

function buildConfig(config) {
  const options = {};
  for (const [name, value] of Object.entries(config)) {
    if (value) options[name] = NUMBERS.has(name) ? Number(value) : value;
  }
  return options;
}

let pyodide;
let formatHtml;

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
  formatHtml = await pyodide.runPythonAsync(`
from djlint.api import format_text, load_config

def _djlint_format(html, options):
    return format_text(load_config(**options), html).rstrip()

_djlint_format
`);
  self.postMessage({ type: "status", message: "ready" });
}

// The page shows its own message: the error is for the console.
const pyodideReadyPromise = loadPyodideAndPackages().catch((error) => {
  self.postMessage({ type: "status", message: "error" });
  throw error;
});

self.onmessage = async (event) => {
  await pyodideReadyPromise;

  const { id, config, html } = event.data;

  const options = pyodide.toPy(buildConfig(config));
  try {
    const output = formatHtml(html, options);
    self.postMessage({ type: "html", message: output, id: id });
  } catch (err) {
    self.postMessage({ type: "error", message: err.message, id: id });
  } finally {
    options.destroy();
  }
};
