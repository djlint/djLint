---
title: "Jinja Template Linter and Formatter"
description: "djLint - это линтер шаблонов jinja и форматер шаблонов jinja! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Jinja"
---

djLint - это линтер шаблонов jinja и форматер шаблонов jinja! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Шаблоны MiniJinja полностью совместимы с Jinja2, поэтому используйте этот же профиль `jinja`.

Шаблоны Jinjava от HubSpot тоже в стиле jinja, поэтому используйте этот профиль и для них.

#### Использование командной строки

```bash
djlint /path/to/templates --profile=jinja
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile="jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
