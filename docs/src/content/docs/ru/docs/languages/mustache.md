---
title: "Mustache Template Linter and Formatter"
description: "djLint - это линтер шаблонов mustache и форматировщик шаблонов mustache! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Mustache"
---

djLint - это линтер шаблонов mustache и форматировщик шаблонов mustache! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Mustache?](https://mustache.github.io/mustache.5.html)**

#### Использование командной строки

```bash
djlint /path/to/templates --profile=handlebars
```

#### Или используйте файл конфигурации

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
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
