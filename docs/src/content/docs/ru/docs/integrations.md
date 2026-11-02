---
title: "Интеграции"
description: "Интегрируйте djLint в свой любимый редактор. Автоматически форматируйте шаблоны с помощью Pre-Commit. Проверяйте их в SublimeText."
sidebar:
  label: "Интеграции"
---

Для djLint существует несколько интеграций с редакторами.

Какой бы редактор вы ни использовали, установите djLint туда, где редактор сможет его найти, лучше всего в виртуальное окружение проекта, и запускайте редактор из этого окружения или укажите ему `djlint` из него. Тогда редактор будет запускать версию, зафиксированную в проекте, и результаты совпадут с результатами хука pre-commit или CI.

## Visual Studio Code

Установите [расширение djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) или, для VSCodium, [его версию в Open VSX](https://open-vsx.org/extension/monosans/djlint). Оно находит djLint в вашем окружении, а если не находит, использует встроенный, и работает через языковой сервер, если ваша версия djLint его поддерживает.

Его код находится на [GitHub](https://github.com/djlint/djlint-vscode).

## Neovim

В Neovim djLint можно использовать как линтер и как форматер.

### Встроенный LSP-клиент (рекомендуется)

Neovim 0.11 и новее может работать с [языковым сервером](#языковой-сервер) djLint напрямую, без плагинов. Так замечания появляются прямо во время набора, с подчёркиванием проблемных фрагментов, а форматирование выполняет `vim.lsp.buf.format()`:

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

См. раздел [Настройки](#настройки).

### conform.nvim и nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) форматирует, а [nvim-lint](https://github.com/mfussenegger/nvim-lint) проверяет код, запуская djLint как команду. Замечания приходят без подчёркивания фрагментов и только тогда, когда вы запускаете проверку в nvim-lint.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [Репозиторий на GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Проверка](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Форматирование](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [Репозиторий на GitHub](https://github.com/mattn/efm-langserver)

1. Установите efm-langserver и djLint через Mason командой `:MasonInstall efm djlint`
1. Добавьте `htmldjango` в `filetypes`.
1. Создайте конфигурацию форматирования:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Свяжите язык с форматером: `htmldjango = { djlint }`.

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

### coc.nvim

- [Пакет npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE от JetBrains

В PyCharm и других IDE на базе IntelliJ используйте бесплатный плагин [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Установите LSP4IJ из Marketplace.
1. Откройте окно инструментов LSP Consoles и добавьте новый языковой сервер.
1. На вкладке **Server** укажите имя `djLint` и команду `djlint --lsp`, с полным путём к `djlint` в виртуальном окружении проекта, если его нет в PATH.
1. На вкладке **Mappings** добавьте маску имён файлов ваших шаблонов, например `*.html`. Если в конфигурации проекта не задан [профиль](/ru/docs/configuration/#profile), для проекта на Django укажите идентификатор языка `htmldjango`, чтобы был выбран нужный профиль.
1. На вкладке **Configuration** можно задать [настройки](#настройки) в формате JSON, в ключе `djlint`.

Замечания появляются в редакторе, а **Reformat Code** может использовать сервер для сопоставленных файлов.

## Sublime Text

### LSP (рекомендуется)

Пакет [LSP](https://packagecontrol.io/packages/LSP) запускает [языковой сервер](#языковой-сервер), который показывает замечания во время набора и форматирует код.

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

djLint можно использовать как плагин линтера для SublimeText. Его можно установить через [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. Установите SublimeLinter
3. Установите SublimeLinter-contrib-djlint

Убедитесь, что djLint установлен в глобальный Python или доступен в `PATH`.

## Helix

Helix может запускать [языковой сервер](#языковой-сервер), настроенный в `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, входящий в состав Emacs 29 и новее:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Затем выполните `M-x eglot` в шаблоне. `eglot-format-buffer` отформатирует его.

## Языковой сервер

`djlint --lsp` запускает djLint как языковой сервер, работающий через stdio. Сервер продолжает работать, поэтому редактор получает замечания во время набора и форматирует документ, не запуская каждый раз новый процесс.

Сервер сообщает о замечаниях и форматирует документы целиком. Дополнительные пакеты ему не нужны. Любой другой редактор с поддержкой LSP может запустить его той же командой.

### Настройки

Сервер читает [конфигурацию](/ru/docs/configuration/) проекта так же, как командная строка: от папки каждого файла вверх. Настройки из редактора важнее неё, но, как и в командной строке, они могут только включить параметр или задать значение: `false` не отключит то, что включено в проекте. Их имена совпадают с именами [параметров командной строки](/ru/docs/configuration/), с подчёркиваниями или в camelCase, а вместо значений через запятую можно передавать списки:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Сервер запрашивает раздел `djlint` через `workspace/configuration`. Редактор, который не умеет на это отвечать, может передать те же ключи в `initializationOptions`.

У двух настроек нет соответствующего параметра командной строки:

- `use_editor_indentation`: форматировать с размером табуляции из редактора, а не с `indent`.
- `python_rules`: установите `false`, чтобы пропускать пользовательские правила с `python_module`; так код проекта не будет запускаться.

djLint берёт `profile` из первого источника, где он задан:

1. Настройки редактора.
1. Конфигурация проекта.
1. Язык документа: например, для `htmldjango` используется профиль `django`.

Если профиль нигде не задан, djLint работает без профиля, как и в командной строке. Проще всего задать `profile` в конфигурации проекта: это работает в любом редакторе, и не нужно настраивать идентификатор языка.

### Как работает сервер

- Замечания появляются после короткой паузы в наборе. Редактор, поддерживающий pull-диагностику, запрашивает их сам, а любому другому сервер присылает их.
- `exclude`, `extend_exclude` и `use_gitignore` действуют и на открытые документы. У исключённого документа нет замечаний, и он не форматируется.
- Сервер перечитывает конфигурацию при изменении `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` или `.gitignore`, если редактор умеет отслеживать файлы, а иначе — при открытии или сохранении документа. Файлы, указанные в `configuration` или `rules`, перечитываются при открытии или сохранении документа. После изменения кода в `python_module` пользовательского правила нужен перезапуск.
- Медленное правило задерживает всё, что идёт после него, потому что сервер выполняет задачи по одной.

## GitHub Actions

В рабочем процессе GitHub Actions djLint выводит каждое замечание как аннотацию, поэтому оно отображается прямо среди изменений пул-реквеста. Настраивать ничего не нужно: djLint сам распознаёт рабочий процесс и переключает формат вывода.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Чтобы вместо этого получить обычный консольный вывод, используйте `--no-github-output`, а чтобы принудительно выводить аннотации вне Actions — `--github-output`.

Аннотации относятся к одному пул-реквесту. Чтобы хранить замечания на вкладке Security репозитория, с историей по всем запускам, запишите их в формате SARIF и загрузите файл:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Шагу загрузки нужно разрешение `security-events: write` на уровне задания или рабочего процесса.

`--sarif` выводит в stdout документ SARIF 2.1.0 и больше ничего, поэтому вывод можно перенаправить, как показано выше. Каждое включённое правило перечисляется со ссылкой на свою документацию, у каждого замечания указаны строка и столбец, а с `--check` файл, который был бы переформатирован, попадает в отчёт под правилом `formatting`. Тот же формат читают Azure DevOps, GitLab и большинство редакторов.

## Pre-Commit

djLint можно использовать как хук [pre-commit](https://pre-commit.com) — и как линтер, и как форматер.

В репозитории есть несколько готовых хуков для отдельных профилей djLint (они лишь заранее задают аргумент `--profile` и сообщают pre-commit, файлы с какими расширениями искать):

- `djlint` для проверки и `djlint-reformat` для форматирования
  Ищут файлы по маске `*.html`, не задавая `--profile`.
- `djlint-django` и `djlint-reformat-django`
  Ищут файлы по маске `*.html` и задают `--profile=django`.
- `djlint-jinja` и `djlint-reformat-jinja`
  Ищут файлы по маскам `*.j2`,`*.jinja` или `*.jinja2` и задают `--profile=jinja`.
- `djlint-nunjucks` и `djlint-reformat-nunjucks`
  Ищут файлы по маске `*.njk` и задают `--profile=nunjucks`.
- `djlint-handlebars` и `djlint-reformat-handlebars`
  Ищут файлы по маске `*.hbs` и задают `--profile=handlebars`.
- `djlint-liquid` и `djlint-reformat-liquid`
  Ищут файлы по маске `*.html` и задают `--profile=liquid`.
- `djlint-golang` и `djlint-reformat-golang`
  Ищут файлы по маске `*.gotmpl` и задают `--profile=golang`.
- `djlint-tera` и `djlint-reformat-tera`
  Ищут файлы по маске `*.html` и задают `--profile=tera`.
- `djlint-askama` и `djlint-reformat-askama`
  Ищут файлы по маске `*.html` и задают `--profile=askama`.

Учтите, что эти готовые хуки иногда слишком строги к тому, какие файлы принимают (у ваших шаблонов может быть другое расширение), поэтому pre-commit явно позволяет переопределить любые из этих заранее заданных параметров. Подробнее о настройке см. в [документации pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

### Стандартный пример для Django

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

С помощью параметров `files` или `exclude` можно ограничить каждый хук своим каталогом и так поддерживать несколько языков шаблонов в одном репозитории.

## MegaLinter

djlint входит в число более чем 100 линтеров, встроенных в [MegaLinter](https://megalinter.io)

Чтобы установить его, просто выполните `npx mega-linter-runner --install` и следуйте инструкциям

- [Репозиторий на GitHub](https://github.com/oxsecurity/megalinter)
- [djlint в документации MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
