---
description: Propojte djLint se svým oblíbeným editorem. Automaticky formátujte šablony pomocí pre-commit. Lintujte v Sublime Textu.
title: Integrace
keywords: linter šablon, formátovač šablon, djLint, HTML, šablony, formátovač, linter, integrace, jazykový server, lsp, neovim, helix
---

# Integrace

Pro djLint existuje několik integrací do editorů.

Ať používáte jakýkoli editor, nainstalujte djLint tam, kde ho editor najde, ideálně do virtuálního prostředí projektu, a editor spouštějte z něj, nebo ho nasměrujte na `djlint` z tohoto prostředí. Editor pak spouští verzi, kterou má váš projekt zafixovanou, se stejnými výsledky jako váš hook pre-commit nebo CI.

## Visual Studio Code

Nainstalujte [rozšíření djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), nebo pro VSCodium [rozšíření z Open VSX](https://open-vsx.org/extension/monosans/djlint). Najde djLint ve vašem prostředí, jinak použije přibalenou verzi, a pokud ho váš djLint podporuje, používá jazykový server.

Jeho kód je na [GitHubu](https://github.com/djlint/djlint-vscode).

## Neovim

djLint lze v Neovimu používat jako linter i formátovač.

### Vestavěný klient LSP (doporučeno)

Neovim 0.11 nebo novější umí komunikovat s [jazykovým serverem](#jazykovy-server) djLint přímo, bez pluginu. Získáte tak nálezy už během psaní, s podtrženými úseky, a formátování pomocí `vim.lsp.buf.format()`:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Chcete-li formátovat při ukládání, přidejte do stejné konfigurace:

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

Viz [Nastavení](#nastaveni).

### conform.nvim a nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formátuje a [nvim-lint](https://github.com/mfussenegger/nvim-lint) lintuje tak, že djLint spouštějí jako příkaz. Nálezy nemají podtržený úsek a objeví se, jen když nvim-lint požádáte o lintování.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [Repozitář na GitHubu](https://github.com/nvimtools/none-ls.nvim)
- [Lintování](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formátování](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

### efm-langserver

::: content

- [Repozitář na GitHubu](https://github.com/mattn/efm-langserver)

1. Nainstalujte efm-langserver a djLint přes Mason příkazem `:MasonInstall efm djlint`
1. Přidejte `htmldjango` do `filetypes`.
1. Vytvořte konfiguraci formátování:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Propojte jazyk s formátovačem pomocí `htmldjango = { djlint }`.

Ukázková konfigurace:

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

- [Balíček npm](https://www.npmjs.com/package/coc-htmldjango)
  :::

## IDE od JetBrains

V PyCharmu a dalších IDE postavených na IntelliJ použijte bezplatný plugin [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Nainstalujte LSP4IJ z Marketplace.
1. Otevřete nástrojové okno LSP Consoles a přidejte nový jazykový server.
1. Na kartě **Server** nastavte název na `djLint` a příkaz na `djlint --lsp`, a pokud `djlint` z virtuálního prostředí projektu není v PATH, uveďte jeho úplnou cestu.
1. Na kartě **Mappings** přidejte vzor názvů souborů pro vaše šablony, například `*.html`. Pokud konfigurace projektu nemá žádný [profil](/cs/docs/configuration/#profile), nastavte u projektu v Djangu ID jazyka na `htmldjango`, aby se vybral ten správný.
1. Na kartě **Configuration** můžete zadat [nastavení](#nastaveni) jako JSON pod klíčem `djlint`.

Nálezy se zobrazují v editoru a **Reformat Code** může pro namapované soubory používat server.

## Sublime Text

### LSP (doporučeno)

Balíček [LSP](https://packagecontrol.io/packages/LSP) spouští [jazykový server](#jazykovy-server), který poskytuje nálezy už během psaní a formátování.

Spusťte **Preferences: LSP Server Configurations** a přidejte:

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

djLint lze používat jako plugin linteru pro Sublime Text. Nainstalovat ho můžete přes [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Nainstalujte SublimeLinter
3. Nainstalujte SublimeLinter-contrib-djlint
   :::

Ujistěte se, že je djLint nainstalovaný v globálním Pythonu nebo je ve vaší `PATH`.

## Helix

Helix umí spouštět [jazykový server](#jazykovy-server) ze souboru `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, který je součástí Emacsu 29 a novějšího:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Pak v šabloně spusťte `M-x eglot`. Příkaz `eglot-format-buffer` ji naformátuje.

## Jazykový server

`djlint --lsp` spustí djLint jako jazykový server přes stdio. Zůstává spuštěný, takže editor dostává nálezy už během psaní a formátuje dokument, aniž by pokaždé spouštěl nový proces.

Hlásí nálezy a formátuje celé dokumenty. Nepotřebuje žádné další balíčky. Spustit ho stejným příkazem může i jakýkoli jiný editor, který podporuje LSP.

### Nastavení

Server čte [konfiguraci](/cs/docs/configuration/) projektu stejně jako příkazový řádek, od složky každého souboru směrem nahoru. Nastavení z editoru mají před ní přednost, ale stejně jako na příkazovém řádku mohou možnost jen zapnout nebo nastavit hodnotu: `false` nevypne to, co projekt zapíná. Mají názvy [možností příkazového řádku](/cs/docs/configuration/), s podtržítky nebo v camelCase, a pro hodnoty oddělené čárkami lze použít seznamy:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Server si oddíl `djlint` vyžádá přes `workspace/configuration`. Editor, který neumí odpovědět, může stejné klíče poslat v `initializationOptions`.

Dvě nastavení nemají odpovídající možnost příkazového řádku:

- `use_editor_indentation`: Formátovat s velikostí tabulátoru z editoru, a ne podle `indent`.
- `python_rules`: Nastavte na `false`, chcete-li přeskočit vlastní pravidla s `python_module`, čímž zabráníte spuštění kódu projektu.

djLint vezme `profile` z první z těchto možností, která ho obsahuje:

1. Nastavení editoru.
1. Konfigurace projektu.
1. Jazyk dokumentu: `htmldjango` například spustí profil `django`.

Pokud žádná z nich profil nemá, spustí se bez profilu, stejně jako na příkazovém řádku. Nejjednodušší volbou je `profile` v konfiguraci projektu: funguje v každém editoru a není potřeba nastavovat žádné ID jazyka.

### Co dělá

- Nálezy přicházejí po krátké pauze v psaní. Editor s pull diagnostikou si o ně řekne, jakémukoli jinému je server pošle sám.
- `exclude`, `extend_exclude` a `use_gitignore` platí pro otevřené dokumenty. Vyloučený dokument nemá žádné nálezy a neformátuje se.
- Konfiguraci znovu načte, když se změní `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` nebo `.gitignore`, pokud editor umí sledovat soubory, a jinak při otevření nebo uložení dokumentu. Soubory zadané v `configuration` nebo `rules` se znovu načtou při otevření nebo uložení dokumentu. Změna kódu v `python_module` vlastního pravidla vyžaduje restart.
- Pomalé pravidlo zdrží vše, co přijde po něm, protože server dělá vždy jen jednu věc najednou.

## GitHub Actions

Ve workflow GitHub Actions hlásí djLint každý nález jako anotaci, takže se zobrazí přímo v diffu pull requestu. Není potřeba nic konfigurovat: djLint workflow rozpozná a výstup přepne automaticky.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Pomocí `--no-github-output` získáte místo toho běžný výstup do konzole, pomocí `--github-output` vynutíte anotace i mimo Actions.

Anotace patří k jednomu pull requestu. Chcete-li mít nálezy na kartě Security repozitáře, s historií napříč spuštěními, zapište je jako SARIF a soubor nahrajte:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Krok nahrání potřebuje oprávnění `security-events: write` na úrovni jobu nebo workflow.

`--sarif` zapíše na stdout dokument SARIF 2.1.0 a nic jiného, takže ho lze přesměrovat jako výše. Každé zapnuté pravidlo je uvedené s odkazem na svou dokumentaci, každý nález nese svůj řádek a sloupec a s `--check` se soubor, který by se přeformátoval, hlásí pod pravidlem `formatting`. Stejný formát čtou Azure DevOps, GitLab i většina editorů.

## Pre-Commit

djLint lze používat jako hook [pre-commit](https://pre-commit.com), a to jako linter i jako formátovač.

Repozitář poskytuje několik předkonfigurovaných hooků pro konkrétní profily djLint (jen předem nastaví argument `--profile` a řekne pre-commit, jaké přípony souborů má hledat):

::: content

- `djlint` pro lintování a `djlint-reformat` pro formátování
  Hledá soubory odpovídající `*.html` a nenastavuje `--profile`.
- `djlint-django` a `djlint-reformat-django`
  Hledá soubory odpovídající `*.html` a nastaví `--profile=django`.
- `djlint-jinja` a `djlint-reformat-jinja`
  Hledá soubory odpovídající `*.j2`,`*.jinja` nebo `*.jinja2` a nastaví `--profile=jinja`.
- `djlint-nunjucks` a `djlint-reformat-nunjucks`
  Hledá soubory odpovídající `*.njk` a nastaví `--profile=nunjucks`.
- `djlint-handlebars` a `djlint-reformat-handlebars`
  Hledá soubory odpovídající `*.hbs` a nastaví `--profile=handlebars`.
- `djlint-liquid` a `djlint-reformat-liquid`
  Hledá soubory odpovídající `*.html` a nastaví `--profile=liquid`.
- `djlint-golang` a `djlint-reformat-golang`
  Hledá soubory odpovídající `*.gotmpl` a nastaví `--profile=golang`.
- `djlint-tera` a `djlint-reformat-tera`
  Hledá soubory odpovídající `*.html` a nastaví `--profile=tera`.
- `djlint-askama` a `djlint-reformat-askama`
  Hledá soubory odpovídající `*.html` a nastaví `--profile=askama`.
  :::

Tyto předdefinované hooky jsou někdy příliš konzervativní v tom, jaké vstupy přijímají (vaše šablony mohou používat jinou příponu), a proto vám pre-commit výslovně umožňuje kteroukoli z těchto předdefinovaných možností přepsat. Další konfiguraci popisuje [dokumentace pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

### Výchozí příklad pro Django

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars s příponou .html místo .hbs

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

Pomocí parametrů `files` nebo `exclude` můžete každý hook omezit na jeho vlastní adresář, a podporovat tak v jednom repozitáři více šablonovacích jazyků.

## MegaLinter

djlint je nativně zabudovaný mezi více než 100 linterů [MegaLinteru](https://megalinter.io)

Chcete-li ho nainstalovat, stačí spustit `npx mega-linter-runner --install` a postupovat podle pokynů

::: content

- [Repozitář na GitHubu](https://github.com/oxsecurity/megalinter)
- [djlint v dokumentaci MegaLinteru](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
