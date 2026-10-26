---
title: "Django Template Linter and Formatter"
description: "djLint - это линтер шаблонов django и форматер шаблонов django! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Django"
---

djLint - это линтер шаблонов django и форматер шаблонов django! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Использование командной строки

```bash
djlint /path/to/templates --profile=django
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
