---
title: "Integrazioni"
description: "Usa djLint nel tuo editor ed eseguilo con pre-commit."
---

Qualunque editor tu usi, installa djLint dove l'editor può trovarlo, idealmente nell'ambiente virtuale del progetto, e avvia l'editor da lì oppure indicagli il `djlint` di quell'ambiente. In questo modo l'editor esegue la versione fissata dal progetto, con gli stessi risultati del tuo hook di pre-commit o della CI.

## Visual Studio Code

Installa l'[estensione djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) dal Visual Studio Marketplace. Cursor, Windsurf, VSCodium e gli altri editor basati su VS Code installano [la stessa estensione da Open VSX](https://open-vsx.org/extension/monosans/djlint). Trova djLint nel tuo ambiente, in mancanza usa una copia inclusa nell'estensione e usa il server di linguaggio quando il tuo djLint lo offre.

Il suo [README](https://github.com/djlint/djlint-vscode#readme) descrive le impostazioni e quale djLint esegue.

## Zed

L'[estensione djLint](https://github.com/djlint/djlint-zed) esegue il [server di linguaggio](#server-di-linguaggio) in HTML e nei linguaggi delle estensioni per i template, come Django, Jinja e Twig. Non è ancora nel registro delle estensioni di Zed, quindi installala come estensione di sviluppo:

1. Installa Rust con [rustup](https://rustup.rs): Zed compila l'estensione con esso e aggiunge da solo il target `wasm32-wasip2`. Con un Rust installato in altro modo, ad esempio con Homebrew o Nix, aggiungilo tu.
1. Clona l'estensione:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. In Zed, apri la palette dei comandi (`cmd-shift-p` su macOS, `ctrl-shift-p` altrove), esegui **zed: install dev extension** e scegli la cartella clonata `djlint-zed`.

Per aggiornarla, esegui `git pull` in quella cartella e poi **zed: rebuild dev extension**.

Serve djLint 1.49 o successivo nel PATH, oppure [uv](https://docs.astral.sh/uv/), che esegue djLint senza installarlo. Il suo [README](https://github.com/djlint/djlint-zed#readme) spiega come renderla il formattatore di un linguaggio e descrive le sue impostazioni.

## Neovim

### Client LSP integrato (consigliato)

Neovim 0.11 o successivo può comunicare direttamente con il [server di linguaggio](#server-di-linguaggio) di djLint, senza plugin. Così ottieni le segnalazioni mentre scrivi, con gli intervalli sottolineati, e `vim.lsp.buf.format()` per la formattazione:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Per formattare al salvataggio, aggiungi questo alla stessa configurazione:

```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = {
    "*.html", "*.jinja", "*.jinja2", "*.j2",
    "*.hbs", "*.handlebars", "*.liquid", "*.gotmpl",
  },
  callback = function(args)
    vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
  end,
})
```

Vedi [Impostazioni](#impostazioni).

### conform.nvim e nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatta e [nvim-lint](https://github.com/mfussenegger/nvim-lint) esegue il lint, avviando djLint come comando. Le segnalazioni non hanno un intervallo sottolineato e arrivano solo quando chiedi a nvim-lint di eseguire il lint.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [Repository GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formattazione](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [Repository GitHub](https://github.com/mattn/efm-langserver)

Assegna a `htmldjango` un formattatore con `formatCommand = "djlint --reformat --quiet --warn --stdin-filename ${INPUT} -"` e `formatStdin = true`.

### coc.nvim

- [Pacchetto npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

In PyCharm e negli altri IDE basati su IntelliJ, usa il plugin gratuito [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Installa LSP4IJ dal Marketplace.
1. Apri la finestra degli strumenti LSP Consoles e aggiungi un nuovo server di linguaggio.
1. Nella scheda **Server**, imposta il nome su `djLint` e il comando su `djlint --lsp`, con il percorso completo del `djlint` presente nell'ambiente virtuale del progetto se non è nel PATH.
1. Nella scheda **Mappings**, aggiungi un pattern di nomi di file per i tuoi template, ad esempio `*.html`. Se la configurazione del progetto non ha un [profilo](/it/docs/configuration/#profile), per un progetto Django imposta l'ID del linguaggio su `htmldjango`, così viene scelto quello giusto.
1. Nella scheda **Configuration** puoi indicare le [impostazioni](#impostazioni) in JSON, sotto una chiave `djlint`.

Le segnalazioni compaiono nell'editor e **Reformat Code** può usare il server per i file mappati.

## Sublime Text

### LSP (consigliato)

Il pacchetto [LSP](https://packagecontrol.io/packages/LSP) esegue il [server di linguaggio](#server-di-linguaggio), che fornisce le segnalazioni mentre scrivi e la formattazione.

Esegui **Preferences: LSP Server Configurations** e aggiungi:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Installa SublimeLinter e [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) con Package Control. djLint deve trovarsi nel PATH che vede Sublime Text.

## Helix

Helix può eseguire il [server di linguaggio](#server-di-linguaggio) da `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, incluso in Emacs 29 e versioni successive:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Poi esegui `M-x eglot` in un template. `eglot-format-buffer` lo formatta.

## Server di linguaggio

`djlint --lsp` esegue djLint come server di linguaggio su stdio. Resta in esecuzione, così un editor riceve le segnalazioni mentre scrivi e formatta un documento senza avviare ogni volta un processo.

Fornisce le segnalazioni e formatta documenti interi. Non richiede pacchetti aggiuntivi. Qualsiasi altro editor che supporta LSP può eseguirlo con lo stesso comando.

### Impostazioni

Il server legge la [configurazione](/it/docs/configuration/) del progetto come fa la riga di comando, risalendo dalla cartella di ciascun file. Le impostazioni dell'editor hanno la precedenza su di essa ma, come sulla riga di comando, possono solo attivare un'opzione o impostare un valore: `false` non disattiva ciò che il progetto attiva. Usano i nomi delle [opzioni della riga di comando](/it/docs/configuration/), con i trattini bassi o in camelCase, e per i valori separati da virgole si possono usare delle liste:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Il server richiede la sezione `djlint` con `workspace/configuration`. Un editor che non può rispondere può inviare le stesse chiavi in `initializationOptions`.

Due impostazioni non hanno un'opzione della riga di comando:

- `use_editor_indentation`: formatta con la dimensione della tabulazione dell'editor, invece di `indent`.
- `python_rules`: impostala su `false` per saltare le regole personalizzate con un `python_module`, così il codice del progetto non viene eseguito.

djLint prende il `profile` dalla prima di queste fonti che ne indica uno:

1. Le impostazioni dell'editor.
1. La configurazione del progetto.
1. Il linguaggio del documento: `htmldjango` esegue il profilo `django`, ad esempio.

Se nessuna lo indica, djLint viene eseguito senza profilo, come sulla riga di comando. Un `profile` nella configurazione del progetto è la scelta più semplice: funziona in ogni editor, senza dover impostare alcun ID di linguaggio.

### Cosa fa

- Le segnalazioni arrivano dopo una breve pausa nella digitazione. Un editor con diagnostica pull le richiede, a qualsiasi altro vengono inviate in push.
- `exclude`, `extend_exclude` e `use_gitignore` si applicano ai documenti aperti. Un documento escluso non ha segnalazioni e non viene formattato.
- Ricarica la configurazione quando cambiano `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` o `.gitignore`, se l'editor è in grado di monitorare i file, e altrimenti quando un documento viene aperto o salvato. I file indicati da `configuration` o `rules` vengono riletti quando un documento viene aperto o salvato. Una modifica al codice del `python_module` di una regola personalizzata richiede un riavvio.
- Una regola lenta fa attendere ciò che viene dopo, perché il server fa una cosa alla volta.

## GitHub Actions

In un workflow di GitHub Actions djLint riporta ogni segnalazione come annotazione, che compare quindi inline nel diff di una pull request. Non serve alcuna configurazione: djLint rileva il workflow e cambia automaticamente l'output.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Usa `--no-github-output` per ottenere invece il normale output della console, oppure `--github-output` per forzare le annotazioni al di fuori di Actions.

Le annotazioni restano legate a una singola pull request. Per conservare le segnalazioni nella scheda Security del repository, con la cronologia tra un'esecuzione e l'altra, scrivile in formato SARIF e carica il file:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Il passaggio di caricamento richiede il permesso `security-events: write` sul job o sul workflow.

`--sarif` scrive su stdout un documento SARIF 2.1.0 e nient'altro, quindi può essere reindirizzato come sopra. Ogni regola attiva è elencata con un link alla sua documentazione, ogni segnalazione riporta la sua riga e colonna e, con `--check`, un file che verrebbe riformattato viene segnalato sotto una regola `formatting`.

## pre-commit

djLint può essere usato come hook di [pre-commit](https://pre-commit.com), sia come linter sia come formattatore.

Ogni profilo ha un hook che esegue il lint, elencato qui, e uno che formatta, con lo stesso nome più `reformat`: `djlint-reformat-django` per `djlint-django`. Impostano `--profile` e i file che pre-commit passa:

| Hook                | Profilo    | File                                 |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | nessuno    | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Per template con altre estensioni, sovrascrivi `files` o `types_or` nella tua configurazione, come descrive la [documentazione di pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

### Esempio predefinito per Django

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars con estensione .html invece di .hbs

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-handlebars
        files: "\\.html"
        types_or: ["html"]
      - id: djlint-handlebars
        files: "\\.html"
        types_or: ["html"]
```

Puoi usare i parametri `files` o `exclude` per limitare ciascun hook alla propria directory, così da supportare più linguaggi di template nello stesso repository.

## MegaLinter

[MegaLinter](https://megalinter.io) include djLint. Esegui `npx mega-linter-runner --install` per configurarlo e consulta [la sua pagina su djLint](https://megalinter.io/latest/descriptors/html_djlint/) per le opzioni.
