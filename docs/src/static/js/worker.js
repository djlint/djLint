importScripts("https://cdn.jsdelivr.net/pyodide/v0.29.4/full/pyodide.js");

function pythonString(value) {
  return JSON.stringify(value.toString());
}

function pythonValue(value, kind) {
  if (kind === "bool") return value ? "True" : "False";
  if (kind === "string") return pythonString(value);
  return value;
}

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
  [
    "format_attribute_js_json_pattern",
    "formatAttributeJsJsonPattern",
    "string",
  ],
  [
    "format_attribute_js_json_min_props",
    "formatAttributeJsJsonMinProps",
    "value",
  ],
  ["blank_line_after_tag", "blankLineAfterTag", "string"],
  ["blank_line_before_tag", "blankLineBeforeTag", "string"],
  ["close_void_tags", "closeVoidTags", "bool"],
  ["ignore_case", "ignoreCase", "bool"],
  ["line_break_after_multiline_tag", "lineBreakAfterMultilineTag", "bool"],
  ["no_line_after_yaml", "noLineAfterYaml", "bool"],
  ["no_set_formatting", "noSetFormatting", "bool"],
  ["no_function_formatting", "noFunctionFormatting", "bool"],
];

function buildConfigArguments(config) {
  const args = CONFIG_ARGS.flatMap(([name, key, kind]) =>
    config[key] ? [`${name}=${pythonValue(config[key], kind)}`] : [],
  );

  return args.length
    ? `,
      ${args.join(",\n      ")}`
    : "";
}

async function loadPyodideAndPackages() {
  self.pyodide = await loadPyodide();
  self.postMessage({ type: "status", message: "Loading micropip" });
  await self.pyodide.loadPackage("micropip");
  self.postMessage({ type: "status", message: "Importing micropip" });
  const micropip = await self.pyodide.pyimport("micropip");
  self.postMessage({ type: "status", message: "Installing djLint" });
  await micropip.install("djlint");
  self.postMessage({
    type: "version",
    message: await self.pyodide.runPythonAsync(`
import platform
from importlib import metadata

f"Running with Python {platform.python_version()}; djLint {metadata.version('djlint')}"
`),
  });
  await self.pyodide.runPythonAsync(`
from djlint.reformat import formatter
from djlint.settings import Config
`);

  self.postMessage({ type: "status", message: "ready" });
}

let pyodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
  await pyodideReadyPromise;

  const { id, config, html } = event.data;

  const configArguments = buildConfigArguments(config);

  try {
    self.pyodide.globals.set("djlint_html", html);
    const output = await self.pyodide.runPythonAsync(`
formatter(Config("."${configArguments}), djlint_html).rstrip()
`);
    self.postMessage({ type: "html", message: output, id: id });
  } catch (err) {
    self.postMessage({ type: "error", message: err.message, id: id });
  }
};
