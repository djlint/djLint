---
title: "Линтер и форматер шаблонов Handlebars"
description: "djLint — линтер и форматер шаблонов Handlebars! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Handlebars"
---

djLint — линтер и форматер шаблонов Handlebars! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Handlebars?](https://handlebarsjs.com/)**

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
