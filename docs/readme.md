# djLint Docs

The docs are built with [Astro Starlight](https://starlight.astro.build).

## Running the docs website locally

1. Change into the docs dir: `cd docs`
2. Install node deps: `npm install --ignore-scripts`
3. Start the dev server: `npm start`

`npm run build` writes the static site to `_site/`.

## Where things are

- `src/content/docs/` holds the pages as Markdown, English at the root and a folder per translation (`zh/`, `ja/`, `es/`, `pt-br/`, `ru/`, `ko/`, `fr/`, `de/`, `zh-tw/`, `it/`, `pl/`, `cs/`, `tr/`). A page missing from a translation falls back to the English one.
- `src/content/i18n/` holds the strings the custom components use; Starlight translates its own interface.
- `src/data/configuration.json` lists every option shown on the configuration page, and `src/data/cli-help.txt` is the `djlint --help` output the getting started page shows. Both are checked against djLint by the tests.
- The changelog page shows the repository's `CHANGELOG.md`.
- `src/components/` holds the home page, the configuration options, the online demo and the header with the section links.

## How the demo works

The demo is running python as a webworker in web assembly from [pyodide](https://pyodide.org/en/stable/index.html).

Before the site is built, `demo-lock.mjs` builds a wheel of djLint from this checkout, resolves its dependencies with `micropip` in Node and writes the wheel and a Pyodide lock file naming them all into `public/static/py/`. An integration in `astro.config.mjs` runs it when Astro starts, so `npm run build` and `npm start` both have it.

When the page is opened, a web worker starts, loads Pyodide with that lock file and loads djLint, which loads all of its dependencies at once (see `public/static/js/worker.js`). The demo runs the djLint of the commit the site was built from, and shows that commit next to the version.

Once the worker responds "ready" the web UI is shown.
