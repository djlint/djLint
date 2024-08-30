importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js");

function capitalize(raw_word) {
  const word = raw_word.toString();
  return word.charAt(0).toUpperCase() + word.slice(1);
}

async function loadPyodideAndPackages() {
  const origin = location.origin;

  self.pyodide = await loadPyodide();
  self.postMessage({ type: "status", message: "Loading micropip" });
  await self.pyodide.loadPackage("micropip");
  self.postMessage({ type: "status", message: "Importing micropip" });
  const micropip = await self.pyodide.pyimport("micropip");
  self.postMessage({ type: "status", message: "Installing djLint" });
  await micropip.install([
    // These packages have no prebuilt wheels
    `${origin}/static/py/cssbeautifier-99-py3-none-any.whl`,
    `${origin}/static/py/EditorConfig-99-py3-none-any.whl`,
    `${origin}/static/py/jsbeautifier-99-py3-none-any.whl`,

    "djlint",
  ]);
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

  const profile = config.profile ? ` ,profile="${config.profile}"` : "";
  const indent = config.indent ? ` ,indent=${config.indent}` : "";
  const preserveLeadingSpace = config.preserveLeadingSpace
    ? ` ,preserve_leading_space=${capitalize(config.preserveLeadingSpace)}`
    : "";
  const preserveBlankSpace = config.preserveBlankSpace
    ? ` ,preserve_blank_lines=${capitalize(config.preserveBlankSpace)}`
    : "";
  const formatJs = config.formatJs
    ? ` ,format_js=${capitalize(config.formatJs)}`
    : "";
  const formatCss = config.formatCss
    ? ` ,format_css=${capitalize(config.formatCss)}`
    : "";
  const customBlocks = config.customBlocks
    ? `config.custom_blocks="${config.customBlocks}"`
    : "";
  const customHtml = config.customHtml
    ? `config.custom_html="${config.customHtml}"`
    : "";
  const maxLineLength = config.maxLineLength
    ? `config.max_line_length=${config.maxLineLength}`
    : "";
  const maxAttributeLength = config.maxAttributeLength
    ? `config.max_attribute_length=${config.maxAttributeLength}`
    : "";
  const formatAttributeTemplateTags = config.formatAttributeTemplateTags
    ? `config.format_attribute_template_tags=${capitalize(config.formatAttributeTemplateTags)}`
    : "";
  const blankLineAfterTag = config.blankLineAfterTag
    ? `config.blank_line_after_tag="${config.blankLineAfterTag}"`
    : "";
  const closeVoidTags = config.closeVoidTags
    ? `config.close_void_tags="${config.closeVoidTags}"`
    : "";

  const ignoreCase = config.ignoreCase
    ? `config.ignore_case="${config.ignoreCase}"`
    : "";

  const lineBreakAfterMultilineTag = config.lineBreakAfterMultilineTag
    ? `config.line_break_after_multiline_tag="${config.lineBreakAfterMultilineTag}"`
    : "";

  const noLineAfterYaml = config.noLineAfterYaml
    ? `config.no_line_after_yaml="${config.noLineAfterYaml}"`
    : "";

  const blankLineBeforeTag = config.blankLineBeforeTag
    ? `config.blank_line_before_tag="${config.blankLineBeforeTag}"`
    : "";

  const noSetFormatting = config.noSetFormatting
    ? `config.no_set_formatting="${config.noSetFormatting}"`
    : "";

  const noFunctionFormatting = config.noFunctionFormatting
    ? `config.no_function_formatting="${config.noFunctionFormatting}"`
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
      temp_file.name${indent}${profile}${preserveLeadingSpace}${preserveBlankSpace}${formatJs}${formatCss}
    )
    ${customBlocks}
    ${customHtml}
    ${maxLineLength}
    ${maxAttributeLength}
    ${formatAttributeTemplateTags}
    ${blankLineAfterTag}
    ${blankLineBeforeTag}
    ${closeVoidTags}
    ${ignoreCase}
    ${lineBreakAfterMultilineTag}
    ${noLineAfterYaml}
    ${blankLineBeforeTag}
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
