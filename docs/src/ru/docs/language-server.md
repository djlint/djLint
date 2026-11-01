---
description: Запустите djLint как языковой сервер, чтобы получать находки при вводе и форматирование в любом редакторе с поддержкой LSP.
title: Языковой сервер
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, языковой сервер, lsp, neovim, zed, helix
---

# Языковой сервер

`djlint --lsp` запускает djLint как языковой сервер через stdio. Он продолжает работать, поэтому редактор получает находки при вводе и форматирует документ, не запуская каждый раз новый процесс.

Сервер сообщает о находках и форматирует документы целиком. Дополнительные пакеты ему не нужны.

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
language-servers = ["vscode-html-language-server", "djlint"]
formatter = { command = "djlint", args = ["--reformat", "--quiet", "-"] }
```

## Настройки

Сервер читает [конфигурацию](/ru/docs/configuration/) проекта так же, как командная строка: от папки каждого файла вверх. Настройки редактора важнее неё. Их имена совпадают с [опциями командной строки](/ru/docs/configuration/), с подчёркиваниями или в camelCase, а значения через запятую можно задавать списками:

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
- Сервер перечитывает конфигурацию при изменении `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc` или `.gitignore`, если редактор умеет следить за файлами.
