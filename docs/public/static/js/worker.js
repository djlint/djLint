import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.2/full/pyodide.mjs";

const CONFIG_ARGS = [
  { kwarg: "profile", key: "profile", kind: "string" },
  { kwarg: "indent", key: "indent", kind: "value" },
  {
    kwarg: "preserve_leading_space",
    key: "preserveLeadingSpace",
    kind: "bool",
  },
  { kwarg: "preserve_blank_lines", key: "preserveBlankSpace", kind: "bool" },
  {
    kwarg: "preserve_class_newlines",
    key: "preserveClassNewlines",
    kind: "bool",
  },
  { kwarg: "format_js", key: "formatJs", kind: "bool" },
  { kwarg: "indent_js", key: "indentJs", kind: "value" },
  { kwarg: "format_css", key: "formatCss", kind: "bool" },
  { kwarg: "indent_css", key: "indentCss", kind: "value" },
  { kwarg: "custom_blocks", key: "customBlocks", kind: "string" },
  { kwarg: "ignore_blocks", key: "ignoreBlocks", kind: "string" },
  { kwarg: "custom_html", key: "customHtml", kind: "string" },
  { kwarg: "max_line_length", key: "maxLineLength", kind: "value" },
  { kwarg: "max_attribute_length", key: "maxAttributeLength", kind: "value" },
  { kwarg: "max_blank_lines", key: "maxBlankLines", kind: "value" },
  {
    kwarg: "format_attribute_template_tags",
    key: "formatAttributeTemplateTags",
    kind: "bool",
  },
  {
    kwarg: "single_attribute_per_line",
    key: "singleAttributePerLine",
    kind: "bool",
  },
  {
    kwarg: "format_attribute_js_json",
    key: "formatAttributeJsJson",
    kind: "bool",
  },
  {
    kwarg: "format_attribute_js_json_pattern",
    key: "formatAttributeJsJsonPattern",
    kind: "string",
  },
  {
    kwarg: "format_attribute_js_json_min_props",
    key: "formatAttributeJsJsonMinProps",
    kind: "value",
  },
  { kwarg: "blank_line_after_tag", key: "blankLineAfterTag", kind: "string" },
  { kwarg: "blank_line_before_tag", key: "blankLineBeforeTag", kind: "string" },
  { kwarg: "close_void_tags", key: "closeVoidTags", kind: "bool" },
  { kwarg: "ignore_case", key: "ignoreCase", kind: "bool" },
  {
    kwarg: "line_break_after_multiline_tag",
    key: "lineBreakAfterMultilineTag",
    kind: "bool",
  },
  { kwarg: "no_line_after_yaml", key: "noLineAfterYaml", kind: "bool" },
  { kwarg: "no_set_formatting", key: "noSetFormatting", kind: "bool" },
  {
    kwarg: "no_function_formatting",
    key: "noFunctionFormatting",
    kind: "bool",
  },
];

function buildConfig(config) {
  const options = {};
  for (const { kwarg, key, kind } of CONFIG_ARGS) {
    const value = config[key];
    if (!value) continue;
    options[kwarg] = kind === "value" ? Number(value) : value;
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
