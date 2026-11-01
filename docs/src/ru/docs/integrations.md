---
description: Интегрируйте djLint с вашим любимым редактором. Автоматическое форматирование ваших шаблонов с помощью Pre-Commit или Visual Studio Code. Lint с SublimeText.
title: Интеграции
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, integrations, языковой сервер, lsp, neovim, zed, helix
---

# {{ "integrations" | i18n }}

Существует несколько интеграций редакторов для djLint.

В любом редакторе установите djLint туда, где редактор его найдёт, лучше всего в виртуальное окружение проекта, и запускайте редактор из него или укажите ему путь к `djlint` этого окружения. Тогда редактор будет использовать версию, закреплённую в проекте, и результаты совпадут с хуком pre-commit и CI.

## Visual Studio Code

Установите [расширение djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) или [его версию из Open VSX](https://open-vsx.org/extension/monosans/djlint) для VSCodium. Оно находит djLint в вашем окружении, использует встроенный, если djLint не установлен, и работает через языковой сервер, когда ваш djLint его поддерживает.

Его код находится на [GitHub](https://github.com/djlint/djlint-vscode).

## Zed

Установите [расширение djLint](https://github.com/djlint/djlint-zed), которое запускает [языковой сервер](#yazykovoj-server). Находки появляются в HTML и в языках расширений для шаблонов сразу после установки.

Чтобы форматировать с помощью djLint, сделайте его форматером языка:

```json
{
  "languages": {
    "HTML": { "formatter": { "language_server": { "name": "djlint" } } }
  }
}
```

[Настройки](#nastrojki) задаются в `lsp.djlint.settings`.

## Neovim

djLint можно использовать как линтер и форматер в Neovim.

### Встроенный клиент LSP (рекомендуется)

Neovim 0.11 и новее умеет работать с [языковым сервером](#yazykovoj-server) djLint напрямую, без плагинов. Это даёт находки при вводе с подчёркнутыми диапазонами и форматирование через `vim.lsp.buf.format()`:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Чтобы форматировать при сохранении, добавьте в ту же конфигурацию:

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

См. [настройки](#nastrojki).

### conform.nvim и nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) форматирует, а [nvim-lint](https://github.com/mfussenegger/nvim-lint) проверяет, запуская djLint как команду. Находки приходят без подчёркнутых диапазонов и только тогда, когда вы просите nvim-lint проверить файл.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [GitHub репозиторий](https://github.com/nvimtools/none-ls.nvim)
- [Линтинг](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Форматирование](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

### efm-langserver

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

### coc.nvim

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::

## IDE от JetBrains

В PyCharm и других IDE на базе IntelliJ используйте бесплатный плагин [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Установите LSP4IJ из Marketplace.
1. Откройте панель LSP Consoles и добавьте новый языковой сервер.
1. На вкладке **Server** укажите имя `djLint` и команду `djlint --lsp`, с полным путём к `djlint` из виртуального окружения проекта, если его нет в PATH.
1. На вкладке **Mappings** добавьте шаблон имён файлов, например `*.html`. Для проекта на Django укажите идентификатор языка `htmldjango`, чтобы выбрался нужный [профиль](/ru/docs/configuration/#profile).
1. На вкладке **Configuration** можно задать [настройки](#nastrojki) в JSON, в ключе `djlint`.

Находки появятся в редакторе, а **Reformat Code** сможет использовать сервер для этих файлов.

## Sublime Text

### LSP (рекомендуется)

Пакет [LSP](https://packagecontrol.io/packages/LSP) запускает [языковой сервер](#yazykovoj-server), который даёт находки при вводе и форматирование.

Выполните **Preferences: LSP Server Configurations** и добавьте:

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

djLint можно использовать в качестве плагина SublimeText Linter. Его можно установить через [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Install SublimeLinter
3. Install SublimeLinter-contrib-djlint
   :::

Убедитесь, что djLint установлен в вашем глобальном python или в вашем `PATH`.

## Helix

Helix запускает [языковой сервер](#yazykovoj-server) из `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, входящий в Emacs 29 и новее:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Затем выполните `M-x eglot` в шаблоне. `eglot-format-buffer` отформатирует его.

## Языковой сервер

`djlint --lsp` запускает djLint как языковой сервер через stdio. Он продолжает работать, поэтому редактор получает находки при вводе и форматирует документ, не запуская каждый раз новый процесс.

Сервер сообщает о находках и форматирует документы целиком. Дополнительные пакеты ему не нужны. Любой другой редактор с поддержкой LSP может запустить его той же командой.

### Настройки

Сервер читает [конфигурацию](/ru/docs/configuration/) проекта так же, как командная строка: от папки каждого файла вверх. Настройки редактора важнее неё, но, как и в командной строке, они могут только включить опцию или задать значение: `false` не выключит то, что включил проект. Их имена совпадают с [опциями командной строки](/ru/docs/configuration/), с подчёркиваниями или в camelCase, а значения через запятую можно задавать списками:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Сервер запрашивает раздел `djlint` через `workspace/configuration`. Редактор, который не умеет на это отвечать, может передать те же ключи в `initializationOptions`.

У двух настроек нет опции командной строки:

- `use_editor_indentation`: форматировать с размером табуляции редактора, а не с `indent`.
- `python_rules`: значение `false` пропускает пользовательские правила с `python_module`, чтобы код проекта не выполнялся.

Если `profile` не задан ни там, ни там, его выбирает язык документа: например, для `htmldjango` это профиль `django`.

### Как это работает

- Находки приходят после короткой паузы в наборе. Редактор с pull-диагностикой запрашивает их сам, остальным сервер отправляет их сам.
- `exclude`, `extend_exclude` и `use_gitignore` действуют на открытые документы. У исключённого документа нет находок, и он не форматируется.
- Сервер перечитывает конфигурацию при изменении `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` или `.gitignore`, если редактор умеет следить за файлами, а иначе при открытии или сохранении документа. Файлы из `configuration` и `rules` перечитываются при открытии или сохранении документа. После изменения кода `python_module` пользовательского правила нужен перезапуск.
- Медленное правило задерживает всё, что идёт за ним, потому что сервер делает всё по очереди.

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

## MegaLinter

djLint встроен в [MegaLinter](https://megalinter.io) вместе с более чем сотней других линтеров.

Чтобы установить его, запустите `npx mega-linter-runner --install` и следуйте инструкциям.

::: content

- [GitHub репозиторий](https://github.com/oxsecurity/megalinter)
- [djlint в документации MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
