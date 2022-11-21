import { EditorView, basicSetup } from 'codemirror';
import { EditorState, Compartment } from '@codemirror/state';
import { html } from '@codemirror/lang-html';

let timer;

let editor = new EditorView({
  state: EditorState.create({
    extensions: [
      basicSetup,
      html(),
      EditorView.updateListener.of((v) => {
        if (v.docChanged) {
          if (timer) clearTimeout(timer);
          timer = setTimeout(() => {
            evaluatePython();
          }, 50);
        }
      }),
    ],
    doc: `Initializing...\n`,
  }),

  parent: document.getElementById('djlint-input'),
});

let output = new EditorView({
  state: EditorState.create({
    extensions: [basicSetup, html()],
    doc: ``,
    readonly: true,
  }),
  parent: document.getElementById('djlint-output'),
});

// add pyodide returned value to the output
function setOutput(stdout) {
  const currentValue = output.state.doc.toString();
  const endPosition = currentValue.length;
  output.dispatch({
    changes: {
      from: 0,
      to: endPosition,
      insert: stdout,
    },
  });
}

function setInput(stdout) {
  const currentValue = editor.state.doc.toString();
  const endPosition = currentValue.length;
  editor.dispatch({
    changes: {
      from: 0,
      to: endPosition,
      insert: stdout,
    },
  });
}

// init pyodide and show sys.version when it's loaded successfully
async function main() {
  let pyodide = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.20.0/full/',
  });

  const origin = window.location.origin;

  // build wheels with pip wheel .

  await pyodide.loadPackage([
    `${origin}/static/py/djlint-99-py3-none-any.whl`,
    `${origin}/static/py/click-99-py3-none-any.whl`,
    `${origin}/static/py/colorama-99-py3-none-any.whl`,
    `${origin}/static/py/cssbeautifier-99-py3-none-any.whl`,
    `${origin}/static/py/EditorConfig-99-py3-none-any.whl`,
    `${origin}/static/py/html_tag_names-99-py3-none-any.whl`,
    `${origin}/static/py/html_void_elements-99-py3-none-any.whl`,
    `${origin}/static/py/importlib_metadata-99-py3-none-any.whl`,
    `${origin}/static/py/jsbeautifier-99-py3-none-any.whl`,
    `${origin}/static/py/pathspec-99-py3-none-any.whl`,
    `${origin}/static/py/PyYAML-99-py3-none-any.whl`,
    `${origin}/static/py/zipp-99-py3-none-any.whl`,
  ]);

  await pyodide.loadPackage('regex');
  await pyodide.loadPackage('six');
  await pyodide.loadPackage('tomli');
  await pyodide.loadPackage('tqdm');

  console.log(
    pyodide.runPython(`
    import sys
    sys.version
  `),
  );

  setInput(`<div>
    <p>Welcome to djLint!</p>
</div>`);
  console.log('Python Ready !');
  return pyodide;
}

// run the main function
let pyodideReadyPromise = main();

// pass the editor value to the pyodide.runPython function and show the result in the output section
async function evaluatePython() {
  let pyodide = await pyodideReadyPromise;
  try {
    pyodide.runPython(`
      import io
      import os
      sys.modules['_multiprocessing'] = object
      from multiprocessing.pool import ThreadPool
      sys.stdout = io.StringIO()

      from pathlib import Path
      from djlint.reformat import reformat_file
      from djlint.settings import Config
      import tempfile

    `);

    let result = await pyodide.runPythonAsync(`
temp_file = tempfile.NamedTemporaryFile(delete=False)
temp_file.write(b"""${editor.state.doc.toString()}""")
temp_file.seek(0)
config = Config(temp_file.name)
print(Path(list(reformat_file(config, Path(temp_file.name)).keys())[0]).read_text().rstrip())
temp_file.close()
os.unlink(temp_file.name)
    `);

    let stdout = pyodide.runPython('sys.stdout.getvalue()');
    pyodide.runPython('sys.stdout.flush()');
    setOutput(stdout);
  } catch (err) {
    setOutput(err);
  }
}
