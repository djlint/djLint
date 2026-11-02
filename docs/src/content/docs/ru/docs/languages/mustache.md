---
title: "Линтер и форматер шаблонов Mustache"
description: "djLint — линтер и форматер шаблонов Mustache! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Mustache"
---

djLint — линтер и форматер шаблонов Mustache! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Mustache?](https://mustache.github.io/mustache.5.html)**

#### Через командную строку

```bash
djlint /path/to/templates --profile=handlebars
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
