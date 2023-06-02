import { EditorView, basicSetup } from 'codemirror';
import { EditorState, Compartment } from '@codemirror/state';
import { html } from '@codemirror/lang-html';

let session_id = 0;
if (typeof Worker !== 'undefined') {
  console.log('creating web worker ');
  let w;

  if (typeof w == 'undefined') {
    w = new Worker('/static/js/worker.js');
  }

  function getConfig() {
    let config = {};
    const customBlocks = document.getElementById(
      'settings-custom-blocks',
    ).value;
    if (customBlocks) config['customBlocks'] = customBlocks;
    const customHtml = document.getElementById('settings-custom-html').value;
    if (customHtml) config['customHtml'] = customHtml;
    const indent = document.getElementById('settings-indent').value;
    if (indent) config['indent'] = indent;
    const blankLineAfterTag = document.getElementById(
      'settings-blank-line-after-tag',
    ).value;
    if (blankLineAfterTag) config['blankLineAfterTag'] = blankLineAfterTag;
    const blankLineBeforeTag = document.getElementById(
      'settings-blank-line-before-tag',
    ).value;
    if (blankLineBeforeTag) config['blankLineBeforeTag'] = blankLineBeforeTag;
    const profile = document.getElementById('settings-profile').value;
    if (profile) config['profile'] = profile;
    const maxLineLength = document.getElementById(
      'settings-max-line-length',
    ).value;
    if (maxLineLength) config['maxLineLength'] = maxLineLength;
    const maxAttributeLength = document.getElementById(
      'settings-max-attribute-length',
    ).value;
    if (maxAttributeLength) config['maxAttributeLength'] = maxAttributeLength;
    const formatAttributeTemplateTags = document.getElementById(
      'settings-format-attribute-template-tags',
    ).checked;
    if (formatAttributeTemplateTags)
      config['formatAttributeTemplateTags'] = formatAttributeTemplateTags;
    const preserveLeadingSpace = document.getElementById(
      'settings-preserve-leading-space',
    ).checked;
    if (preserveLeadingSpace)
      config['preserveLeadingSpace'] = preserveLeadingSpace;
    const preserveBlankSpace = document.getElementById(
      'settings-preserve-blank-space',
    ).checked;
    if (preserveBlankSpace) config['preserveBlankSpace'] = preserveBlankSpace;
    const formatJs = document.getElementById('settings-format-js').checked;
    if (formatJs) config['formatJs'] = formatJs;
    const formatCss = document.getElementById('settings-format-css').checked;
    if (formatCss) config['formatCss'] = formatCss;

    const closeVoidTags = document.getElementById(
      'settings-close-void-tags',
    ).checked;
    if (closeVoidTags) config['closeVoidTags'] = closeVoidTags;
    const ignoreCase = document.getElementById('settings-ignore-case').checked;
    if (ignoreCase) config['ignoreCase'] = ignoreCase;
    const lineBreakAfterMultilineTag = document.getElementById(
      'settings-line-break-after-multiline-tag',
    ).checked;
    if (lineBreakAfterMultilineTag)
      config['lineBreakAfterMultilineTag'] = lineBreakAfterMultilineTag;
    const noLineAfterYaml = document.getElementById(
      'settings-no-line-after-yaml',
    ).checked;
    if (noLineAfterYaml) config['noLineAfterYaml'] = noLineAfterYaml;

    const noFunctionFormatting = document.getElementById(
      'settings-no-function-formatting',
    ).checked;
    if (noFunctionFormatting)
      config['noFunctionFormatting'] = noFunctionFormatting;
    const noSetFormatting = document.getElementById(
      'settings-no-set-formatting',
    ).checked;
    if (noSetFormatting) config['noSetFormatting'] = noSetFormatting;

    return config;
  }

  const runPython = (script) => {
    session_id += 1;
    w.postMessage({
      config: getConfig(),
      html: script,
      id: session_id,
    });
  };

  w.onmessage = (event) => {
    const { id, type, message, ...data } = event.data;
    if (type == 'status') {
      const div = document.createElement('div');
      div.innerText = message;
      const status = document.getElementById('djlint-status');
      status.insertBefore(div, status.lastElementChild);

      if (message === 'ready') {
        document.getElementById('djlint-status').classList.add('is-hidden');
        document
          .getElementById('djlint-settings')
          .closest('.columns.is-hidden')
          .classList.remove('is-hidden');
        runPython(editor.state.doc.toString());
      }
    }
    if ((type == 'error' || type == 'html') && id == session_id) {
      setOutput(message);
    } else if (type == 'status') {
      console.log(message);
    } else if (type == 'version') {
      document.getElementById('djlint-version').textContent = message;
    } else {
      console.log(event.data);
    }
  };

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
              runPython(v.state.doc.toString());
            }, 100);
          }
        }),
      ],
      doc: `<div>\n    <p>Welcome to djLint online!</p>\n</div>`,
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

  document.getElementById('djlint-settings').addEventListener('change', () => {
    runPython(editor.state.doc.toString());
  });
} else {
  // Sorry! No Web Worker support..
  document
    .getElementById('djlint-status')
    .innerText(
      'Sorry, a browser that supports web workers is required to use this online tool.',
    );
}

// pass the editor value to the pyodide.runPython function and show the result in the output section

// document.getElementById("djlint-settings").addEventListener("change", () => {evaluatePython()})
