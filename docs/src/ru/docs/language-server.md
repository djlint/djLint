---
description: Запустите djLint как языковой сервер, чтобы получать находки при вводе и форматирование в любом редакторе с поддержкой LSP.
title: Языковой сервер
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, языковой сервер, lsp, neovim, zed, helix
---

# Языковой сервер

`djlint --lsp` запускает djLint как языковой сервер через stdio. Он продолжает работать, поэтому редактор получает находки при вводе и форматирует документ, не запуская каждый раз новый процесс.

Сервер сообщает о находках и форматирует документы целиком. Дополнительные пакеты ему не нужны.

В любом редакторе установите djLint туда, где редактор его найдёт, лучше всего в виртуальное окружение проекта, и запускайте редактор из него или укажите ему путь к `djlint` этого окружения. Тогда редактор будет использовать версию, закреплённую в проекте, и результаты совпадут с хуком pre-commit и CI.

## Visual Studio Code

Установите [расширение djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) или [его версию из Open VSX](https://open-vsx.org/extension/monosans/djlint) для VSCodium. Оно находит djLint в вашем окружении, использует встроенный, если djLint не установлен, и работает через языковой сервер, когда ваш djLint его поддерживает.

## Neovim

В Neovim 0.11 и новее:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Чтобы отформатировать документ, вызовите `vim.lsp.buf.format()`.

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

## Zed

Установите [расширение djLint](https://github.com/djlint/zed-djlint).

## Helix

В `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## IDE от JetBrains

В PyCharm и других IDE на базе IntelliJ используйте бесплатный плагин [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Установите LSP4IJ из Marketplace.
1. Откройте панель LSP Consoles и добавьте новый языковой сервер.
1. На вкладке **Server** укажите имя `djLint` и команду `djlint --lsp`, с полным путём к `djlint` из виртуального окружения проекта, если его нет в PATH.
1. На вкладке **Mappings** добавьте шаблон имён файлов, например `*.html`. Для проекта на Django укажите идентификатор языка `htmldjango`, чтобы выбрался нужный [профиль](/ru/docs/configuration/#profile).
1. На вкладке **Configuration** можно задать [настройки](#nastrojki) в JSON, в ключе `djlint`.

Находки появятся в редакторе, а **Reformat Code** сможет использовать сервер для этих файлов.

## Sublime Text

С пакетом [LSP](https://packagecontrol.io/packages/LSP) выполните **Preferences: LSP Server Configurations** и добавьте:

```json
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

## Emacs

Eglot, входящий в Emacs 29 и новее:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Затем выполните `M-x eglot` в шаблоне. `eglot-format-buffer` отформатирует его.

## Настройки

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

## Как это работает

- Находки приходят после короткой паузы в наборе. Редактор с pull-диагностикой запрашивает их сам, остальным сервер отправляет их сам.
- `exclude`, `extend_exclude` и `use_gitignore` действуют на открытые документы. У исключённого документа нет находок, и он не форматируется.
- Сервер перечитывает конфигурацию при изменении `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` или `.gitignore`, если редактор умеет следить за файлами.
