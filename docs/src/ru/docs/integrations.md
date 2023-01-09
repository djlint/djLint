---
description: Интегрируйте djLint с вашим любимым редактором. Автоматическое форматирование ваших шаблонов с помощью Pre-Commit или Visual Studio Code. Lint с SublimeText.
title: Интеграции
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, integrations
---

# {{ "integrations" | i18n }}

Существует несколько интеграций редакторов для djLint.

## Pre-Commit

djLint можно использовать как [pre-commit](https://pre-commit.com) крючок.

Репозиторий предоставляет несколько предварительно настроенных хуков для определенных профилей djLint (он просто задает аргумент `--profile` и указывает pre-commit, какие расширения файлов искать):

::: content

- `djlint-django` для шаблонов Django:
  Это будет искать файлы, соответствующие `templates/**.html` и устанавливать `--profile=django`.
- `djlint-jinja`.
  Это будет искать файлы, соответствующие `*.j2` и устанавливать `--профиль=jinja`.
- `djlint-nunjucks`.
  Будет искать файлы, соответствующие `*.njk` и устанавливать `--profile=nunjucks`.
- `djlint-handlebars`
  Будет искать файлы, соответствующие `*.hbs` и устанавливать `--profile=handlebars`.
- `djlint-golang`
  Будет искать файлы, соответствующие `*.tmpl` и устанавливать `--profile=golang`.
  :::

Обратите внимание, что эти предопределенные хуки иногда слишком консервативны в принимаемых ими входных данных (ваши шаблоны могут использовать другое расширение), поэтому pre-commit явно позволяет вам переопределять любые из этих предопределенных опций. См. [pre-commit документы](https://pre-commit.com/#pre-commit-configyaml---hooks) для дополнительной настройки.

### Пример Django по умолчанию

```yaml
repos:
  - repo: https://github.com/Riverside-Healthcare/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-django
```

### Handlebars с расширением .html вместо .hbs

```yaml
repos:
  - repo: https://github.com/Riverside-Healthcare/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-handlebars
        files: "\\.html"
        types_or: ['html']
```

Вы можете использовать параметры `files` или `exclude`, чтобы ограничить каждый хук своим каталогом, что позволит вам поддерживать несколько языков шаблонов в одном репозитории.

## SublimeText Linter

djLint можно использовать в качестве плагина SublimeText Linter. Его можно установить через [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shft + p`
2. Install SublimeLinter
3. Install SublimeLinter-contrib-djlint
   :::

Убедитесь, что djLint установлен в вашем глобальном python или в вашем `PATH`.

## Visual Studio Code

::: content

- [GitHub репозиторий](https://github.com/monosans/djlint-vscode)
- [Страница на VS Marketplace](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
- [Страница на Open VSX](https://open-vsx.org/extension/monosans/djlint)
  :::

## neovim

djLint можно использовать в качестве форматера в neovim с помощью плагина `null-ls`.

::: content

- [GitHub репозиторий](https://github.com/jose-elias-alvarez/null-ls.nvim/)
- [Пример конфигурации](https://github.com/shaeinst/roshnivim/blob/5d991fcfa1b8f865f9653a98c6d97a829d4a2add/lua/plugins/null-ls_nvim.lua#L84-L91)
  :::

## coc.nvim

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::
