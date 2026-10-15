# djLint Docs

Docs are made with [11ty](https://www.11ty.dev).

## Running the docs website locally

1. change into the docs dir. `cd docs`
2. install node deps. `npm install --ignore-scripts`
3. turn on the website. `npm start`

## How the demo works

The demo is running python as a webworker in web assembly from [pyodide](https://pyodide.org/en/stable/index.html).

When the page is opened, a web worker starts, loads Pyodide and installs the latest djLint and its dependencies from PyPI with `micropip` (see `src/static/js/worker.js`).

Once the worker responds "ready" the web UI is shown.
