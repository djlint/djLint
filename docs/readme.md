# djLint Docs

Docs are made with [11ty](https://www.11ty.dev).

## Running the docs website locally

1. change into the docs dir. `cd docs`
2. install node deps. `npm install --ignore-scripts`
3. turn on the website. `npm start`

## How the demo works

The demo is running python as a webworker in web assembly from [pyodide](https://pyodide.org/en/stable/index.html).

Before the site is built, `demo-lock.mjs` builds a wheel of djLint from this checkout, resolves its dependencies with `micropip` in Node and writes the wheel and a Pyodide lock file naming them all into `src/static/py/`. Eleventy runs it before it builds the site, from `.eleventy.js`, so `npm run build`, `npm start` and a plain `eleventy` all have it.

When the page is opened, a web worker starts, loads Pyodide with that lock file and loads djLint, which loads all of its dependencies at once (see `src/static/js/worker.js`). The demo runs the djLint of the commit the site was built from, and shows that commit next to the version.

Once the worker responds "ready" the web UI is shown.
