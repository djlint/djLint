---
title: "Liquid Template Linter and Formatter"
description: "djLint - это линтер шаблонов Liquid и форматер шаблонов Liquid! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Liquid"
---

djLint - это линтер шаблонов Liquid и форматер шаблонов Liquid! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Liquid?](https://shopify.github.io/liquid/)**

Один профиль покрывает все диалекты Liquid: темы Shopify, Jekyll, LiquidJS (Eleventy) и Fluid (Orchard Core).

#### Использование командной строки

```bash
djlint /path/to/templates --profile=liquid
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
