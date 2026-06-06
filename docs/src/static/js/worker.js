importScripts("https://cdn.jsdelivr.net/pyodide/v0.29.4/full/pyodide.js");

function capitalize(raw_word) {
  const word = raw_word.toString();
  return word.charAt(0).toUpperCase() + word.slice(1);
}

function pythonString(value) {
  return JSON.stringify(value.toString());
}

function addBoolArg(args, name, value) {
  if (value) args.push(`${name}=${capitalize(value)}`);
}

function addStringArg(args, name, value) {
  if (value) args.push(`${name}=${pythonString(value)}`);
}

function addValueArg(args, name, value) {
  if (value) args.push(`${name}=${value}`);
}

async function loadPyodideAndPackages() {
  const origin = location.origin;

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

  self.postMessage({ type: "status", message: "ready" });
}

let pyodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
  await pyodideReadyPromise;

  const { id, config, html } = event.data;

  const configArgs = [];
  addStringArg(configArgs, "profile", config.profile);
  addValueArg(configArgs, "indent", config.indent);
  addBoolArg(configArgs, "preserve_leading_space", config.preserveLeadingSpace);
  addBoolArg(configArgs, "preserve_blank_lines", config.preserveBlankSpace);
  addBoolArg(
    configArgs,
    "preserve_class_newlines",
    config.preserveClassNewlines,
  );
  addBoolArg(configArgs, "format_js", config.formatJs);
  addValueArg(configArgs, "indent_js", config.indentJs);
  addBoolArg(configArgs, "format_css", config.formatCss);
  addValueArg(configArgs, "indent_css", config.indentCss);
  addStringArg(configArgs, "custom_blocks", config.customBlocks);
  addStringArg(configArgs, "ignore_blocks", config.ignoreBlocks);
  addStringArg(configArgs, "custom_html", config.customHtml);
  addValueArg(configArgs, "max_line_length", config.maxLineLength);
  addValueArg(configArgs, "max_attribute_length", config.maxAttributeLength);
  addValueArg(configArgs, "max_blank_lines", config.maxBlankLines);
  addBoolArg(
    configArgs,
    "format_attribute_template_tags",
    config.formatAttributeTemplateTags,
  );
  addBoolArg(
    configArgs,
    "format_attribute_js_json",
    config.formatAttributeJsJson,
  );
  addStringArg(
    configArgs,
    "format_attribute_js_json_pattern",
    config.formatAttributeJsJsonPattern,
  );
  addValueArg(
    configArgs,
    "format_attribute_js_json_min_props",
    config.formatAttributeJsJsonMinProps,
  );
  addStringArg(configArgs, "blank_line_after_tag", config.blankLineAfterTag);
  addStringArg(configArgs, "blank_line_before_tag", config.blankLineBeforeTag);
  addBoolArg(configArgs, "close_void_tags", config.closeVoidTags);
  addBoolArg(configArgs, "ignore_case", config.ignoreCase);
  addBoolArg(
    configArgs,
    "line_break_after_multiline_tag",
    config.lineBreakAfterMultilineTag,
  );
  addBoolArg(configArgs, "no_line_after_yaml", config.noLineAfterYaml);
  addBoolArg(configArgs, "no_set_formatting", config.noSetFormatting);
  addBoolArg(configArgs, "no_function_formatting", config.noFunctionFormatting);

  const configArguments = configArgs.length
    ? `,
      ${configArgs.join(",\n      ")}`
    : "";

  try {
    await self.pyodide.runPythonAsync(`
import sys
from types import ModuleType

sys.modules["_multiprocessing"] = ModuleType("_multiprocessing")

from io import StringIO

sys.stdout = StringIO()

from pathlib import Path
from tempfile import NamedTemporaryFile

from djlint.reformat import reformat_file
from djlint.settings import Config
`);
    await self.pyodide.runPythonAsync("sys.stdout.flush()");
    await self.pyodide.runPythonAsync(`
with NamedTemporaryFile(mode="w", encoding="utf-8", delete_on_close=False) as temp_file:
    temp_file.write("""${html}""")
    temp_file.close()
    config = Config(
      temp_file.name${configArguments}
    )
    result = Path(next(iter(reformat_file(config, Path(temp_file.name))))).read_text(encoding="utf-8")
print(result.rstrip())
`);
    const stdout = await self.pyodide.runPythonAsync("sys.stdout.getvalue()");
    await self.pyodide.runPythonAsync("sys.stdout.flush()");
    self.postMessage({ type: "html", message: stdout, id: id });
  } catch (err) {
    self.postMessage({ type: "error", message: err.message, id: id });
  }
};
