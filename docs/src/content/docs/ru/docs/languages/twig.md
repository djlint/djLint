---
title: "Twig Template Linter and Formatter"
description: "djLint - это линтер шаблонов twig и форматировщик шаблонов twig! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Twig"
---

djLint - это линтер шаблонов twig и форматировщик шаблонов twig! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Twig?](https://twig.symfony.com/)**

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
