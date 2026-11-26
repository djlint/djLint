---
title: "Integracje"
description: "Używaj djLint w swoim edytorze i uruchamiaj go za pomocą pre-commit."
---

Niezależnie od edytora zainstaluj djLint tam, gdzie edytor może go znaleźć, najlepiej w środowisku wirtualnym projektu, a następnie uruchamiaj edytor z tego środowiska albo wskaż mu `djlint` z tego środowiska. Dzięki temu edytor uruchamia wersję przypiętą w projekcie i daje takie same wyniki jak hook pre-commit czy CI.

Jeśli projekt instaluje djLint przez [npm](/pl/docs/getting-started/#instalacja), jego polecenie to `node_modules/.bin/djlint` w projekcie, a na Windows `node_modules\.bin\djlint.cmd`. Tam, gdzie edytor poniżej uruchamia `djlint`, podaj mu tę ścieżkę. Rozszerzenia dla VS Code i Zed znajdą go same.

## Visual Studio Code

Zainstaluj [rozszerzenie djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) z Visual Studio Marketplace. Cursor, Windsurf, VSCodium i inne edytory oparte na VS Code instalują [to samo rozszerzenie z Open VSX](https://open-vsx.org/extension/monosans/djlint). Rozszerzenie znajduje djLint w twoim środowisku, a gdy go tam nie ma, korzysta z dołączonej wersji; jeśli twój djLint ma serwer języka, rozszerzenie go używa.

Jego [README](https://github.com/djlint/djlint-vscode#readme) opisuje ustawienia rozszerzenia i to, którego djLint ono uruchamia.

## Zed

[Rozszerzenie djLint](https://github.com/djlint/djlint-zed) uruchamia [serwer języka](#serwer-jezyka) w HTML i w językach rozszerzeń szablonów, takich jak Django, Jinja i Twig. Nie ma go jeszcze w rejestrze rozszerzeń Zeda, więc zainstaluj je jako rozszerzenie deweloperskie:

1. Zainstaluj Rusta przez [rustup](https://rustup.rs): Zed buduje nim rozszerzenie i sam dodaje target `wasm32-wasip2`. Z Rustem z innego źródła, na przykład z Homebrew albo Nixa, dodaj go samodzielnie.
1. Sklonuj rozszerzenie:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. W Zedzie otwórz paletę poleceń (`cmd-shift-p` na macOS, gdzie indziej `ctrl-shift-p`), uruchom **zed: install dev extension** i wybierz sklonowany folder `djlint-zed`.

Aby je zaktualizować, uruchom w tym folderze `git pull`, a potem **zed: rebuild dev extension**.

Potrzebuje djLinta 1.49 lub nowszego w PATH lub zainstalowanego w projekcie przez npm albo [uv](https://docs.astral.sh/uv/), które uruchamia djLinta bez instalacji. Jego [README](https://github.com/djlint/djlint-zed#readme) pokazuje, jak ustawić je jako formater języka, i opisuje jego ustawienia.

## Neovim

Niektórym rozszerzeniom szablonów Neovim nie nadaje typu pliku. Niezależnie od tego, której opcji poniżej używasz, najpierw je zarejestruj:

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Wbudowany klient LSP (zalecany)

Neovim 0.11 lub nowszy może komunikować się z [serwerem języka](#serwer-jezyka) djLint bezpośrednio, bez żadnej wtyczki. Daje to zgłoszenia już podczas pisania, z podkreślonymi zakresami, oraz formatowanie przez `vim.lsp.buf.format()`.

[nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) nowszy niż v2.12.0 zawiera jego konfigurację, więc z nim wystarczy jedna linia:

```lua
vim.lsp.enable("djlint")
```

Dla djLint zainstalowanego w projekcie przez npm wstaw przed tę linię `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })`, a na Windows z `"node_modules/.bin/djlint.cmd"`.

Bez nvim-lspconfig lub z jego starszą wersją zdefiniuj konfigurację samodzielnie:

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

Aby formatować przy zapisie, dodaj do tej samej konfiguracji:

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

Zobacz [Ustawienia](#ustawienia).

### conform.nvim i nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatuje, a [nvim-lint](https://github.com/mfussenegger/nvim-lint) lintuje, uruchamiając djLint jako polecenie. Zgłoszenia nie mają podkreślonego zakresu i pojawiają się dopiero wtedy, gdy poprosisz nvim-lint o lintowanie. Profil pochodzi z [konfiguracji](/pl/docs/configuration/#profile) projektu, tak jak w wierszu poleceń. Ten przykład wymaga djLint 1.49 lub nowszego.

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

- [Repozytorium na GitHubie](https://github.com/nvimtools/none-ls.nvim)
- [Lintowanie](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatowanie](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [Pakiet npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

W PyCharmie i innych IDE opartych na IntelliJ użyj darmowej wtyczki [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Zainstaluj LSP4IJ z Marketplace.
1. Otwórz okno narzędziowe LSP Consoles i dodaj nowy serwer języka.
1. Na karcie **Server** ustaw nazwę `djLint` i polecenie `djlint --lsp`, z pełną ścieżką do `djlint` ze środowiska wirtualnego projektu, jeśli nie ma go w PATH.
1. Na karcie **Mappings** dodaj wzorce nazw plików swoich szablonów. Jeśli konfiguracja projektu nie zawiera [profilu](/pl/docs/configuration/#profile), wybiera go identyfikator języka przy wzorcu:

   | Wzorce                                | Identyfikator języka          |
   | ------------------------------------- | ----------------------------- |
   | `*.html`, `*.htm`                     | `html`, w Django `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                       |
   | `*.njk`, `*.twig`                     | `nunjucks`                    |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                  |
   | `*.liquid`                            | `liquid`                      |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                      |
   | `*.tera`                              | `tera`                        |
   | `*.mako`                              | `mako`                        |

1. Na karcie **Configuration** możesz podać [ustawienia](#ustawienia) w formacie JSON, pod kluczem `djlint`.

Zgłoszenia pojawiają się w edytorze, a **Reformat Code** może używać serwera dla zmapowanych plików.

## Sublime Text

### LSP (zalecany)

Pakiet [LSP](https://packagecontrol.io/packages/LSP) uruchamia [serwer języka](#serwer-jezyka), który zapewnia zgłoszenia podczas pisania oraz formatowanie.

Uruchom **Preferences: LSP Server Configurations** i dodaj:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Zainstaluj SublimeLinter i [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) przez Package Control. djLint musi być w PATH widocznym dla Sublime Text.

## Helix

Helix może uruchamiać [serwer języka](#serwer-jezyka) skonfigurowany w `languages.toml`. Lista `language-servers` zastępuje tę, którą Helix ma dla danego języka, więc po `djlint` zostaw jego własne serwery:

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

Helix sam nie otwiera żadnego pliku jako `htmldjango`. W projekcie Django dodaj `file-types = ["html"]` do tego wpisu w pliku `.helix/languages.toml` projektu.

## Emacs

Eglot, dostarczany z Emacsem 29 i nowszymi:

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Następnie uruchom `M-x eglot` w szablonie. `eglot-format-buffer` go sformatuje. `html-mode`, `mhtml-mode` i `web-mode` nie wskazują języka szablonów, więc w nich profil pochodzi z [konfiguracji](/pl/docs/configuration/#profile) projektu.

## Serwer języka

`djlint --lsp` uruchamia djLint jako serwer języka komunikujący się przez stdio. Serwer działa bez przerwy, więc edytor dostaje zgłoszenia podczas pisania i formatuje dokument bez każdorazowego uruchamiania nowego procesu.

Serwer przekazuje zgłoszenia i formatuje całe dokumenty. Nie wymaga dodatkowych pakietów. Każdy inny edytor obsługujący LSP może go uruchomić tym samym poleceniem.

### Ustawienia

Serwer wczytuje [konfigurację](/pl/docs/configuration/) projektu tak samo jak wiersz poleceń: od folderu każdego pliku w górę. Ustawienia z edytora mają przed nią pierwszeństwo, ale tak jak w wierszu poleceń mogą jedynie włączyć opcję lub ustawić wartość: `false` nie wyłącza tego, co włącza projekt. Mają nazwy [opcji wiersza poleceń](/pl/docs/configuration/), zapisane z podkreśleniami lub w camelCase, a wartości oddzielane przecinkami można podawać jako listy:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Serwer pobiera sekcję `djlint` przez `workspace/configuration`. Edytor, który nie potrafi na to odpowiedzieć, może wysłać te same klucze w `initializationOptions`.

Dwa ustawienia nie mają odpowiednika w wierszu poleceń:

- `use_editor_indentation`: formatowanie z rozmiarem tabulacji ustawionym w edytorze zamiast `indent`.
- `python_rules`: ustaw na `false`, aby pominąć własne reguły z `python_module`, dzięki czemu kod projektu nie zostanie uruchomiony.

djLint bierze `profile` z pierwszego z tych źródeł, które go zawiera:

1. Ustawienia edytora.
1. Konfiguracja projektu.
1. Język dokumentu: na przykład dla `htmldjango` uruchamiany jest profil `django`.

Jeśli żadne z nich go nie zawiera, djLint działa bez profilu, tak jak w wierszu poleceń. `profile` w konfiguracji projektu to najprostsze rozwiązanie: działa w każdym edytorze i nie wymaga ustawiania identyfikatora języka.

### Co robi

- Zgłoszenia pojawiają się po krótkiej przerwie w pisaniu. Edytor obsługujący diagnostykę typu pull sam o nie prosi, a każdy inny dostaje je w trybie push.
- `exclude`, `extend_exclude` i `use_gitignore` dotyczą otwartych dokumentów. Wykluczony dokument nie ma zgłoszeń i nie jest formatowany.
- Serwer ponownie wczytuje konfigurację, gdy zmieni się `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` lub `.gitignore`, jeśli edytor potrafi obserwować pliki, a w przeciwnym razie przy otwarciu lub zapisaniu dokumentu. Pliki wskazane przez `configuration` lub `rules` są wczytywane ponownie przy otwarciu lub zapisaniu dokumentu. Zmiana kodu w `python_module` własnej reguły wymaga ponownego uruchomienia serwera.
- Powolna reguła wstrzymuje wszystko, co przychodzi po niej, ponieważ serwer robi tylko jedną rzecz naraz.

## GitHub Actions

W workflow GitHub Actions djLint zgłasza każdy problem jako adnotację, dzięki czemu jest on widoczny bezpośrednio w diffie pull requesta. Nie trzeba niczego konfigurować: djLint wykrywa workflow i automatycznie przełącza format wyjścia.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Użyj `--no-github-output`, aby zamiast tego otrzymać zwykłe wyjście konsoli, lub `--github-output`, aby wymusić adnotacje poza Actions.

Adnotacje należą do jednego pull requesta. Aby przechowywać zgłoszenia na karcie Security repozytorium, wraz z historią kolejnych uruchomień, zapisz je w formacie SARIF i prześlij plik:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Krok przesyłania wymaga uprawnienia `security-events: write` dla zadania lub workflow.

`--sarif` zapisuje na stdout dokument SARIF 2.1.0 i nic więcej, więc można go przekierować tak jak powyżej. Każda włączona reguła jest wymieniona wraz z linkiem do swojej dokumentacji, każde zgłoszenie zawiera wiersz i kolumnę, a przy `--check` plik, który zostałby przeformatowany, jest zgłaszany pod regułą `formatting`.

## pre-commit

djLint może działać jako hook [pre-commit](https://pre-commit.com), zarówno jako linter, jak i formater.

Każdy z tych profili ma hook lintujący, wymieniony poniżej, i hook formatujący o tej samej nazwie z `reformat`: `djlint-reformat-django` dla `djlint-django`. Ustawiają `--profile` i pliki, które przekazuje pre-commit. `angular` nie ma własnych hooków: ustaw dla `djlint` lub `djlint-reformat` `args: [--profile=angular]`.

| Hook                | Profil     | Pliki                                |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | brak       | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Dla szablonów z innymi rozszerzeniami nadpisz w swojej konfiguracji `files`, a także `types_or`, jeśli hook je ustawia, bo pre-commit wymaga dopasowania obu. Zobacz [dokumentację pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

### Domyślny przykład dla Django

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars z rozszerzeniem .html zamiast .hbs

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

Za pomocą parametrów `files` lub `exclude` możesz ograniczyć każdy hook do jego własnego katalogu, co pozwala obsługiwać kilka języków szablonów w jednym repozytorium.

## MegaLinter

[MegaLinter](https://megalinter.io) zawiera djLint. Aby go skonfigurować, uruchom `npx mega-linter-runner --install`, a opcje znajdziesz na [jego stronie o djLint](https://megalinter.io/latest/descriptors/html_djlint/).
