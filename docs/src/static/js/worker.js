importScripts('https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js');

function capitalize(raw_word) {
  const word = raw_word.toString();
  return word.charAt(0).toUpperCase() + word.slice(1);
}

async function loadPyodideAndPackages() {
  const origin = location.origin;

  self.pyodide = await loadPyodide();
  // build wheels with pip wheel .

  await self.pyodide.loadPackage([
    `${origin}/static/py/djlint-99-py3-none-any.whl`,
    `${origin}/static/py/click-99-py3-none-any.whl`,
    `${origin}/static/py/colorama-99-py3-none-any.whl`,
    `${origin}/static/py/cssbeautifier-99-py3-none-any.whl`,
    `${origin}/static/py/EditorConfig-99-py3-none-any.whl`,
    `${origin}/static/py/html_tag_names-99-py3-none-any.whl`,
    `${origin}/static/py/html_void_elements-99-py3-none-any.whl`,
    `${origin}/static/py/jsbeautifier-99-py3-none-any.whl`,
    `${origin}/static/py/pathspec-99-py3-none-any.whl`,
    `${origin}/static/py/PyYAML-99-py3-none-any.whl`,
    `${origin}/static/py/json5-99-py3-none-any.whl`,
  ]);

  postMessage({
    type: 'status',
    message:
      'Installing djlint, click, colorama, cssbeautifier, editorconfig, html_tag_names, html_void_elements, jsbeautifier, pathspec, pyyaml ..',
  });
  await self.pyodide.loadPackage('regex');
  postMessage({ type: 'status', message: 'Installing regex..' });
  await self.pyodide.loadPackage('six');
  postMessage({ type: 'status', message: 'Installing six..' });
  await self.pyodide.loadPackage('tomli');
  postMessage({ type: 'status', message: 'Installing tomli..' });
  await self.pyodide.loadPackage('tqdm');
  postMessage({ type: 'status', message: 'Installing tqdm..' });

  postMessage({
    type: 'version',
    message: pyodide.runPython(`
    import platform
    from importlib import metadata
    f"running with Python {platform.python_version()}; djLint {metadata.version('djlint')}"
  `),
  });

  postMessage({ type: 'status', message: 'ready' });
  return pyodide;
}

let pyodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
  await pyodideReadyPromise;

  const { id, config, html } = event.data;

  const profile = config.profile ? `\n,profile="${config.profile}"` : '';
  const indent = config.indent ? `\n,indent=${config.indent}` : '';
  const preserveLeadingSpace = config.preserveLeadingSpace
    ? `\n,preserve_leading_space=${capitalize(config.preserveLeadingSpace)}`
    : '';
  const preserveBlankSpace = config.preserveBlankSpace
    ? `\n,preserve_blank_lines=${capitalize(config.preserveBlankSpace)}`
    : '';
  const formatJs = config.formatJs
    ? `\n,format_js=${capitalize(config.formatJs)}`
    : '';
  const formatCss = config.formatCss
    ? `\n,format_css=${capitalize(config.formatCss)}`
    : '';
  const customBlocks = config.customBlocks
    ? `config.custom_blocks="${config.customBlocks}"`
    : '';
  const customHtml = config.customHtml
    ? `config.custom_html="${config.customHtml}"`
    : '';
  const maxLineLength = config.maxLineLength
    ? `config.max_line_length=${config.maxLineLength}`
    : '';
  const maxAttributeLength = config.maxAttributeLength
    ? `config.max_attribute_length=${config.maxAttributeLength}`
    : '';
  const formatAttributeTemplateTags = config.formatAttributeTemplateTags
    ? `config.format_attribute_template_tags=${capitalize(
        config.formatAttributeTemplateTags,
      )}`
    : '';
  const blankLineAfterTag = config.blankLineAfterTag
    ? `config.blank_line_after_tag="${config.blankLineAfterTag}"`
    : '';
  const closeVoidTags = config.closeVoidTags
    ? `config.close_void_tags="${config.closeVoidTags}"`
    : '';

  const ignoreCase = config.ignoreCase
    ? `config.ignore_case="${config.ignoreCase}"`
    : '';

  const lineBreakAfterMultilineTag = config.lineBreakAfterMultilineTag
    ? `config.line_break_after_multiline_tag="${config.lineBreakAfterMultilineTag}"`
    : '';

  const noLineAfterYaml = config.noLineAfterYaml
    ? `config.no_line_after_yaml="${config.noLineAfterYaml}"`
    : '';

  const blankLineBeforeTag = config.blankLineBeforeTag
    ? `config.blank_line_before_tag="${config.blankLineBeforeTag}"`
    : '';

  const noSetFormatting = config.noSetFormatting
    ? `config.no_set_formatting="${config.noSetFormatting}"`
    : '';

  const noFunctionFormatting = config.noFunctionFormatting
    ? `config.no_function_formatting="${config.noFunctionFormatting}"`
    : '';

  try {
    await self.pyodide.runPythonAsync(`
      import io
      import os
      import sys
      sys.modules['_multiprocessing'] = object
      from multiprocessing.pool import ThreadPool
      sys.stdout = io.StringIO()

      from pathlib import Path
      from djlint.reformat import reformat_file
      from djlint.settings import Config
      import tempfile

    `);
    await self.pyodide.runPythonAsync('sys.stdout.flush()');

    await pyodide.runPythonAsync(`
temp_file = tempfile.NamedTemporaryFile(delete=False)
temp_file.write(str.encode("""${html}"""))
temp_file.seek(0)
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
print(Path(list(reformat_file(config, Path(temp_file.name)).keys())[0]).read_text().rstrip())
temp_file.close()
os.unlink(temp_file.name)
    `);

    let stdout = await self.pyodide.runPythonAsync('sys.stdout.getvalue()');
    await self.pyodide.runPythonAsync('sys.stdout.flush()');
    postMessage({ type: 'html', message: stdout, id: id });
  } catch (err) {
    self.postMessage({ type: 'error', message: err.message, id: id });
  }
};
