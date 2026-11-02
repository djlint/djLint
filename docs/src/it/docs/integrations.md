---
description: Integra djLint con il tuo editor preferito. Formatta automaticamente i template con pre-commit. Esegui il lint con SublimeText.
title: Integrazioni
keywords: linter per template, formattatore per template, djLint, HTML, template, formattatore, linter, integrazioni, server di linguaggio, lsp, neovim, helix
---

# Integrazioni

Per djLint esistono diverse integrazioni con gli editor.

Qualunque editor tu usi, installa djLint dove l'editor può trovarlo, idealmente nell'ambiente virtuale del progetto, e avvia l'editor da lì oppure indicagli il `djlint` di quell'ambiente. In questo modo l'editor esegue la versione fissata dal progetto, con gli stessi risultati del tuo hook di pre-commit o della CI.

## Visual Studio Code

Installa l'[estensione djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), oppure [quella su Open VSX](https://open-vsx.org/extension/monosans/djlint) per VSCodium. Trova djLint nel tuo ambiente, in mancanza usa una copia inclusa nell'estensione e usa il server di linguaggio quando il tuo djLint lo offre.

Il suo codice è su [GitHub](https://github.com/djlint/djlint-vscode).

## Neovim

djLint può essere usato come linter e formattatore in Neovim.

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

::: content

- [Repository GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formattazione](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

### efm-langserver

::: content

- [Repository GitHub](https://github.com/mattn/efm-langserver)

1. Installa efm-langserver e djLint con Mason tramite `:MasonInstall efm djlint`
1. Aggiungi `htmldjango` a `filetypes`.
1. Crea la configurazione di formattazione:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Collega il linguaggio al formattatore con `htmldjango = { djlint }`.

Configurazione di esempio:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}

require("lspconfig").efm.setup({
    filetypes = { "htmldjango" },
    init_options = { documentFormatting = true },
    settings = {
        rootMarkers = { ".git/" },
        languages = {
            htmldjango = { djlint },
        },
    },
})
```

:::

### coc.nvim

::: content

- [Pacchetto npm](https://www.npmjs.com/package/coc-htmldjango)
  :::

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
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

### SublimeLinter

djLint può essere usato come plugin linter di SublimeText. Si può installare tramite [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Installa SublimeLinter
3. Installa SublimeLinter-contrib-djlint
   :::

Assicurati che djLint sia installato nel Python globale o che si trovi nel `PATH`.

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

Le annotazioni appartengono a una singola pull request. Per conservare le segnalazioni nella scheda Security del repository, con la cronologia tra un'esecuzione e l'altra, scrivile in formato SARIF e carica il file:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Il passaggio di caricamento richiede il permesso `security-events: write` sul job o sul workflow.

`--sarif` scrive su stdout un documento SARIF 2.1.0 e nient'altro, quindi può essere reindirizzato come sopra. Ogni regola attiva è elencata con un link alla sua documentazione, ogni segnalazione riporta la sua riga e colonna e, con `--check`, un file che verrebbe riformattato viene segnalato sotto una regola `formatting`. Azure DevOps, GitLab e la maggior parte degli editor leggono lo stesso formato.

## Pre-Commit

djLint può essere usato come hook di [pre-commit](https://pre-commit.com), sia come linter sia come formattatore.

Il repository fornisce diversi hook preconfigurati per specifici profili di djLint (si limitano a preimpostare l'argomento `--profile` e a indicare a pre-commit quali estensioni di file cercare):

::: content

- `djlint` per il lint e `djlint-reformat` per la formattazione
  Cerca i file che corrispondono a `*.html` senza impostare `--profile`.
- `djlint-django` e `djlint-reformat-django`
  Cerca i file che corrispondono a `*.html` e imposta `--profile=django`.
- `djlint-jinja` e `djlint-reformat-jinja`
  Cerca i file che corrispondono a `*.j2`,`*.jinja` o `*.jinja2` e imposta `--profile=jinja`.
- `djlint-nunjucks` e `djlint-reformat-nunjucks`
  Cerca i file che corrispondono a `*.njk` e imposta `--profile=nunjucks`.
- `djlint-handlebars` e `djlint-reformat-handlebars`
  Cerca i file che corrispondono a `*.hbs` e imposta `--profile=handlebars`.
- `djlint-liquid` e `djlint-reformat-liquid`
  Cerca i file che corrispondono a `*.html` e imposta `--profile=liquid`.
- `djlint-golang` e `djlint-reformat-golang`
  Cerca i file che corrispondono a `*.gotmpl` e imposta `--profile=golang`.
- `djlint-tera` e `djlint-reformat-tera`
  Cerca i file che corrispondono a `*.html` e imposta `--profile=tera`.
- `djlint-askama` e `djlint-reformat-askama`
  Cerca i file che corrispondono a `*.html` e imposta `--profile=askama`.
  :::

Nota che a volte questi hook predefiniti sono troppo restrittivi negli input che accettano (i tuoi template potrebbero usare un'estensione diversa), per questo pre-commit permette esplicitamente di sovrascrivere qualsiasi opzione predefinita. Consulta la [documentazione di pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks) per ulteriori opzioni di configurazione.

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

djlint è integrato nativamente tra gli oltre 100 linter di [MegaLinter](https://megalinter.io)

Per installarlo, basta eseguire `npx mega-linter-runner --install` e seguire le istruzioni

::: content

- [Repository GitHub](https://github.com/oxsecurity/megalinter)
- [djlint nella documentazione di MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
