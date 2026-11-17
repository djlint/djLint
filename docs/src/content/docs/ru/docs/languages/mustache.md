---
title: "Линтер и форматер шаблонов Mustache"
description: "djLint проверяет и форматирует шаблоны Mustache. Задайте профиль handlebars, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Mustache"
---

djLint проверяет и форматирует шаблоны Mustache. Задайте профиль `handlebars`, чтобы правила и форматирование подходили для них.

**[Что такое Mustache?](https://mustache.github.io/mustache.5.html)**

## Через командную строку

```bash
djlint /path/to/templates --profile=handlebars
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
