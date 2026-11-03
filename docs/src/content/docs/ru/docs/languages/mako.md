---
title: "Линтер и форматер шаблонов Mako"
description: "djLint проверяет и форматирует шаблоны Mako. Задайте профиль mako, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Mako"
---

djLint проверяет и форматирует шаблоны Mako. Задайте профиль `mako`, чтобы правила и форматирование подходили для них.

**[Что такое Mako?](https://www.makotemplates.org/)**

С профилем mako управляющая строка вроде `% if x:` и комментарий `##` всегда остаются на отдельной строке, а тег, атрибуты которого зависят от управляющих строк, сохраняет их как написано. Блоки Python и содержимое `<%doc>` и `<%text>` не меняются, как и script или style с синтаксисом Mako при `--format-js` или `--format-css`. Строки между `% if` и `% endif`, а также между тегом `<%block>` или `<%def>` и его закрывающим тегом, если каждый стоит на отдельной строке, получают отступ, как в любом другом блоке. Код в выражении `${}` остаётся как написано.

## Через командную строку

```bash
djlint /path/to/templates --profile=mako
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
