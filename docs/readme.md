# djLint Docs

The docs are built with [Astro Starlight](https://starlight.astro.build).

## Running the docs website locally

1. Change into the docs dir: `cd docs`
2. Install node deps: `npm install --ignore-scripts`
3. Start the dev server: `npm start`

`npm run build` writes the static site to `_site/`.

## Where things are

- `src/content/docs/` holds the pages as Markdown, English at the root and a folder per translation (`ru/`, `fr/`, `zh/`). A page missing from a translation falls back to the English one.
- `src/content/i18n/` holds the strings the custom components use; Starlight translates its own interface.
- `src/data/configuration.json` lists every option shown on the configuration page, and `src/data/cli-help.txt` is the `djlint --help` output the getting started page shows. Both are checked against djLint by the tests.
- The changelog page shows the repository's `CHANGELOG.md`.
- `src/components/` holds the home page, the configuration options, the online demo and the header with the section links.

## How the demo works

The demo is running python as a webworker in web assembly from [pyodide](https://pyodide.org/en/stable/index.html).

When the page is opened, a web worker starts, loads Pyodide and installs the latest djLint and its dependencies from PyPI with `micropip` (see `public/static/js/worker.js`).

Once the worker responds "ready" the web UI is shown.
