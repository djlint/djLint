---
title: "Integrationen"
description: "djLint in Ihrem Editor verwenden und mit pre-commit ausführen."
---

Egal welchen Editor Sie verwenden: Installieren Sie djLint dort, wo der Editor es findet, am besten in der virtuellen Umgebung des Projekts, und starten Sie den Editor von dort aus oder verweisen Sie ihn auf das `djlint` dieser Umgebung. So führt der Editor die Version aus, die Ihr Projekt festlegt, mit denselben Ergebnissen wie Ihr pre-commit-Hook oder Ihre CI.

## Visual Studio Code

Installieren Sie die [djLint-Erweiterung](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) aus dem Visual Studio Marketplace. Cursor, Windsurf, VSCodium und andere auf VS Code basierende Editoren beziehen [dieselbe Erweiterung über Open VSX](https://open-vsx.org/extension/monosans/djlint). Sie findet djLint in Ihrer Umgebung, greift sonst auf ein mitgeliefertes djLint zurück und verwendet den Sprachserver, wenn Ihr djLint ihn mitbringt.

Das [README](https://github.com/djlint/djlint-vscode#readme) der Erweiterung beschreibt ihre Einstellungen und welches djLint sie ausführt.

## Zed

Die [djLint-Erweiterung](https://github.com/djlint/djlint-zed) führt den [Sprachserver](#sprachserver) in HTML und in den Sprachen der Template-Erweiterungen aus, etwa Django, Jinja und Twig. Sie ist noch nicht in der Erweiterungsliste von Zed, installieren Sie sie daher als Dev-Erweiterung:

1. Installieren Sie Rust über [rustup](https://rustup.rs), Zed baut die Erweiterung damit und fügt das Target `wasm32-wasip2` selbst hinzu. Mit einem Rust aus anderer Quelle, etwa Homebrew oder Nix, fügen Sie es selbst hinzu.
1. Klonen Sie die Erweiterung:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. Öffnen Sie in Zed die Befehlspalette (`cmd-shift-p` auf macOS, sonst `ctrl-shift-p`), führen Sie **zed: install dev extension** aus und wählen Sie den geklonten Ordner `djlint-zed`.

Zum Aktualisieren führen Sie in diesem Ordner `git pull` aus und danach **zed: rebuild dev extension**.

Sie braucht djLint 1.49 oder neuer im PATH oder [uv](https://docs.astral.sh/uv/), das djLint ohne Installation ausführt. Ihr [README](https://github.com/djlint/djlint-zed#readme) zeigt, wie Sie sie als Formatter einer Sprache festlegen, und beschreibt ihre Einstellungen.

## Neovim

### Integrierter LSP-Client (empfohlen)

Neovim 0.11 oder neuer kann ohne Plug-in direkt mit dem [Sprachserver](#sprachserver) von djLint kommunizieren. Damit erhalten Sie Befunde schon während der Eingabe, mit unterstrichenen Bereichen, und zum Formatieren `vim.lsp.buf.format()`:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = {
    "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "twig",
    "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
  },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Um beim Speichern zu formatieren, ergänzen Sie dieselbe Konfiguration um Folgendes:

```lua
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    if vim.lsp.get_client_by_id(args.data.client_id).name ~= "djlint" then
      return
    end
    vim.api.nvim_create_autocmd("BufWritePre", {
      buffer = args.buf,
      callback = function()
        vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
      end,
    })
  end,
})
```

Siehe [Einstellungen](#einstellungen).

### conform.nvim und nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatiert und [nvim-lint](https://github.com/mfussenegger/nvim-lint) lintet, indem sie djLint als Befehl ausführen. Befunde haben keinen unterstrichenen Bereich und kommen erst, wenn Sie nvim-lint zum Linten auffordern.

```lua
local formatters, linters = {}, {}
for _, filetype in ipairs({
  "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "twig",
  "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
}) do
  formatters[filetype] = { "djlint" }
  linters[filetype] = { "djlint" }
end
require("conform").setup({ formatters_by_ft = formatters })
require("lint").linters_by_ft = linters
```

### none-ls

- [GitHub-Repository](https://github.com/nvimtools/none-ls.nvim)
- [Linten](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatieren](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [npm-Paket](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains-IDEs

Verwenden Sie in PyCharm und den anderen IDEs auf Basis von IntelliJ das kostenlose Plug-in [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Installieren Sie LSP4IJ aus dem Marketplace.
1. Öffnen Sie das Toolfenster „LSP Consoles“ und fügen Sie einen neuen Sprachserver hinzu.
1. Setzen Sie auf dem Tab **Server** den Namen auf `djLint` und den Befehl auf `djlint --lsp`, mit dem vollständigen Pfad des `djlint` in der virtuellen Umgebung des Projekts, falls es nicht im PATH liegt.
1. Fügen Sie auf dem Tab **Mappings** die Dateinamensmuster Ihrer Templates hinzu. Hat die Konfiguration des Projekts kein [Profil](/de/docs/configuration/#profile), wählt die Sprach-ID eines Musters es aus:

   | Muster                                | Sprach-ID                      |
   | ------------------------------------- | ------------------------------ |
   | `*.html`, `*.htm`                     | `html`, in Django `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                        |
   | `*.njk`, `*.twig`                     | `nunjucks`                     |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                   |
   | `*.liquid`                            | `liquid`                       |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                       |
   | `*.tera`                              | `tera`                         |
   | `*.mako`                              | `mako`                         |

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

Installieren Sie SublimeLinter und [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) über Package Control. djLint muss in dem PATH liegen, den Sublime Text sieht.

## Helix

Helix kann den [Sprachserver](#sprachserver) über `languages.toml` ausführen. Eine Liste `language-servers` ersetzt die, die Helix für diese Sprache hat, also behalten Sie dessen eigene Server nach `djlint` bei:

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

## Emacs

Eglot, das ab Emacs 29 mitgeliefert wird:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode)
                 . ("djlint" "--lsp"))))
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

`--sarif` schreibt ein SARIF-2.1.0-Dokument nach stdout und sonst nichts, sodass es sich wie oben umleiten lässt. Jede aktivierte Regel wird mit einem Link zu ihrer Dokumentation aufgeführt, jeder Befund enthält Zeile und Spalte, und mit `--check` wird eine Datei, die neu formatiert würde, unter einer Regel `formatting` gemeldet.

## pre-commit

djLint lässt sich als [pre-commit](https://pre-commit.com)-Hook sowohl als Linter als auch als Formatter verwenden.

Diese Profile haben jeweils einen Hook zum Linten, hier aufgeführt, und einen zum Formatieren mit demselben Namen plus `reformat`: `djlint-reformat-django` zu `djlint-django`. Sie setzen `--profile` und die Dateien, die pre-commit übergibt. `angular` hat keine eigenen Hooks: Geben Sie `djlint` oder `djlint-reformat` `args: [--profile=angular]` mit.

| Hook                | Profil     | Dateien                              |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | keins      | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Für Templates mit anderen Dateiendungen überschreiben Sie `files` in Ihrer Konfiguration und, wo der Hook es setzt, auch `types_or`, da bei pre-commit beides passen muss. Siehe die [Dokumentation von pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

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

[MegaLinter](https://megalinter.io) enthält djLint. Führen Sie `npx mega-linter-runner --install` aus, um es einzurichten, und lesen Sie die Optionen auf [seiner Seite zu djLint](https://megalinter.io/latest/descriptors/html_djlint/) nach.
