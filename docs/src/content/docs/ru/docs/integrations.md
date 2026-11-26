---
title: "Интеграции"
description: "Используйте djLint в своём редакторе и запускайте его через pre-commit."
---

Какой бы редактор вы ни использовали, установите djLint туда, где редактор сможет его найти, лучше всего в виртуальное окружение проекта, и запускайте редактор из этого окружения или укажите ему `djlint` из него. Тогда редактор будет запускать версию, зафиксированную в проекте, и результаты совпадут с результатами хука pre-commit или CI.

Если djLint в проекте установлен через [npm](/ru/docs/getting-started/#ustanovka), его команда лежит в проекте: `node_modules/.bin/djlint`, а на Windows `node_modules\.bin\djlint.cmd`. Там, где редактор ниже запускает `djlint`, укажите ему этот путь. Расширения для VS Code и Zed находят его сами.

## Visual Studio Code

Установите [расширение djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) из Visual Studio Marketplace. Cursor, Windsurf, VSCodium и другие редакторы на основе VS Code ставят [то же расширение из Open VSX](https://open-vsx.org/extension/monosans/djlint). Оно ищет djLint в вашем окружении и, если не находит, использует встроенный. Если ваша версия djLint поддерживает языковой сервер, расширение работает через него.

В его [README](https://github.com/djlint/djlint-vscode#readme) описаны настройки расширения и то, какой djLint оно запускает.

## Zed

[Расширение djLint](https://github.com/djlint/djlint-zed) запускает [языковой сервер](#yazykovoj-server) в HTML и в языках шаблонных расширений, например Django, Jinja и Twig. В реестре расширений Zed его пока нет, поэтому установите его как dev-расширение:

1. Установите Rust через [rustup](https://rustup.rs): Zed собирает им расширение и сам добавляет таргет `wasm32-wasip2`. Если Rust установлен иначе, например через Homebrew или Nix, добавьте таргет сами.
1. Склонируйте расширение:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. Откройте в Zed палитру команд (`cmd-shift-p` на macOS, `ctrl-shift-p` в остальных системах), выполните **zed: install dev extension** и выберите склонированную папку `djlint-zed`.

Чтобы обновить расширение, выполните в этой папке `git pull`, а затем **zed: rebuild dev extension**.

Нужен djLint 1.49 или новее в PATH или установленный в проекте через npm, либо [uv](https://docs.astral.sh/uv/), который запускает djLint без установки. В [README](https://github.com/djlint/djlint-zed#readme) расширения описано, как назначить его форматером языка, и перечислены его настройки.

## Neovim

Некоторым расширениям шаблонов Neovim не назначает filetype. Какой бы вариант ниже вы ни выбрали, сначала зарегистрируйте их:

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Встроенный LSP-клиент (рекомендуется)

Neovim 0.11 и новее может работать с [языковым сервером](#yazykovoj-server) djLint напрямую, без плагинов. Так замечания появляются прямо во время набора, с подчёркиванием проблемных фрагментов, а форматирование выполняет `vim.lsp.buf.format()`.

В [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) новее v2.12.0 его конфигурация уже есть, так что с ним хватит одной строки:

```lua
vim.lsp.enable("djlint")
```

Если djLint стоит в проекте через npm, поставьте перед этой строкой `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })`, на Windows с путём `"node_modules/.bin/djlint.cmd"`.

Без nvim-lspconfig или с его старой версией задайте конфигурацию сами:

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

Чтобы форматировать при сохранении, добавьте в ту же конфигурацию:

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

См. раздел [Настройки](#nastrojki).

### conform.nvim и nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) форматирует, а [nvim-lint](https://github.com/mfussenegger/nvim-lint) проверяет код, запуская djLint как команду. Замечания приходят без подчёркивания фрагментов и только тогда, когда вы запускаете проверку в nvim-lint. Профиль берётся из [конфигурации](/ru/docs/configuration/#profile) проекта, как в командной строке. Этому примеру нужен djLint 1.49 или новее.

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

- [Репозиторий на GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Проверка](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Форматирование](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [Пакет npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE от JetBrains

В PyCharm и других IDE на базе IntelliJ используйте бесплатный плагин [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Установите LSP4IJ из Marketplace.
1. Откройте окно инструментов LSP Consoles и добавьте новый языковой сервер.
1. На вкладке **Server** укажите имя `djLint` и команду `djlint --lsp`, с полным путём к `djlint` в виртуальном окружении проекта, если его нет в PATH.
1. На вкладке **Mappings** добавьте маски имён файлов ваших шаблонов. Если в конфигурации проекта не задан [профиль](/ru/docs/configuration/#profile), его выбирает идентификатор языка у маски:

   | Маски                                 | Идентификатор языка           |
   | ------------------------------------- | ----------------------------- |
   | `*.html`, `*.htm`                     | `html`, в Django `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                       |
   | `*.njk`, `*.twig`                     | `nunjucks`                    |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                  |
   | `*.liquid`                            | `liquid`                      |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                      |
   | `*.tera`                              | `tera`                        |
   | `*.mako`                              | `mako`                        |

1. На вкладке **Configuration** можно задать [настройки](#nastrojki) в формате JSON, в ключе `djlint`.

Замечания появляются в редакторе, а **Reformat Code** может использовать сервер для сопоставленных файлов.

## Sublime Text

### LSP (рекомендуется)

Пакет [LSP](https://packagecontrol.io/packages/LSP) запускает [языковой сервер](#yazykovoj-server), который показывает замечания во время набора и форматирует код.

Выполните **Preferences: LSP Server Configurations** и добавьте:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Установите через Package Control SublimeLinter и [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint). djLint должен быть в PATH, который видит Sublime Text.

## Helix

Helix может запускать [языковой сервер](#yazykovoj-server), настроенный в `languages.toml`. Список `language-servers` заменяет тот, что есть у Helix для этого языка, поэтому оставьте после `djlint` его собственные серверы:

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

Сам Helix не открывает ни один файл как `htmldjango`. В проекте на Django добавьте `file-types = ["html"]` к этой записи в `.helix/languages.toml` проекта.

## Emacs

Eglot, входящий в состав Emacs 29 и новее:

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Затем выполните `M-x eglot` в шаблоне. `eglot-format-buffer` отформатирует его. `html-mode`, `mhtml-mode` и `web-mode` не называют язык шаблонов, поэтому в них профиль берётся из [конфигурации](/ru/docs/configuration/#profile) проекта.

## Языковой сервер

`djlint --lsp` запускает djLint как языковой сервер, работающий через stdio. Сервер работает постоянно, поэтому редактор получает замечания во время набора и форматирует документ, не запуская каждый раз новый процесс.

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

`--sarif` выводит в stdout документ SARIF 2.1.0 и больше ничего, поэтому вывод можно перенаправить, как показано выше. Каждое включённое правило перечисляется со ссылкой на свою документацию, у каждого замечания указаны строка и столбец, а с `--check` файл, который был бы переформатирован, попадает в отчёт под правилом `formatting`.

## pre-commit

djLint можно использовать как хук [pre-commit](https://pre-commit.com) и для проверки, и для форматирования.

У каждого из этих профилей есть хук для проверки (хуки перечислены ниже) и хук для форматирования с тем же именем, но с `reformat`: `djlint-reformat-django` для `djlint-django`. Хуки задают `--profile` и файлы, которые передаёт pre-commit. У `angular` своих хуков нет: добавьте `args: [--profile=angular]` к `djlint` или `djlint-reformat`.

| Хук                 | Профиль    | Файлы                                |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | нет        | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Для шаблонов с другими расширениями переопределите `files` в своей конфигурации, а если хук задаёт `types_or`, то и его, потому что pre-commit требует, чтобы совпадали оба. Подробнее в [документации pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

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

[MegaLinter](https://megalinter.io) включает djLint. Чтобы настроить его, выполните `npx mega-linter-runner --install`, а параметры описаны на [странице djLint в документации MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/).
