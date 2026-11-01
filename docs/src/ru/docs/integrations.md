---
description: Интегрируйте djLint с вашим любимым редактором. Автоматическое форматирование ваших шаблонов с помощью Pre-Commit или Visual Studio Code. Lint с SublimeText.
title: Интеграции
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, integrations
---

# {{ "integrations" | i18n }}

Существует несколько интеграций редакторов для djLint.

## GitHub Actions

В workflow GitHub Actions djLint выводит каждую находку как аннотацию, поэтому она видна прямо в диффе пул-реквеста. Настраивать ничего не нужно: djLint сам определяет workflow и переключает вывод.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

`--no-github-output` возвращает обычный консольный вывод, а `--github-output` включает аннотации за пределами Actions.

Аннотации привязаны к одному пул-реквесту. Чтобы хранить находки во вкладке Security репозитория вместе с историей по запускам, запишите их в формате SARIF и загрузите файл:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Для загрузки у задачи или всего workflow должно быть разрешение `security-events: write`.

`--sarif` выводит в stdout документ SARIF 2.1.0 и больше ничего, поэтому вывод можно перенаправить в файл, как выше. В нём перечислены все включённые правила со ссылками на их документацию, у каждой находки указаны строка и столбец, а с `--check` файл, который был бы переформатирован, попадает в отчёт под правилом `formatting`. Тот же формат читают Azure DevOps, GitLab и большинство редакторов.

## Pre-Commit

djLint можно использовать как [pre-commit](https://pre-commit.com) хук в качестве как линтера, так и форматировщика.

Репозиторий предоставляет несколько предварительно настроенных хуков для определенных профилей djLint (он просто задает аргумент `--profile` и указывает pre-commit, какие расширения файлов искать):

::: content

- `djlint` для линтинга и `djlint-reformat` для форматирования
  Будет искать файлы, соответствующие `*.html`, без установки `--profile`.
- `djlint-django` и `djlint-reformat-django`
  Будет искать файлы, соответствующие `*.html`, и устанавливать `--profile=django`.
- `djlint-jinja` и `djlint-reformat-jinja`
  Будет искать файлы, соответствующие `*.j2`, `*.jinja` или `*.jinja2`, и устанавливать `--profile=jinja`.
- `djlint-nunjucks` и `djlint-reformat-nunjucks`
  Будет искать файлы, соответствующие `*.njk`, и устанавливать `--profile=nunjucks`.
- `djlint-handlebars` и `djlint-reformat-handlebars`
  Будет искать файлы, соответствующие `*.hbs`, и устанавливать `--profile=handlebars`.
- `djlint-liquid` и `djlint-reformat-liquid`
  Будет искать файлы, соответствующие `*.html`, и устанавливать `--profile=liquid`.
- `djlint-golang` и `djlint-reformat-golang`
  Будет искать файлы, соответствующие `*.gotmpl`, и устанавливать `--profile=golang`.
- `djlint-tera` и `djlint-reformat-tera`
  Будет искать файлы, соответствующие `*.html`, и устанавливать `--profile=tera`.
- `djlint-askama` и `djlint-reformat-askama`
  Будет искать файлы, соответствующие `*.html`, и устанавливать `--profile=askama`.
  :::

Обратите внимание, что эти предопределенные хуки иногда слишком консервативны в принимаемых ими входных данных (ваши шаблоны могут использовать другое расширение), поэтому pre-commit явно позволяет вам переопределять любые из этих предопределенных опций. См. [pre-commit документы](https://pre-commit.com/#pre-commit-configyaml---hooks) для дополнительной настройки.

### Пример Django по умолчанию

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars с расширением .html вместо .hbs

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

Вы можете использовать параметры `files` или `exclude`, чтобы ограничить каждый хук своим каталогом, что позволит вам поддерживать несколько языков шаблонов в одном репозитории.

## SublimeText Linter

djLint можно использовать в качестве плагина SublimeText Linter. Его можно установить через [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Install SublimeLinter
3. Install SublimeLinter-contrib-djlint
   :::

Убедитесь, что djLint установлен в вашем глобальном python или в вашем `PATH`.

## Visual Studio Code

::: content

- [GitHub репозиторий](https://github.com/djlint/djlint-vscode)
- [Страница на VS Marketplace](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
- [Страница на Open VSX](https://open-vsx.org/extension/monosans/djlint)
  :::

## neovim

djLint можно использовать как линтер и форматер в neovim.

Neovim 0.11 и новее умеет работать с [языковым сервером](/ru/docs/language-server/) djLint напрямую, без плагинов. Это даёт находки при вводе с подчёркнутыми диапазонами и форматирование через `vim.lsp.buf.format()`:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Настройки описаны на странице [Языковой сервер](/ru/docs/language-server/#nastrojki). Плагины ниже запускают djLint как обычную команду.

С помощью плагина `none-ls`.

::: content

- [GitHub репозиторий](https://github.com/nvimtools/none-ls.nvim)
- [Линтинг](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Форматирование](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

С помощью `coc.nvim`.

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::

С помощью `efm-langserver`.

::: content

- [GitHub репозиторий](https://github.com/mattn/efm-langserver)

1. Установите efm-langserver и djLint через Mason: `:MasonInstall efm djlint`
1. Добавьте `htmldjango` в `filetypes`.
1. Создайте конфигурацию форматирования:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Свяжите язык с форматировщиком через `htmldjango = { djlint }`.

Пример конфигурации:

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

## Zed

Установите [расширение djLint](https://github.com/djlint/zed-djlint), которое запускает [языковой сервер](/ru/docs/language-server/).

## Helix

Helix запускает [языковой сервер](/ru/docs/language-server/) из `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["vscode-html-language-server", "djlint"]
```

## IDE от JetBrains, Sublime Text и Emacs

Они тоже работают через [языковой сервер](/ru/docs/language-server/). Как настроить [IDE от JetBrains](/ru/docs/language-server/#ide-ot-jetbrains), [Sublime Text](/ru/docs/language-server/#sublime-text) и [Emacs](/ru/docs/language-server/#emacs).

## MegaLinter

djLint встроен в [MegaLinter](https://megalinter.io) вместе с более чем сотней других линтеров.

Чтобы установить его, запустите `npx mega-linter-runner --install` и следуйте инструкциям.

::: content

- [GitHub репозиторий](https://github.com/oxsecurity/megalinter)
- [djlint в документации MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
