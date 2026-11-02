---
title: "Integracje"
description: "Zintegruj djLint ze swoim ulubionym edytorem. Automatycznie formatuj szablony za pomocą Pre-Commit. Lintuj w SublimeText."
sidebar:
  label: "Integracje"
---

Dla djLint powstało kilka integracji z edytorami.

Niezależnie od edytora zainstaluj djLint tam, gdzie edytor może go znaleźć, najlepiej w środowisku wirtualnym projektu, a następnie uruchamiaj edytor z tego środowiska albo wskaż mu `djlint` z tego środowiska. Dzięki temu edytor uruchamia wersję przypiętą w projekcie i daje takie same wyniki jak hook pre-commit czy CI.

## Visual Studio Code

Zainstaluj [rozszerzenie djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) lub, w przypadku VSCodium, [jego wersję z Open VSX](https://open-vsx.org/extension/monosans/djlint). Rozszerzenie znajduje djLint w twoim środowisku, a gdy go tam nie ma, korzysta z dołączonej wersji; jeśli twój djLint ma serwer języka, rozszerzenie go używa.

Jego kod jest dostępny na [GitHubie](https://github.com/djlint/djlint-vscode).

## Neovim

W Neovimie djLint może służyć jako linter i formater.

### Wbudowany klient LSP (zalecany)

Neovim 0.11 lub nowszy może komunikować się z [serwerem języka](#serwer-języka) djLint bezpośrednio, bez żadnej wtyczki. Daje to zgłoszenia już podczas pisania, z podkreślonymi zakresami, oraz formatowanie przez `vim.lsp.buf.format()`:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Aby formatować przy zapisie, dodaj do tej samej konfiguracji:

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

Zobacz [Ustawienia](#ustawienia).

### conform.nvim i nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatuje, a [nvim-lint](https://github.com/mfussenegger/nvim-lint) lintuje, uruchamiając djLint jako polecenie. Zgłoszenia nie mają podkreślonego zakresu i pojawiają się dopiero wtedy, gdy poprosisz nvim-lint o lintowanie.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [Repozytorium na GitHubie](https://github.com/nvimtools/none-ls.nvim)
- [Lintowanie](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatowanie](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [Repozytorium na GitHubie](https://github.com/mattn/efm-langserver)

1. Zainstaluj efm-langserver i djLint za pomocą Masona poleceniem `:MasonInstall efm djlint`
1. Dodaj `htmldjango` do `filetypes`.
1. Utwórz konfigurację formatowania:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Połącz język z formaterem za pomocą `htmldjango = { djlint }`.

Przykładowa konfiguracja:

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

- [Pakiet npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

W PyCharmie i innych IDE opartych na IntelliJ użyj darmowej wtyczki [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Zainstaluj LSP4IJ z Marketplace.
1. Otwórz okno narzędziowe LSP Consoles i dodaj nowy serwer języka.
1. Na karcie **Server** ustaw nazwę `djLint` i polecenie `djlint --lsp`, z pełną ścieżką do `djlint` ze środowiska wirtualnego projektu, jeśli nie ma go w PATH.
1. Na karcie **Mappings** dodaj wzorzec nazw plików dla swoich szablonów, na przykład `*.html`. Jeśli konfiguracja projektu nie zawiera [profilu](/pl/docs/configuration/#profile), w projekcie Django ustaw identyfikator języka `htmldjango`, aby został wybrany właściwy profil.
1. Na karcie **Configuration** możesz podać [ustawienia](#ustawienia) w formacie JSON, pod kluczem `djlint`.

Zgłoszenia pojawiają się w edytorze, a **Reformat Code** może używać serwera dla zmapowanych plików.

## Sublime Text

### LSP (zalecany)

Pakiet [LSP](https://packagecontrol.io/packages/LSP) uruchamia [serwer języka](#serwer-języka), który zapewnia zgłoszenia podczas pisania oraz formatowanie.

Uruchom **Preferences: LSP Server Configurations** i dodaj:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint może działać jako wtyczka lintera SublimeText. Można ją zainstalować przez [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. Zainstaluj SublimeLinter
3. Zainstaluj SublimeLinter-contrib-djlint

Upewnij się, że djLint jest zainstalowany w globalnym Pythonie lub dostępny w `PATH`.

## Helix

Helix może uruchamiać [serwer języka](#serwer-języka) skonfigurowany w `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, dostarczany z Emacsem 29 i nowszymi:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Następnie uruchom `M-x eglot` w szablonie. `eglot-format-buffer` go sformatuje.

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

`--sarif` zapisuje na stdout dokument SARIF 2.1.0 i nic więcej, więc można go przekierować tak jak powyżej. Każda włączona reguła jest wymieniona wraz z linkiem do swojej dokumentacji, każde zgłoszenie zawiera wiersz i kolumnę, a przy `--check` plik, który zostałby przeformatowany, jest zgłaszany pod regułą `formatting`. Ten sam format odczytują Azure DevOps, GitLab i większość edytorów.

## Pre-Commit

djLint może działać jako hook [pre-commit](https://pre-commit.com), zarówno jako linter, jak i formater.

Repozytorium udostępnia kilka wstępnie skonfigurowanych hooków dla konkretnych profili djLint (ustawiają one jedynie argument `--profile` i informują pre-commit, jakich rozszerzeń plików ma szukać):

- `djlint` do lintowania i `djlint-reformat` do formatowania
  Szukają plików pasujących do `*.html` bez ustawiania `--profile`.
- `djlint-django` i `djlint-reformat-django`
  Szukają plików pasujących do `*.html` i ustawiają `--profile=django`.
- `djlint-jinja` i `djlint-reformat-jinja`
  Szukają plików pasujących do `*.j2`,`*.jinja` lub `*.jinja2` i ustawiają `--profile=jinja`.
- `djlint-nunjucks` i `djlint-reformat-nunjucks`
  Szukają plików pasujących do `*.njk` i ustawiają `--profile=nunjucks`.
- `djlint-handlebars` i `djlint-reformat-handlebars`
  Szukają plików pasujących do `*.hbs` i ustawiają `--profile=handlebars`.
- `djlint-liquid` i `djlint-reformat-liquid`
  Szukają plików pasujących do `*.html` i ustawiają `--profile=liquid`.
- `djlint-golang` i `djlint-reformat-golang`
  Szukają plików pasujących do `*.gotmpl` i ustawiają `--profile=golang`.
- `djlint-tera` i `djlint-reformat-tera`
  Szukają plików pasujących do `*.html` i ustawiają `--profile=tera`.
- `djlint-askama` i `djlint-reformat-askama`
  Szukają plików pasujących do `*.html` i ustawiają `--profile=askama`.

Pamiętaj, że te predefiniowane hooki bywają zbyt zachowawcze w kwestii akceptowanych plików wejściowych (twoje szablony mogą mieć inne rozszerzenie), dlatego pre-commit wprost pozwala nadpisać każdą z tych predefiniowanych opcji. Więcej o konfiguracji przeczytasz w [dokumentacji pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

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

djlint jest natywnie wbudowany w [MegaLinter](https://megalinter.io), wśród ponad 100 linterów

Aby go zainstalować, po prostu uruchom `npx mega-linter-runner --install` i postępuj zgodnie z instrukcjami

- [Repozytorium na GitHubie](https://github.com/oxsecurity/megalinter)
- [djlint w dokumentacji MegaLintera](https://megalinter.io/latest/descriptors/html_djlint/)
