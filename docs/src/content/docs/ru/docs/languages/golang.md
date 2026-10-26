---
title: "Go Template Linter and Formatter"
description: "djLint - это линтер шаблонов Go и форматер шаблонов Go! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint."
sidebar:
  label: "Go templates"
---

djLint - это линтер шаблонов Go и форматер шаблонов Go! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.

**[Что такое шаблоны Go?](https://pkg.go.dev/text/template)**

На шаблонах Go (`text/template`, `html/template`) также работают темы Hugo и чарты Helm, поэтому используйте для них этот же профиль.

#### Использование командной строки

```bash
djlint /path/to/templates --profile=golang
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="golang"
```

```toml title="djlint.toml / .djlint.toml"
profile="golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::
