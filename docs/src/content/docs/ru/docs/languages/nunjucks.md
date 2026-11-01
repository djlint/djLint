---
title: "Nunjucks Template Linter and Formatter"
description: "djLint - это линтер шаблонов nunjucks и форматер шаблонов nunjucks! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Nunjucks"
---

djLint - это линтер шаблонов nunjucks и форматер шаблонов nunjucks! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Nunjucks?](https://mozilla.github.io/nunjucks/)**

Шаблоны Pebble (Java) совместимы с Twig, поэтому используйте для них этот же профиль.

#### Использование командной строки

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
