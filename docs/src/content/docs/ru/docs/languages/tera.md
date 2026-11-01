---
title: "Tera Template Linter and Formatter"
description: "djLint - это линтер шаблонов Tera и форматер шаблонов Tera! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Tera"
---

djLint - это линтер шаблонов Tera и форматер шаблонов Tera! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Tera?](https://keats.github.io/tera/)**

#### Использование командной строки

```bash
djlint /path/to/templates --profile=tera
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="tera"
```

```toml title="djlint.toml / .djlint.toml"
profile="tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
