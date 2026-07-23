import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.2/full/pyodide.mjs";

// [djLint Config kwarg, config key from editor.js, value kind]
const CONFIG_ARGS = [
  ["profile", "profile", "string"],
  ["indent", "indent", "value"],
  ["preserve_leading_space", "preserveLeadingSpace", "bool"],
  ["preserve_blank_lines", "preserveBlankSpace", "bool"],
  ["preserve_class_newlines", "preserveClassNewlines", "bool"],
  ["format_js", "formatJs", "bool"],
  ["indent_js", "indentJs", "value"],
  ["format_css", "formatCss", "bool"],
  ["indent_css", "indentCss", "value"],
  ["custom_blocks", "customBlocks", "string"],
  ["ignore_blocks", "ignoreBlocks", "string"],
  ["custom_html", "customHtml", "string"],
  ["max_line_length", "maxLineLength", "value"],
  ["max_attribute_length", "maxAttributeLength", "value"],
  ["max_blank_lines", "maxBlankLines", "value"],
  ["format_attribute_template_tags", "formatAttributeTemplateTags", "bool"],
  ["single_attribute_per_line", "singleAttributePerLine", "bool"],
  ["format_attribute_js_json", "formatAttributeJsJson", "bool"],
  ["format_attribute_js_json_pattern", "formatAttributeJsJsonPattern", "string"],
  ["format_attribute_js_json_min_props", "formatAttributeJsJsonMinProps", "value"],
  ["blank_line_after_tag", "blankLineAfterTag", "string"],
  ["blank_line_before_tag", "blankLineBeforeTag", "string"],
  ["close_void_tags", "closeVoidTags", "bool"],
  ["ignore_case", "ignoreCase", "bool"],
  ["line_break_after_multiline_tag", "lineBreakAfterMultilineTag", "bool"],
  ["no_line_after_yaml", "noLineAfterYaml", "bool"],
  ["no_set_formatting", "noSetFormatting", "bool"],
  ["no_function_formatting", "noFunctionFormatting", "bool"],
];

// Build a plain JS object of djLint Config kwargs from the editor settings.
// Passed to Python via toPy (a dict) instead of interpolating into source.
function buildConfig(config) {
  const options = {};
  for (const [name, key, kind] of CONFIG_ARGS) {
    const value = config[key];
    if (!value) continue;
    options[name] = kind === "value" ? Number(value) : value;
  }
  return options;
}

let pyodide;
let formatHtml;

async function loadPyodideAndPackages() {
  pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v314.0.2/full/",
  });
  self.postMessage({ type: "status", message: "Loading micropip" });
  await pyodide.loadPackage("micropip");
  self.postMessage({ type: "status", message: "Installing djLint" });
  const micropip = pyodide.pyimport("micropip");
  await micropip.install("djlint");
  self.postMessage({
    type: "version",
    message: await pyodide.runPythonAsync(`
import platform
from importlib import metadata

f"Running with Python {platform.python_version()}; djLint {metadata.version('djlint')}"
`),
  });
  // Call the library API directly. Config("-") is stdin mode (no filesystem
  // walking); options is a dict unpacked into Config's keyword arguments.
  formatHtml = await pyodide.runPythonAsync(`
from djlint.reformat import formatter
from djlint.settings import Config

def _djlint_format(html, options):
    return formatter(Config("-", **options), html).rstrip()

_djlint_format
`);
  self.postMessage({ type: "status", message: "ready" });
}

const pyodideReadyPromise = loadPyodideAndPackages();

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
