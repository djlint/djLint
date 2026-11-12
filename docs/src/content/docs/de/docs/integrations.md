---
title: "Integrationen"
description: "djLint in Ihrem Editor verwenden und mit pre-commit ausführen."
sidebar:
  label: "Integrationen"
---

Für djLint gibt es mehrere Editor-Integrationen.

Egal welchen Editor Sie verwenden: Installieren Sie djLint dort, wo der Editor es findet, am besten in der virtuellen Umgebung des Projekts, und starten Sie den Editor von dort aus oder verweisen Sie ihn auf das `djlint` dieser Umgebung. So führt der Editor die Version aus, die Ihr Projekt festlegt, mit denselben Ergebnissen wie Ihr pre-commit-Hook oder Ihre CI.

## Visual Studio Code

Installieren Sie die [djLint-Erweiterung](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) oder für VSCodium [die Erweiterung auf Open VSX](https://open-vsx.org/extension/monosans/djlint). Sie findet djLint in Ihrer Umgebung, greift sonst auf ein mitgeliefertes djLint zurück und verwendet den Sprachserver, wenn Ihr djLint ihn mitbringt.

Der Code der Erweiterung liegt auf [GitHub](https://github.com/djlint/djlint-vscode).

## Zed

Installieren Sie die [djLint-Erweiterung](https://github.com/djlint/djlint-zed), die den [Sprachserver](#sprachserver) startet. Die Befunde erscheinen gleich nach der Installation in HTML und in den Sprachen der Template-Erweiterungen. Sie braucht djLint 1.49 oder neuer. Sie startet das `djlint` aus dem PATH oder, wenn dort keins ist, djLint über uv; ein anderes legen Sie mit `lsp.djlint.binary.path` fest.

Um mit djLint zu formatieren, machen Sie es zum Formatierer einer Sprache:

```json
{ "languages": { "HTML": { "formatter": { "language_server": { "name": "djlint" } } } } }
```

[Einstellungen](#einstellungen) stehen unter `lsp.djlint.settings`.

## Neovim

djLint lässt sich in Neovim als Linter und als Formatter verwenden.

### Integrierter LSP-Client (empfohlen)

Neovim 0.11 oder neuer kann ohne Plug-in direkt mit dem [Sprachserver](#sprachserver) von djLint kommunizieren. Damit erhalten Sie Befunde schon während der Eingabe, mit unterstrichenen Bereichen, und zum Formatieren `vim.lsp.buf.format()`:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Um beim Speichern zu formatieren, ergänzen Sie dieselbe Konfiguration um Folgendes:

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

Siehe [Einstellungen](#einstellungen).

### conform.nvim und nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatiert und [nvim-lint](https://github.com/mfussenegger/nvim-lint) lintet, indem sie djLint als Befehl ausführen. Befunde haben keinen unterstrichenen Bereich und kommen erst, wenn Sie nvim-lint zum Linten auffordern.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [GitHub-Repository](https://github.com/nvimtools/none-ls.nvim)
- [Linten](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatieren](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [GitHub-Repository](https://github.com/mattn/efm-langserver)

1. Installieren Sie efm-langserver und djLint mit Mason über `:MasonInstall efm djlint`.
1. Fügen Sie `htmldjango` zu `filetypes` hinzu.
1. Legen Sie eine Formatierungskonfiguration an:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Verbinden Sie die Sprache mit `htmldjango = { djlint }` mit dem Formatter.

Beispielkonfiguration:

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

### coc.nvim

- [npm-Paket](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains-IDEs

Verwenden Sie in PyCharm und den anderen IDEs auf Basis von IntelliJ das kostenlose Plug-in [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Installieren Sie LSP4IJ aus dem Marketplace.
1. Öffnen Sie das Toolfenster „LSP Consoles“ und fügen Sie einen neuen Sprachserver hinzu.
1. Setzen Sie auf dem Tab **Server** den Namen auf `djLint` und den Befehl auf `djlint --lsp`, mit dem vollständigen Pfad des `djlint` in der virtuellen Umgebung des Projekts, falls es nicht im PATH liegt.
1. Fügen Sie auf dem Tab **Mappings** ein Dateinamensmuster für Ihre Templates hinzu, etwa `*.html`. Hat die Konfiguration des Projekts kein [Profil](/de/docs/configuration/#profile), setzen Sie bei einem Django-Projekt die Sprach-ID auf `htmldjango`, damit das richtige gewählt wird.
1. Auf dem Tab **Configuration** können Sie [Einstellungen](#einstellungen) als JSON unter einem Schlüssel `djlint` festlegen.

Die Befunde erscheinen im Editor, und **Reformat Code** kann den Server für die zugeordneten Dateien verwenden.

## Sublime Text

### LSP (empfohlen)

Das Paket [LSP](https://packagecontrol.io/packages/LSP) führt den [Sprachserver](#sprachserver) aus, der Befunde schon während der Eingabe liefert und formatiert.

Führen Sie **Preferences: LSP Server Configurations** aus und fügen Sie Folgendes hinzu:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint lässt sich als Linter-Plug-in für Sublime Text verwenden. Installieren können Sie es über [Package Control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. SublimeLinter installieren
3. SublimeLinter-contrib-djlint installieren

Stellen Sie sicher, dass djLint in Ihrem globalen Python installiert ist oder in Ihrem `PATH` liegt.

## Helix

Helix kann den [Sprachserver](#sprachserver) über `languages.toml` ausführen:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, das ab Emacs 29 mitgeliefert wird:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Führen Sie dann in einem Template `M-x eglot` aus. `eglot-format-buffer` formatiert es.

## Sprachserver

`djlint --lsp` startet djLint als Sprachserver über stdio. Er läuft dauerhaft, sodass ein Editor schon während der Eingabe Befunde erhält und ein Dokument formatiert, ohne jedes Mal einen Prozess zu starten.

Er meldet Befunde und formatiert ganze Dokumente. Er benötigt keine zusätzlichen Pakete. Jeder andere Editor, der LSP spricht, kann ihn mit demselben Befehl ausführen.

### Einstellungen

Der Server liest die [Konfiguration](/de/docs/configuration/) des Projekts so wie die Befehlszeile, vom Ordner jeder Datei aus aufwärts. Einstellungen aus dem Editor haben Vorrang vor ihr, können aber wie auf der Befehlszeile nur eine Option einschalten oder einen Wert setzen: `false` schaltet nicht aus, was das Projekt einschaltet. Sie tragen die Namen der [Befehlszeilenoptionen](/de/docs/configuration/), mit Unterstrichen oder in camelCase, und für kommagetrennte Werte lassen sich Listen verwenden:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Der Server fragt den Abschnitt `djlint` über `workspace/configuration` ab. Ein Editor, der darauf nicht antworten kann, kann dieselben Schlüssel in `initializationOptions` senden.

Zwei Einstellungen haben keine Befehlszeilenoption:

- `use_editor_indentation`: Mit der Tabulatorgröße des Editors formatieren statt mit `indent`.
- `python_rules`: Auf `false` setzen, um benutzerdefinierte Regeln mit einem `python_module` zu überspringen. So wird kein Code des Projekts ausgeführt.

djLint übernimmt das `profile` aus der ersten dieser Quellen, die eines angibt:

1. Die Einstellungen des Editors.
1. Die Konfiguration des Projekts.
1. Die Sprache des Dokuments: `htmldjango` führt zum Beispiel das Profil `django` aus.

Gibt keine davon eines an, läuft djLint wie auf der Befehlszeile ohne Profil. Ein `profile` in der Konfiguration des Projekts ist die einfachste Wahl: Es funktioniert in jedem Editor, ohne dass eine Sprach-ID eingerichtet werden muss.

### Verhalten

- Befunde kommen nach einer kurzen Tipppause. Ein Editor mit Pull-Diagnosen fragt sie ab, jeder andere bekommt sie zugeschickt.
- `exclude`, `extend_exclude` und `use_gitignore` gelten für geöffnete Dokumente. Ein ausgeschlossenes Dokument hat keine Befunde und wird nicht formatiert.
- Der Server lädt die Konfiguration neu, wenn sich `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` oder `.gitignore` ändern, sofern der Editor Dateien überwachen kann, und andernfalls, wenn ein Dokument geöffnet oder gespeichert wird. Dateien, die über `configuration` oder `rules` angegeben sind, werden neu gelesen, wenn ein Dokument geöffnet oder gespeichert wird. Eine Änderung am Code im `python_module` einer benutzerdefinierten Regel erfordert einen Neustart.
- Eine langsame Regel hält alles auf, was danach kommt, denn der Server erledigt eine Sache nach der anderen.

## GitHub Actions

In einem GitHub-Actions-Workflow meldet djLint jeden Befund als Annotation, sodass er direkt im Diff eines Pull Requests erscheint. Eine Konfiguration ist nicht nötig: djLint erkennt den Workflow und stellt die Ausgabe automatisch um.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Mit `--no-github-output` erhalten Sie stattdessen die einfache Konsolenausgabe, mit `--github-output` erzwingen Sie Annotationen auch außerhalb von Actions.

Annotationen gehören zu einem einzelnen Pull Request. Um Befunde im Tab „Security“ des Repositorys aufzubewahren, mit einem Verlauf über mehrere Läufe hinweg, schreiben Sie sie als SARIF und laden Sie die Datei hoch:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Der Upload-Schritt benötigt die Berechtigung `security-events: write` für den Job oder den Workflow.

`--sarif` schreibt ein SARIF-2.1.0-Dokument nach stdout und sonst nichts, sodass es sich wie oben umleiten lässt. Jede aktivierte Regel wird mit einem Link zu ihrer Dokumentation aufgeführt, jeder Befund enthält Zeile und Spalte, und mit `--check` wird eine Datei, die neu formatiert würde, unter einer Regel `formatting` gemeldet. Azure DevOps, GitLab und die meisten Editoren lesen dasselbe Format.

## Pre-Commit

djLint lässt sich als [pre-commit](https://pre-commit.com)-Hook sowohl als Linter als auch als Formatter verwenden.

Das Repository stellt mehrere vorkonfigurierte Hooks für bestimmte djLint-Profile bereit (sie setzen lediglich das Argument `--profile` vorab und teilen pre-commit mit, nach welchen Dateiendungen gesucht werden soll):

- `djlint` zum Linten und `djlint-reformat` zum Formatieren
  Sucht nach Dateien, die auf `*.html` passen, ohne `--profile` zu setzen.
- `djlint-django` und `djlint-reformat-django`
  Sucht nach Dateien, die auf `*.html` passen, und setzt `--profile=django`.
- `djlint-jinja` und `djlint-reformat-jinja`
  Sucht nach Dateien, die auf `*.j2`,`*.jinja` oder `*.jinja2` passen, und setzt `--profile=jinja`.
- `djlint-nunjucks` und `djlint-reformat-nunjucks`
  Sucht nach Dateien, die auf `*.njk` passen, und setzt `--profile=nunjucks`.
- `djlint-handlebars` und `djlint-reformat-handlebars`
  Sucht nach Dateien, die auf `*.hbs` passen, und setzt `--profile=handlebars`.
- `djlint-liquid` und `djlint-reformat-liquid`
  Sucht nach Dateien, die auf `*.html` passen, und setzt `--profile=liquid`.
- `djlint-golang` und `djlint-reformat-golang`
  Sucht nach Dateien, die auf `*.gotmpl` passen, und setzt `--profile=golang`.
- `djlint-tera` und `djlint-reformat-tera`
  Sucht nach Dateien, die auf `*.html` passen, und setzt `--profile=tera`.
- `djlint-askama` und `djlint-reformat-askama`
  Sucht nach Dateien, die auf `*.html` passen, und setzt `--profile=askama`.
- `djlint-mako` und `djlint-reformat-mako`
  Sucht nach Dateien, die auf `*.html` passen, und setzt `--profile=mako`.

Beachten Sie, dass diese vordefinierten Hooks bei den akzeptierten Eingaben manchmal zu zurückhaltend sind (Ihre Templates verwenden vielleicht eine andere Dateiendung). Deshalb erlaubt pre-commit ausdrücklich, jede dieser vordefinierten Optionen zu überschreiben. Weitere Konfigurationsmöglichkeiten finden Sie in der [Dokumentation von pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

### Standardbeispiel für Django

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars mit der Endung .html statt .hbs

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

Mit den Parametern `files` oder `exclude` können Sie jeden Hook auf ein eigenes Verzeichnis beschränken und so mehrere Template-Sprachen im selben Repository unterstützen.

## MegaLinter

djlint ist nativ in die über 100 Linter von [MegaLinter](https://megalinter.io) eingebunden.

Zur Installation führen Sie einfach `npx mega-linter-runner --install` aus und folgen den Anweisungen.

- [GitHub-Repository](https://github.com/oxsecurity/megalinter)
- [djlint in der Dokumentation von MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
