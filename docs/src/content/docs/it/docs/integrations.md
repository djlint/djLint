---
title: "Integrazioni"
description: "Usa djLint nel tuo editor ed eseguilo con pre-commit."
---

Qualunque editor tu usi, installa djLint dove l'editor può trovarlo, idealmente nell'ambiente virtuale del progetto, e avvia l'editor da lì oppure indicagli il `djlint` di quell'ambiente. In questo modo l'editor esegue la versione fissata dal progetto, con gli stessi risultati del tuo hook di pre-commit o della CI.

Se il progetto installa djLint con [npm](/it/docs/getting-started/#installazione), il suo comando è `node_modules/.bin/djlint` nel progetto, oppure `node_modules/.bin/djlint.cmd` su Windows. Le versioni di djLint su npm precedenti alla 1.54.0 non lo hanno. Dove un editor qui sotto esegue `djlint`, indicagli quel percorso. Il percorso è relativo: se l'editor esegue djLint da una cartella diversa da quella con `node_modules`, indica il percorso completo. Le estensioni per VS Code e Zed lo trovano da sole.

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

Serve djLint 1.49 o successivo nel PATH, 1.54.0 o successivo installato nel progetto con npm, oppure [uv](https://docs.astral.sh/uv/), che esegue djLint senza installarlo. Il suo [README](https://github.com/djlint/djlint-zed#readme) spiega come renderla il formattatore di un linguaggio e descrive le sue impostazioni.

## Neovim

Neovim non assegna un filetype ad alcune estensioni dei template. Qualunque opzione qui sotto usi, registrale prima:

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Client LSP integrato (consigliato)

Neovim 0.11 o successivo può comunicare direttamente con il [server di linguaggio](#server-di-linguaggio) di djLint, senza plugin. Così ottieni le segnalazioni mentre scrivi, con gli intervalli sottolineati, e `vim.lsp.buf.format()` per la formattazione.

[nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) dalla v2.13.0 in poi include la configurazione di djLint, quindi con esso basta una riga:

```lua
vim.lsp.enable("djlint")
```

Per djLint installato con npm nel progetto, metti `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })` prima di quella riga, con `"node_modules/.bin/djlint.cmd"` su Windows.

Senza nvim-lspconfig, o con una versione precedente, definisci tu la configurazione:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = {
    "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
    "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
  },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

In entrambi i casi Neovim non formatta da solo al salvataggio. Per farlo, aggiungi anche questo alla configurazione:

```lua
local group = vim.api.nvim_create_augroup("djlint_format", {})
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    if vim.lsp.get_client_by_id(args.data.client_id).name ~= "djlint" then
      return
    end
    vim.api.nvim_clear_autocmds({ group = group, buffer = args.buf })
    vim.api.nvim_create_autocmd("BufWritePre", {
      group = group,
      buffer = args.buf,
      callback = function()
        vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
      end,
    })
  end,
})
```

Vedi [Impostazioni](#impostazioni).

### conform.nvim e nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatta e [nvim-lint](https://github.com/mfussenegger/nvim-lint) esegue il lint, avviando djLint come comando. Le segnalazioni non hanno un intervallo sottolineato e arrivano solo quando chiedi a nvim-lint di eseguire il lint. Il profilo viene dalla [configurazione](/it/docs/configuration/#profile) del progetto, come da riga di comando. Questo esempio richiede djLint 1.49 o successivo.

```lua
local formatters, linters = {}, {}
for _, filetype in ipairs({
  "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
  "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
}) do
  formatters[filetype] = { "djlint" }
  linters[filetype] = { "djlint" }
end
require("conform").setup({
  formatters_by_ft = formatters,
  formatters = { djlint = { prepend_args = { "--stdin-filename", "$FILENAME" } } },
})
local lint = require("lint")
lint.linters_by_ft = linters
vim.list_extend(lint.linters.djlint.args, {
  "--stdin-filename",
  function()
    return vim.api.nvim_buf_get_name(0)
  end,
})
```

### none-ls

- [Repository GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formattazione](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [Pacchetto npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

In PyCharm e negli altri IDE basati su IntelliJ, usa il plugin gratuito [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Installa LSP4IJ dal Marketplace.
1. Apri la finestra degli strumenti LSP Consoles e aggiungi un nuovo server di linguaggio.
1. Nella scheda **Server**, imposta il nome su `djLint` e il comando su `djlint --lsp`, con il percorso completo del `djlint` presente nell'ambiente virtuale del progetto se non è nel PATH.
1. Nella scheda **Mappings**, aggiungi i pattern di nomi di file dei tuoi template. Se la configurazione del progetto non ha un [profilo](/it/docs/configuration/#profile), lo sceglie l'ID del linguaggio di ciascun pattern:

   | Pattern                               | ID del linguaggio                 |
   | ------------------------------------- | --------------------------------- |
   | `*.html`, `*.htm`                     | `html`, o `htmldjango` con Django |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                           |
   | `*.njk`, `*.twig`                     | `nunjucks`                        |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                      |
   | `*.liquid`                            | `liquid`                          |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                          |
   | `*.tera`                              | `tera`                            |
   | `*.mako`                              | `mako`                            |

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

Helix può eseguire il [server di linguaggio](#server-di-linguaggio) da `languages.toml`. Un elenco `language-servers` sostituisce quello che Helix ha per quel linguaggio, quindi tieni i suoi server dopo `djlint`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server", "superhtml"]

[[language]]
name = "htmldjango"
language-servers = ["djlint", "djlsp", "vscode-html-language-server", "superhtml"]

[[language]]
name = "gotmpl"
language-servers = ["djlint", "gopls"]

[[language]]
name = "jinja"
language-servers = ["djlint"]

[[language]]
name = "nunjucks"
language-servers = ["djlint"]

[[language]]
name = "twig"
language-servers = ["djlint"]

[[language]]
name = "tera"
language-servers = ["djlint"]
```

Helix da solo non apre nessun file come `htmldjango`. In un progetto Django, aggiungi `file-types = ["html"]` a quella voce nel `.helix/languages.toml` del progetto.

## Emacs

Eglot, incluso in Emacs 29 e versioni successive:

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Poi esegui `M-x eglot` in un template. `eglot-format-buffer` lo formatta. `html-mode`, `mhtml-mode` e `web-mode` non indicano alcun linguaggio di template, quindi lì il profilo viene dalla [configurazione](/it/docs/configuration/#profile) del progetto.

## Agenti di programmazione

I [plugin di djLint](https://github.com/djlint/agent-plugins) passano a un agente di programmazione le segnalazioni sui template che modifica, così le corregge prima di andare avanti. Richiedono djLint 1.49 o successivo nel PATH, oppure nell'ambiente virtuale del progetto se avvii l'agente con quell'ambiente attivo. Eseguono il lint dei file corrispondenti ai pattern della tabella in [IDE JetBrains](#ide-jetbrains). Imposta il [profilo](/it/docs/configuration/#profile) nella configurazione del progetto, che tutti seguono.

Un agente che lavora nel tuo editor, come quelli di Cursor, Windsurf o Zed, o Copilot in VS Code, vede invece le segnalazioni dell'estensione djLint dell'editor.

### Claude Code

Il plugin esegue il [server di linguaggio](#server-di-linguaggio), le cui segnalazioni Claude Code mostra al modello dopo ogni modifica. In una sessione:

```text
/plugin marketplace add djlint/agent-plugins
/plugin install djlint@djlint
```

Claude Code non aggiorna da solo i plugin di altri marketplace. Attiva l'aggiornamento automatico per il marketplace `djlint` in `/plugin`, oppure esegui `claude plugin update djlint@djlint`.

### Codex

Un hook esegue il lint dei template che l'agente aggiunge o modifica e aggiunge le segnalazioni al risultato della sua modifica. Funziona con il Node.js nel PATH.

```bash
codex plugin marketplace add djlint/agent-plugins
codex plugin add djlint@djlint
```

Codex esegue l'hook solo dopo che lo hai segnato come attendibile in `/hooks`, e chiede di nuovo conferma dopo ogni aggiornamento. Per aggiornare, esegui `codex plugin marketplace upgrade djlint`, poi `codex plugin add djlint@djlint`.

### GitHub Copilot CLI

Lo stesso hook di Codex, con il Node.js nel PATH:

```bash
copilot plugin marketplace add djlint/agent-plugins
copilot plugin install djlint@djlint
```

Per aggiornare, esegui `copilot plugin update djlint`.

### Gemini CLI

Lo stesso hook, in un'estensione:

```bash
gemini extensions install https://github.com/djlint/agent-plugins
```

Per aggiornare, esegui `gemini extensions update djlint`.

### OpenCode

Un plugin che aggiunge le segnalazioni al risultato di ogni modifica, in OpenCode 2:

```bash
opencode plugin add github:djlint/agent-plugins#main
```

OpenCode 1 e i suoi fork, come Kilo Code, lo accettano in `opencode.json`:

```json
{ "plugin": ["github:djlint/agent-plugins#main"] }
```

Si aggiorna da solo dal branch `main`.

### Crush

Crush esegue il server di linguaggio da `crush.json` e mostra all'agente le sue segnalazioni dopo ogni modifica:

```json
{
  "lsp": {
    "djlint": {
      "command": "djlint",
      "args": ["--lsp"],
      "filetypes": [
        "html",
        "htm",
        "jinja",
        "jinja2",
        "j2",
        "njk",
        "twig",
        "hbs",
        "handlebars",
        "mustache",
        "liquid",
        "gotmpl",
        "gohtml",
        "tera",
        "mako"
      ]
    }
  }
}
```

### Aider

Aider esegue il lint dei file che modifica e passa al modello ciò che stampa il linter. Per eseguire il lint dei file HTML con djLint:

```bash
aider --lint-cmd "html: djlint --lint"
```

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

Ognuno di questi profili ha un hook che esegue il lint, elencato qui, e uno che formatta, con lo stesso nome più `reformat`: `djlint-reformat-django` per `djlint-django`. Impostano `--profile` e i file che pre-commit passa. `angular` non ha hook propri: aggiungi `args: [--profile=angular]` a `djlint` o `djlint-reformat`.

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

Per template con altre estensioni, sovrascrivi `files` nella tua configurazione, e anche `types_or` dove l'hook lo imposta, perché pre-commit richiede che corrispondano entrambi. Vedi la [documentazione di pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

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
