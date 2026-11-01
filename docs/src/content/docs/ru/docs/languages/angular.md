---
title: "Angular Template Linter"
description: "djLint - это линтер шаблонов Angular! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Angular"
---

djLint - это линтер шаблонов Angular! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое Angular?](https://angular.io/guide/template-syntax)**

#### Использование командной строки

```bash
djlint /path/to/templates --profile=angular
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
