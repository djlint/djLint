# djLint Docs

Docs are made with [11ty](https://www.11ty.dev).

## Running the docs website locally

1. change into the docs dir. `cd docs`
2. install node deps. `npm install --ignore-scripts`
3. turn on the website. `npm start`

## How the demo works

The demo is running python as a webworker in web assembly from [pyodide](https://pyodide.org/en/stable/index.html).

When the page is access a webworker starts, downloads python, installs djLint and deps (notice the wheels in `/src/static/py` that are updated when a new release is created.).

Once the worker responds "ready" the web UI is shown.
